import subprocess
import sys 

def kill_firefox_processes():
    if sys.platform == 'win32':
        subprocess.call('taskkill /F /IM firefox.exe', shell=True)
    elif sys.platform == 'linux':
        subprocess.call('killall firefox', shell=True)
    elif sys.platform == 'darwin':
        subprocess.call('killall Firefox', shell=True)

kill_firefox_processes()