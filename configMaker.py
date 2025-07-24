import configparser
import os

class ConfigLoader:
    def __init__(self, path="config.ini"):
        self.path = path
        self.config = configparser.ConfigParser()
        self.last_mod = None
        self.load_or_create_config()

    def load_or_create_config(self):
        if os.path.exists(self.path):
                self.config.read(self.path)
                self.last_mod = os.path.getmtime(self.path)
        else:
             self.config['limits'] = {
                    "cpu" : "90",
                    "memory" : "90",
                    "disk" : "80"
             }

             with open(self.path, 'w')as configfile:
                  self.config.write(configfile)
                  print(f"nie znaleziono pliku 'config.ini', stworzono domyślny w {self.path}")
                  
                
                  
                
    def reload_if_changed(self):
         current_mtime = os.path.getmtime(self.path)
         if current_mtime != self.last_mod:
              print("[INFO] Config changed, Reloading")
              self.load_or_create_config()


    def get_limit(self, name, default = 90):
        try:
            return int(self.config["limits"].get(name, default))
        except (KeyError, ValueError):
            return default
        
    def get_log_interval(self, name, default = 3600): # TODO: Dopisać sterowanie czasem zbierania
         try:
            return int(self.config["log_time"].get(name, default))
         except (KeyError, ValueError):
              return default



