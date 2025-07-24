import json
import os
from datetime import datetime as dt

class JSONLogger:
    def __init__(self, prefix = "logs/sys_log", indent = 4):
        self.prefix = prefix
        self.indent = indent
        os.makedirs("logs", exist_ok= True)

    def log(self, data: dict):
        data_str = dt.now().strftime("%Y-%m-%d")
        filename = f"{self.prefix}_{data_str}.json"

        if os.path.exists(filename):
             with open(filename, "r") as f:
                try:
                    logs = json.load(f)
                except json.JSONDecodeError:
                    logs = []
        else:
            logs = []

        logs.append(data)

        with open(filename, "w") as f:
            json.dump(logs, f, indent = self.indent)
