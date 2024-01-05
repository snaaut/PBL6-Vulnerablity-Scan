from selenium import webdriver
import os 
import json
import traceback
from datetime import datetime, timedelta

def getDriver(app):
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
                        if f != []:
                            for cookie in cookies:
                                print("adding cookie : ",f)
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
        try :
            driver.quit()
            return None
        except :
            driver =None
        return None