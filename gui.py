import sys
import tkinter as tk
from tkinter import ttk, messagebox
from database.models import Alert, init_db
import os
import time
from MonitorThread import MonitorThread
from monitor import SystemMonitor
from StatsGraps import MetricGraph

class Application:
    def __init__(self, root, monitor_thread):
        self.root = root
        self.monitor_thread = monitor_thread
        self.net_counters_reset = {}
        self.monitor = SystemMonitor()
        self.root.title("System Monitor")
        self.root.geometry("800x600")
       # self.root.resizable(width=False, height=False)
        self.root.minsize(400,300)
        
        self.root.call('wm', 'attributes', '.', '-topmost', '1')
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.setup_widgets()
        self.auto_refresh()
        self.update_network_stats()
        
    
#        self.setup_stats_combo

    def setup_widgets(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)
        self.notebook.pack(fill='both', expand=True)
        self.setup_alerts_tab()
        self.setup_stats_tab()
        self.load_alerts()
        self.setup_network_tab()
        self.setup_log_tab()
        # self.load_stats()

    def setup_alerts_tab(self):
        self.alerts_frame = tk.Frame(self.notebook)
        self.tree = ttk.Treeview(
            self.alerts_frame,
            columns=("timestamp", "message", "user"),
            show='headings'
        )
        self.tree.heading("timestamp", text="Czas", anchor="center")
        self.tree.heading("message", text="Wiadomość", anchor="center")
        self.tree.heading("user", text="Użytkownik", anchor="center")
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.clear_alerts_button = tk.Button(self.alerts_frame, text="Clear", command=self.clear_alerts)
        self.load_alerts_button = tk.Button(self.alerts_frame, text="refresh", command=self.load_alerts)
        self.load_alerts_button.pack(side=tk.LEFT, padx=5)
        self.clear_alerts_button.pack(side=tk.RIGHT, padx=5)
        self.notebook.add(self.alerts_frame, text="Alerts")
        #self.setup_stats_tab()

        self.load_alerts()
#        self.load_stats()



    def setup_stats_tab(self):
        self.stats_frame = tk.Frame(self.notebook)
        self.notebook.add(self.stats_frame, text="Resource Graphs")

        self.metric_callbacks = {
            "CPU": lambda: self.monitor.get_cpu_usage(),
            "Memory": lambda: self.monitor.get_memory_info().get("percent", 0),
            "Disk": lambda: self.monitor.get_disk_usage().get("percent", 0),
            
        }

    
        self.metric_selector = ttk.Combobox(
            self.stats_frame,
            values=list(self.metric_callbacks.keys())
        )
        self.metric_selector.set("CPU")
        self.metric_selector.pack(pady=10)

        
        self.current_graph = MetricGraph(
            parent=self.stats_frame,
            get_data_callback=self.metric_callbacks["CPU"],
            title = None,
            interval=1000,
            y_range=(0, 100)
        )
        self.current_graph.pack(fill="both", expand=True)
        

        self.metric_selector.bind("<<ComboboxSelected>>", self.on_metric_change)


    def setup_network_tab(self):
        self.network_frame= tk.Frame(self.notebook)
        self.notebook.add(self.network_frame, text="Network")

        self.network_frame.grid_columnconfigure(0, weight=1)
        self.network_frame.grid_columnconfigure(1, weight=1)
        
        

        self.network_labels = {
            "bytes_sent" : tk.Label(self.network_frame),
            "bytes_recv" : tk.Label(self.network_frame),
            "packets_sent" : tk.Label(self.network_frame),
            "packets_recv" : tk.Label(self.network_frame),
            "errin": tk.Label(self.network_frame),
            "errout": tk.Label(self.network_frame),
            "dropin": tk.Label(self.network_frame),
            "dropout": tk.Label(self.network_frame)
        }

        self.network_frame.grid_rowconfigure(len(self.network_labels) + 1, weight=1)

        for i, label in enumerate(self.network_labels.values()):
            label.grid(row=i, column=0, sticky="w", columnspan=2 ,padx=10, pady=2)
        self.clear_stats = tk.Button(self.network_frame, text="Reset counters", command=self.reset_net_counters)
        self.clear_stats.grid(row=len(self.network_labels), column=1, sticky="sw", padx=10, pady=15)
        self.display_text = tk.StringVar()
        self.display_text.set("Current Data Flow:")
        self.display = tk.Label(self.network_frame, textvariable=self.display_text)
        self.display.grid(row=18, column=0, sticky="w", padx=10)
        self.upload_label = tk.Label(self.network_frame, text="Upload: 0 kB/s")
        self.upload_label.grid(row=19, column=0, sticky="w", padx=10, pady=0)
        self.download_label = tk.Label(self.network_frame, text="Download: 0 kB/s")
        self.download_label.grid(row=21, column=0, sticky="w", padx=10)

    def setup_log_tab(self):
        
        self.log_tab = tk.Frame(self.notebook)
        self.notebook.add(self.log_tab, text="Logs")
        self.items_list = tk.Listbox(self.log_tab, width=32)
        self.items_list.grid(row=0, column=0, sticky="nsew", padx=(5,10),pady=(10,5))
        self.log_tab.grid_rowconfigure(0, weight=1, pad=10)
        self.text_area = tk.Text(self.log_tab, wrap="word")
        self.text_area.grid(row=0, column=1, sticky="nsew", padx=(0, 10), pady=(10, 5))
        self.log_tab.grid_rowconfigure(0, weight=1)
        self.log_tab.grid_columnconfigure(1, weight=1)
        self.scroll_bar = tk.Scrollbar(self.log_tab, command=self.text_area.yview, cursor="double_arrow", activerelief="ridge", jump=0, width=15)
        self.scroll_bar.grid(row=0, column=2, sticky="ns", pady=(10, 5))
        self.text_area.config(yscrollcommand=self.scroll_bar.set)
        self.items_list.bind("<<ListboxSelect>>", self.load_selected_log)

    def load_selected_log(self, event):
        selection = event.widget.curselection()
        if not selection:
            return
        
        index = selection[0]
        file_name = event.widget.get(index)
        file_path = os.path.join("logs", file_name)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
                content = f"Can't parse {file_name} file due to: {e}"
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert(tk.END, content)


    def refresh_log_list(self):
        path = "logs"
        self.items_list.delete(0, tk.END)

        files_list = sorted(
            (f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))),
            key=lambda f: os.path.getmtime(os.path.join(path, f)),
            reverse=True
        )

        for file_name in files_list:
            if "sys_log" in file_name and file_name.endswith(".json"):
                self.items_list.insert(tk.END, file_name)


        
        


    def update_network_stats(self):
        stats = self.monitor.get_net_io_count()

        self.network_descriptions = {
            "bytes_sent": "Bytes out ",
            "bytes_recv": "Bytes in ",
            "packets_sent": "Packets out ",
            "packets_recv": "Packets in ",
            "errin": "Number of errors while receiving ",
            "errout": "Number of errors while sending ",
            "dropin": "Number of incoming packets which were dropped ",
            "dropout": "Number of outgoing packets which were dropped "
}
        for key, label in self.network_labels.items():
            base = self.net_counters_reset.get(key, 0)
            value = stats.get(key, 0) - base
            description = self.network_descriptions.get(key, key)
            label.config(text=f"{description}: {value}")
        self.root.after(1000, self.update_network_stats)

        movement = self.monitor.get_net_movement()
        upload = movement["upload"]/1024
        download = movement["download"]/1024
        self.upload_label.config(text=f"Upload ↑ {upload:.2f} KB/s")
        self.download_label.config(text=f"Download ↓ {download:.2f} KB/s")


    def on_metric_change(self, event):
        try:
            selected_metric = self.metric_selector.get()

            if hasattr(self, 'current_graph'):
                # self.current_graph.stop()  
                self.current_graph.destroy()

            callback = self.metric_callbacks.get(selected_metric)
            y_range = (0, 100)  

            self.current_graph = MetricGraph(
                parent=self.stats_frame,
                title=selected_metric,
                get_data_callback=callback,
                interval=200,
                y_range=y_range
            )
            self.current_graph.pack(fill="both", expand=True)
        except Exception as e:
            print(f"Error: {e}")

    def on_tab_change(self,event):
        tab_index = self.notebook.index(self.notebook.select())
        tab_text = self.notebook.tab(tab_index, "text")
        if tab_text == "Logs":
            self.refresh_log_list()


    def load_alerts(self):
        self.tree.delete(*self.tree.get_children())
        for alert in Alert.select().where((Alert.hidden == False) | (Alert.hidden.is_null(True))).order_by(Alert.timestampField.desc()):
            self.tree.insert("", tk.END, values=(
                alert.timestampField.strftime("%d/%m/%Y %H:%M:%S"),
                alert.message,
                alert.user.name if alert.user else "Brak"
            ))

    def clear_alerts(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        query = Alert.update(hidden=True).where(Alert.hidden == False)
        query.execute()

    def reset_net_counters(self):
        stats = self.monitor.get_net_io_count()
        self.net_counters_reset = stats.copy()
        for key, label in self.network_labels.items():
            description = self.network_descriptions.get(key,key)
            label.config(text=f"{description}:0")


    def auto_refresh(self):
        self.load_alerts()
        self.root.after(5000, self.auto_refresh)  # odświeżaj co 5 sekund

    def on_close(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.withdraw()
            if hasattr(self.monitor_thread, "stop"):
                self.monitor_thread.stop()
            if self.monitor_thread.is_alive():
                self.monitor_thread.join(timeout=5)
            self.root.destroy()



    

if __name__ == "__main__":
    init_db()
    monitor_thread = MonitorThread()
    monitor_thread.start()
    root = tk.Tk()
    app = Application(root, monitor_thread)
    root.mainloop()

