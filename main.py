"""
Warning : 
To run Security Scan please install dependances : 
python 3.7 or highter and download library : 
'pip install -r requirements.txt --user' or 'pip install -r requirements.txt'

Please note that you must ask the administrator for permission before using this tool on his site.
Security Scan cannot be held responsible for any abuse. 
You are responsible for your actions.

Thank's
"""

import traceback
from gevent import monkey
monkey.patch_all()
import locale
import app
from tkinter import *
import json

version = "0.0.14"#Security Scan version
root = ""

#khỏi chạy trình quét bảo mật
with open("caches/save.json", "r") as fichier:
    try :
        data = json.load(fichier)
        isfirstStart=data["firstStart"]
    except :
        data = None
        if not data or data == None:
            isfirstStart = True
    
    fichier.close()
#checkLastRelease()
try :
    print(" Warning : \n Please note that you must ask the administrator for permission before using this tool on his site. \n Security Scan cannot be held responsible for any abuse. \n You are responsible for your actions. ")
    software=app.App("en", isfirstStart) 
except  :
    print("Critical error during starting of Security Scan")

