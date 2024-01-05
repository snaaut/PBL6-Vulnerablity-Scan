import gevent
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import traceback
from urllib.parse import urljoin
import requests
import re
from driver import getDriver

class SSRF_Scanner():
    def __init__(self, page, app):
        print("Starting SSRF scan")
        try : 
            self.payloads = ["http://127.0.0.1/","http://0.0.0.0","http://localhost:80","http://2130706433","http://localhost/"]
            self.threadsEnCours = False
            self.page =page
            self.threads = []
            self.vulnFound=None
            self.vitesse = 4
           #self.vitesse = app.getSpeedScan()

            self.startScan(app)
        except :
            app.webScanner.error.append("SSRF scan crash with error : "+traceback.format_exc())
            return

    def getVulnFound(self):
        return self.vulnFound

    def startScan(self,app):
        try :
            if self.vitesse == 1:
                sous_liste = [self.payloads]
            else:
                taille_sous_liste = len(self.payloads) // self.vitesse
                reste = len(self.payloads) % self.vitesse
                sous_liste = []
                debut = 0
                for i in range(self.vitesse):
                    fin = debut + taille_sous_liste
                    if i < reste:
                        fin += 1 
                    sous_liste.append(self.payloads[debut:fin])
                    debut = fin
        except:
            app.webScanner.error.append("Critical error cuttting payloads SSRF"+traceback.format_exc())
            return   
        groupesPayload=[]
        for groupe in sous_liste:
            if not(groupe == [] or groupe == None or groupe == "" or groupe == [ ]):
                groupesPayload.append(groupe)

        self.threadsEnCours = True
        try:
            threads = [gevent.spawn(self.checkSSRF, self.page, groupesPayload[i],app) for i in range(len(groupesPayload))]
            gevent.joinall(threads)
        except:
            app.webScanner.error.append("Critical error multi threading !!! Please contact support."+traceback.format_exc())
            print("ending SSRF scan")


    def checkSSRF(self,page=None, payloads=[],app=None):
        try : 
            driver = getDriver(app)
            if driver == None :
                app.webScanner.error.append("The browser driver does not exist. SSRF analysis failed. Please check your software settings and or configurations.")
                return
            for method in ["GET", "POST"]:
                for payload in payloads:  
                    if self.threadsEnCours :
                        driver.get(self.page)
                        #đợi web load xong
                        WebDriverWait(driver, 10).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
                        forms = driver.find_elements(By.XPATH, "//form")
                        ancientHTML = driver.page_source
                        for form in forms:
                            input_element = form.find_element(By.TAG_NAME, "input")
                            input_element.send_keys(payload)
                            input_element.send_keys(Keys.ENTER)
                            if method == "GET":
                                try : 
                                    driver.get(urljoin(self.page, form.get_attribute("action") + "?" + form.text))
                                except : 
                                    pass
                            else:
                                try :
                                    submit_button = driver.find_element(By.XPATH, "//input[@type='submit']")
                                    submit_button.click()
                                except :
                                    pass 
                            # Phân tích phản hồi
                            response = requests.get(driver.current_url, timeout=5)
                            html = response.text
                            actualHTML = driver.page_source
                            if response.status_code == 200 and ancientHTML!=actualHTML:
                                print("possible faille analyse...")
                                html = response.text
                                if not re.search(r"<form(.*)"+payload+r"(.)+</form>", html, re.DOTALL):
                                    self.vulnFound="⚠ Possible SSRF vulnerability on : " + str(page) + " with : "+payload+" Currently, SSRF scanning can produce many false positives."
                                    driver.quit()
                                    return

                            time.sleep(0.1)
                    else :
                        driver.quit()
                        return
            return
        except :
            app.webScanner.error.append("Error during SSRF analyse "+traceback.format_exc())
            driver.quit()
            return
        
    

