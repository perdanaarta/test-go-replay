import datetime
import os

class Logger:
    def __init__(self, appname: str):
        self.appname = appname

    def __time_now(self) -> str:
        now = datetime.datetime.now()
        return(now.strftime("%Y-%m-%d %H:%M:%S"))
    
    def __write(self, message):
        with open(f"/home/arta/test_server/{self.appname}.log", "a") as f:
            f.write(f"{message}\n")

    def info(self, message):
        msg = f"{self.__time_now()} [{self.appname}] [INFO] {message}"
        self.__write(msg)
        print(msg)
    
    def warn(self, message):
        msg = f"{self.__time_now()} [{self.appname}] [WARN] {message}"
        self.__write(msg)
        print(msg)

    def error(self, message):
        msg = f"{self.__time_now()} [{self.appname}] [ERROR] {message}"
        self.__write(msg)
        print(msg)
