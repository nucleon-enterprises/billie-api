import os
import psutil

def getsys():
    for proc in psutil.process_iter():
        print(proc.name)
