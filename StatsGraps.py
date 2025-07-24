import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk
import threading
import time

from monitor import SystemMonitor


class BaseGraph(tk.Frame):
    def __init__(self, parent, title,  get_data_callback, interval=1000, y_range=(0,100)):
        super().__init__(parent)
        self.parent=parent
        self.get_data = get_data_callback
        self.interval = interval
        self.latest_value = 0
        self.data =[0]*60

        self._setup_figure(title, y_range)
        self._start_data_thread()
        self.update_graph()

    def _setup_figure(self, title, y_range):
        self.fig = Figure(figsize=(5, 2), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title(title)
        self.ax.set_ylim(*y_range)
        self.ax.set_xlabel("Czas (s)")
        self.ax.set_ylabel("Wartość (%)")
        self.ax.grid()
        self.line, = self.ax.plot(self.data)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def _start_data_thread(self):
        threading.Thread(target=self._data_collector_thread, daemon=True).start()

    def _data_collector_thread(self):
        while True:
            try:
                self.latest_value = self.get_data()
            except Exception as e:
                print(f'[Thread Error] {e}')
            time.sleep(self.interval / 1000)

    def update_graph(self):
        try:
            self.data.append(self.latest_value)
            self.data = self.data[-60:]
            self.line.set_ydata(self.data)
            self.line.set_xdata(range(len(self.data)))
            self.ax.relim()
            self.ax.autoscale_view()
            self.canvas.draw()
        except Exception as e:
            print(f"[Update Error] {e}")

        self.after(self.interval, self.update_graph)


class MetricGraph(BaseGraph):
    def __init__(self, parent, title, get_data_callback, interval=1000, y_range=(0, 100)):
        super().__init__(parent, title, get_data_callback, interval, y_range)






