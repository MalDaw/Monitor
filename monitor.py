from statistics import pstdev
import psutil as psu
import getpass as gp
from datetime import datetime as dt
import socket
import time


class SystemMonitor:
    def __init__(self):
        self.net_baseline = psu.net_io_counters()
        self._last_net_snap = psu.net_io_counters()

    def get_net_movement(self):
        current = psu.net_io_counters()
        prev = self._last_net_snap

        movement = {
            "upload": current.bytes_sent - prev.bytes_sent,
            "download": current.bytes_recv - prev.bytes_recv
        }

        self._last_net_snap = current
        return movement

    def get_cpu_usage(self, interval = 1):
        return psu.cpu_percent(interval)
    
    def get_memory_info(self):
        memo = psu.virtual_memory()
        return memo._asdict()
    
    def get_username(self):
        return gp.getuser()
    
    def get_time(self):
        return dt.now().strftime("%H:%M:%S")
    
    def get_disk_usage(self, path = '/'):
        return psu.disk_usage(path)._asdict()
    
    def get_disk_io_count(self, perdisk=False, nowrap=True):
        return psu.disk_io_counters(perdisk, nowrap)._asdict()
    
    def get_net_io_count(self, pernic=False, nowrap=True):
        current = psu.net_io_counters()
        baseline = self.net_baseline

        return {
                "bytes_sent": current.bytes_sent - baseline.bytes_sent,
                "bytes_recv": current.bytes_recv - baseline.bytes_recv,
                "packets_sent": current.packets_sent - baseline.packets_sent,
                "packets_recv": current.packets_recv - baseline.packets_recv,
                "errin": current.errin - baseline.errin,
                "errout": current.errout - baseline.errout,
                "dropin": current.dropin - baseline.dropin,
                "dropout": current.dropout - baseline.dropout
        }

        #return psu.net_io_counters(pernic, nowrap)._asdict()

    def reset_net_counters(self):
        self.net_baseline = psu.net_io_counters()


        
    
    def get_net_conns(self, kind="all"):
        connections = psu.net_connections(kind)
        result = []

        for conn in connections:
            try:
                result.append({
                    "fd": conn.fd,
                    "family": conn.family,
                    "type": conn.type,
                    "laddr": f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "",
                    "raddr": f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "",
                    "status": conn.status,
                    "pid": conn.pid if conn.pid != None else "not found"
                })
            except Exception:
                continue  

        return result


    







    


         