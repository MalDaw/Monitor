import threading
from manager import MonitorManager


class MonitorThread(threading.Thread):
    def __init__(self, interval=5):
        super().__init__(daemon=True)
        self.interval = interval
        self.manager = MonitorManager()
        self._stop_event = threading.Event()


    def run(self):
        while not self._stop_event.is_set():
            self.manager.run()
            self._stop_event.wait(self.interval)

    def stop(self):
        self._stop_event.set()
