import traceback
import requests
from bs4 import BeautifulSoup

class CSP_Scanner():
    def __init__(self, page, app) -> None:
        try : 
            self.page = page
            self.vulnFound = None
            self.startScan(app)
        except :
            app.webScanner.error.append("Due to a serious error the search could not be executed."+traceback.format_exc())
            return

    def getVulnFound(self):
        return self.vulnFound

    def startScan(self,app):
        try : 
            print("Start Content Security Policy scan")
            compteurSlash=0
            compteurIndex=0
            for char in self.page :
                compteurIndex+=1
                if char == "/" :
                    compteurSlash+=1
                if compteurSlash == 3 :
                    self.page = self.page[:compteurIndex-1]
                    break

            self.CSP = self.check_csp(self.page,app)
            print("CSP enabled : ", self.CSP)

            if self.CSP != True :   
                self.vulnFound = "! Content Security Policy is not enabled. " + str(self.page)
        
        except :
            app.webScanner.error.append("Error during start scan of CSP"+traceback.format_exc())
        

    def check_csp(self,url,app):
        try : 
            """
            Check if the Content Security Policy is enabled on the given URL.
            """
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            csp_header = response.headers.get('Content-Security-Policy')
            
            # kiểm tra header có chứa CSP hay không
            if csp_header:
                return True
            
            # kiểm tra trong thẻ meta có CSP hay không
            meta_tags = soup.find_all('meta', attrs={'http-equiv': 'Content-Security-Policy'})
            if len(meta_tags) > 0:
                return True
            
            # kiểm tra trong <script> và <style> 
            script_tags = soup.find_all('script')
            for script in script_tags:
                if script.has_attr('nonce') or script.has_attr('sha256'):
                    return True
            
            style_tags = soup.find_all('style')
            for style in style_tags:
                if style.has_attr('nonce') or style.has_attr('sha256'):
                    return True
            
            # Kiểm tra xem báo cáo vi phạm CSP có được gửi hay không
            report_uri = response.headers.get('Content-Security-Policy-Report-Only')
            if report_uri:
                report_response = requests.post(report_uri, data={})
                if report_response.status_code == 204:
                    return True
            
            # Kiểm tra các header chính sách bảo mật HTTP khác
            xfo_header = response.headers.get('X-Frame-Options')
            xss_header = response.headers.get('X-XSS-Protection')
            hsts_header = response.headers.get('Strict-Transport-Security')
            if xfo_header or xss_header or hsts_header:
                return True
            
            return False
        except :
            app.webScanner.error.append("Error during CSP scan"+traceback.format_exc())
            return False
