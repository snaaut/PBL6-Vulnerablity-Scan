import re
from selenium.webdriver.support.ui import WebDriverWait
import traceback
from driver import getDriver
class LFI_RFI_Scanner():
    # LFI and RFI vulnerabilities
    def __init__(self, page, app) -> None:
        try : 
            self.page =page
            self.vulnFound=None
            self.startScan(app)
        except :
            app.webScanner.error.append("Due to a serious error the search could not be executed."+traceback.format_exc())
            return

    def getVulnFound(self):
        return self.vulnFound

    def startScan(self,app):
        #phân tích các lỗ hổng LFI/RFI trong các biểu mẫu
        print("Start LFI/RFI scan")
        driver = getDriver(app)
        if driver == None :
            app.webScanner.error.append("The browser driver does not exist. XSS analysis failed. Please check your software settings and or configurations.")
            return
        if re.search(r"(file=|path=|files=)", self.page):#kiểm tra xem trang web có hoạt động với tham số file= hoặc path= hoặc files= không
            print("possible faille analyse des risques...")
            #làm sạch 
            if  self.page.endswith("/"):
                self.page=self.page[:-1]
            driver.get(self.page)
            WebDriverWait(driver, 10).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
            pageSourceBefore = driver.page_source

            for char in self.page :
                if char == "=" :
                    self.page=self.page[:self.page.index(char)+1]
                    print(self.page)
            driver.get(self.page+"../")
            WebDriverWait(driver, 10).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
            pageSourceAfter = driver.page_source
            if pageSourceBefore != pageSourceAfter:
                self.vulnFound="⚠ Possible LFI or RFI vulnerability on : " + str(self.page)
                print("LFI vuln found")
                driver.quit() 
                return
        
