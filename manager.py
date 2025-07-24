from monitor import SystemMonitor
from logger import JSONLogger
import configMaker
from utils import add_metadata
from datetime import datetime as dt
import time
import socket
from database.models import init_db
import Alert_log

class MonitorManager:
    def __init__(self):
        self.monitor = SystemMonitor()
        self.logger = JSONLogger()
        self.config = configMaker.ConfigLoader("config.ini")
        init_db()
        self.alert_logger = Alert_log.AlertLogger()
        self.latest_metrics = {}

    @add_metadata("CPU_usage")
    def cpu(self):
        return self.monitor.get_cpu_usage()
    

    @add_metadata("Memory_info")
    def memory(self):
        return self.monitor.get_memory_info()
    
    @add_metadata("Disk_usage")
    def disk(self):
        return self.monitor.get_disk_usage()


    @add_metadata("Net IO")
    def net_io(self):
        return self.monitor.get_net_io_count()
    
    #@add_metadata("Alerts")
    def check_alerts(self, metrics):
        alerts = []
        self.config.reload_if_changed()
        cpu_limit = self.config.get_limit("cpu")
        disk_limit = self.config.get_limit("disk")
        memory_limit = self.config.get_limit("memory")

        for metric in metrics:
            if metric["title"] == "CPU_usage" and metric["data"] > cpu_limit:
                alerts.append(f"CPU usage is {metric['data']}% (limit: {cpu_limit}%)")

            if metric["title"] == "Memory_info" and metric["data"]["percent"] > memory_limit:
                alerts.append(f"Memory usage is {metric['data']['percent']}% (limit: {memory_limit}%)")

            if metric["title"] == "Disk_usage" and metric["data"]["percent"] > disk_limit:
                alerts.append(f"Disk usage is {metric['data']['percent']}% (limit: {disk_limit}%)")

        return alerts
    
    def run(self):
        data = {
            "timestamp": dt.now().isoformat(),
            "user": self.monitor.get_username(),
            "hostname": socket.gethostname(),
            "metrics": [
                self.cpu(),
                self.memory(),
                self.disk(),
                self.net_io(),
            ]
        }

        self.latest_metrics = {
            "cpu": data["metrics"][0]["data"],          
            "memory": data["metrics"][1]["data"]["percent"],  
            "disk": data["metrics"][2]["data"]["percent"],    
            "net_io": data["metrics"][3]["data"]   
        }

        alerts = self.check_alerts(data["metrics"])
        if alerts:
            for alert in alerts:
                print(alert)
                self.alert_logger.log_alert(
                    message = alert,
                    source = self._extract_source_from_alert(alert),
                    user = data["user"]
                )
        self.logger.log(data)

    def get_metric(self, name):
        return self.latest_metrics.get(name, 0)

    def _extract_source_from_alert(self, alert_text):
        if "CPU" in alert_text:
            return "CPU"
        elif "Memory" in alert_text:
            return "Memory"
        elif "Disk" in alert_text:
            return "Disk"
        else:
            return "unknown"

        
    