#WARNING : this file is deprecated and should not be used anymore. It is kept for historical reasons only.

import time
from selenium import webdriver
import os 
import sys
import json
import traceback
from datetime import datetime, timedelta
import gevent
from selenium.common.exceptions import UnexpectedAlertPresentException,NoAlertPresentException
driversStorage=[]
driverStorageController =[-1,""]#[0] : dernier driver fourni / [1] : scan en cours

def createADriver(app):
    driver=None
    try : 
        if app.varBrowser.get()=="Firefox":
            options = webdriver.FirefoxOptions()
            options.add_argument('-headless')
            driver =  webdriver.Firefox(options=options)
        elif app.varBrowser.get()=="Chrome" :
            options = webdriver.ChromeOptions()
            options.add_argument('-headless')
            driver = webdriver.Chrome(options=options)
        elif app.varBrowser.get()=="Safari" :
            driver = webdriver.Safari()
        elif app.varBrowser.get()=="Edge" :
            options = webdriver.EdgeOptions()
            options.add_argument('-headless')
            driver = webdriver.Edge(options=options)
        #chargement page vide :
        cookies_path = "caches/cookies.json"
        if driver != None:
            if os.path.exists(cookies_path):
                with open(cookies_path, "r") as f:
                    if f != "" and os.path.getsize(cookies_path) > 0 and f != None:
                        cookies = json.load(f)
                        for cookie in cookies:
                            nom = cookie[0]
                            valeur = cookie[1]
                            domain = cookie[2]
                            cookie ={
                                    'name':str(nom),
                                    'value': str(valeur),
                                    'domain': str(domain),
                                    'path': '/',
                                    'expiry': int((datetime.utcnow() + timedelta(days=30)).timestamp()),
                                    'httpOnly': True,
                                    'secure': False,
                                    'sameSite': 'Lax',
                                    'partitionKey':'default',
                                    'priority': 'Medium'
                                    }
                            try : 
                                if "https" in domain :
                                    driver.get(domain)
                                else : 
                                    #nettoyage du domaine: 
                                    if domain[0]=="." or domain[0]=="/":
                                        domain=domain[1:]
                                    driver.get("https://"+str(domain))
                                driver.add_cookie(cookie)
                            except:
                                if app.language == "fr":
                                    app.webScanner.error.append("Le navigateur n'est pas parvenu à ajouter un cookie veuillez verifier que le nom de domain est correct:"+traceback.format_exc())
                                elif app.language == "en":
                                    app.webScanner.error.append("The browser failed to add a cookie please check that the domain name is correct:"+traceback.format_exc())
                f.close()
        return driver
    except:
        if app.language == "fr":
            app.webScanner.error.append("Un problème liè au navigateur est survenu. Veuillez verifier dans les réglages que votre selection est la bonne. Navigateur selectioné actuellement :"+ app.varBrowser.get()+ "Rapport de Crash : "+ "Le navigateur n'est pas parvenu à ajouter un cookie veuillez verifier que le nom de domain est correct:"+traceback.format_exc())
        elif app.language == "en":
            app.webScanner.error.append("A browser related problem has occurred. Please check in the settings that your selection is correct. Currently selected browser :"+ app.varBrowser.get()+ "Crash report : "+ "The browser failed to add a cookie please check that the domain name is correct:"+traceback.format_exc())
        driver.quit()
        return None

def createDrivers(app):
    global driversStorage
    #this function create all the drivers needed for all scan 1 driver / speed set
    for i in range (app.getSpeedScan()) :
        print("starting a brower")
        driver = gevent.spawn(createADriver, app).get()
        if driver != None :
            driversStorage.append(driver)
        print("a browser is ready")

def getDriver(app, typeOfScan):
        #return a driver for direct use
        global driversStorage, driverStorageController
        if driverStorageController[1] == typeOfScan:
            driver = driversStorage[driverStorageController[0]+1]
            driverStorageController[0] += 1
            print("driverStorageController[0] : ",driverStorageController, "len(driversStorage) : ",len(driversStorage))
            while True:
                try:
                    driver.get("https://google.com")
                    break
                except UnexpectedAlertPresentException:
                    print("alert detected")
                    try:
                        alert = driver.switch_to.alert
                        alert.accept()
                    except NoAlertPresentException:
                        print("No alert present, continuing...")
                        break   
            return driver
        else : 
            driverStorageController[0] = -1
            driverStorageController[1] = typeOfScan
            driver = driversStorage[0]
            print("First get of type of scan","driverStorageController[0] : ",driverStorageController, "len(driversStorage) : ",len(driversStorage))
            while True:
                try:
                    driver.get("https://google.com")
                    print("pas d'alerte")
                    break
                except UnexpectedAlertPresentException:
                    print("alert detected")
                    try:
                        alert = driver.switch_to.alert
                        alert.accept()
                    except NoAlertPresentException:
                        print("No alert present, continuing...")
                        break
            return driver
        
def closeDrivers():
    global driversStorage
    if driversStorage == []:
        return
    for driver in driversStorage:
        driver.quit()
    driversStorage=[]
