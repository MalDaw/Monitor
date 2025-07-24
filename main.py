import time
from monitor import SystemMonitor
import json
from logger import JSONLogger
from database.models import init_db

from manager import MonitorManager


monitor = SystemMonitor()
manager = MonitorManager()
logger = JSONLogger()


init_db()
print(monitor.get_net_io_count())

    

