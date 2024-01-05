import requests
import traceback
from bs4 import BeautifulSoup
import re

class CSRF_Scanner():
    def __init__(self, page, app) -> None:
        try : 
            print("CSRF detection starting")
            self.page = page
            self.vulnFound = None
            self.SENSITIVE_HTTP_METHODS = ['POST', 'PUT', 'DELETE']
            self.CSRF_TOKEN_NAME_PATTERN = re.compile(r'^(csrf|_token|csrfmiddleware|authenticity)_token$', re.IGNORECASE)
            self.HEADERSAGENT = {'User-Agent':"Mozilla/5.0 (X11; Linux i686; rv:110.0) Gecko/20100101 Firefox/110.0"}
            self.startScan(app)

        except :
            app.webScanner.error.append("Due to a serious error the search could not be executed."+traceback.format_exc())
            return

    def getVulnFound(self):
        #trẻ về danh sách lỗ hổng
        return self.vulnFound

    def startScan(self,app):
        vulnerable_forms = self.detect_csrf_vulnerability(app)
        print("vuln form :", vulnerable_forms)
        if vulnerable_forms != []:
            self.vulnFound="⚠ Possible CSRF vulnerability on : " + str(self.page)

    def detect_csrf_vulnerability(self,app):
        #phát hiện url có thể bị tấn công csrf
        #Đầu tiên sẽ tìm các form có phương thức POST, GET, DELETE
        #Sau đó sẽ kiểm tra trong các form đó có các csrf token hợp lệ hay không
        #Nếu không có thì form đó dễ bị tấn công CSRF
        url = self.page
        try:
            with requests.Session() as session:
                session.headers.update(self.HEADERSAGENT)
                response = session.get(url)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    forms = soup.find_all('form')
                    csrf_vulnerable_forms = []
                    for form in forms:
                        print(len(forms))
                        try : 
                            if form.attrs['method'].upper() in self.SENSITIVE_HTTP_METHODS:
                                print("try")
                                if not self.is_csrf_token_present_and_valid(session, form, url):
                                    print("detection")
                                    csrf_vulnerable_forms.append(form)
                        except:
                            pass
                    print("CSRF ending scan")
                    return csrf_vulnerable_forms
                else:
                    print(f"Error retrieving page {url}.")
        except :
            app.webScanner.error.append("Error in CSRF detection of : "+url+"."+traceback.format_exc())

    def is_csrf_token_present_and_valid(self,session, form, url, app):
        #kiểm tra xem mã thông báo CSRF có hiện diện và hợp lệ không
        try : 
            csrf_token_present = False
            csrf_token_valid = False
            print(1, form.find_all('input'))
            # Tìm token CSRF trong Input
            
            for input in form.find_all('input'):
                print(1.1)
                if input.get('type') == 'hidden' and input.get('name'):
                    print(1.2)
                    if self.CSRF_TOKEN_NAME_PATTERN.match(input['name']):
                        print(1.3)
                        csrf_token_present = True
                        csrf_token_value = input['value']
                        print(1.4)
                        break
            # Tìm token csrf trong các phần tử meta
            meta_tags = form.find_all('meta')
            for meta_tag in meta_tags:
                if 'name' in meta_tag.attrs and 'content' in meta_tag.attrs:
                    if self.CSRF_TOKEN_NAME_PATTERN.match(meta_tag['name']):
                        csrf_token_present = True
                        csrf_token_value = meta_tag['content']
                        break
            print(2)
            # Tìm token CSRF trong thuộc tính data-*
            data_attrs = form.find_all(attrs={"data-*": self.CSRF_TOKEN_NAME_PATTERN})
            for data_attr in data_attrs:
                csrf_token_present = True
                csrf_token_value = data_attr['data-*']
                break

            if csrf_token_present:
                headers = {'Referer': url}
                data = {input['name']: csrf_token_value}
                response = session.post(url, headers=headers, data=data)
                if response.status_code == 200:
                    csrf_token_valid = True
            print("present",csrf_token_present, "valid",csrf_token_valid)
            return csrf_token_present and csrf_token_valid
        except :
            print("aie") 
            app.webScanner.error.append("Error during getting page on CSRF scan"+url+traceback.format_exc())