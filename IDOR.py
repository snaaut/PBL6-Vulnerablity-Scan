import traceback
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, urlencode, parse_qs
import json
import re

class IDOR_Scanner():
    #Insecure Direct Object Reference vulnerabilty
    def __init__(self, page, app) -> None:
        try : 
            self.page = page
            self.vulnFound = None
            result = self.detect_idor_vulnerability(page,app)
            if result == True :
                self.vulnFound="⚠ Possible IDOR vulnerability on : " + str(self.page)
        except :
            app.webScanner.error.append("Due to a serious error the IDOR scan could not be executed."+traceback.format_exc())
            return

    def getVulnFound(self):
        return self.vulnFound

    def detect_idor_vulnerability(self,url,app):
        try:
            authorized_resources = self.get_authorized_resources(url,app)
            print(authorized_resources)
            authorized_resources.append(url)
            response = requests.get(url)
            if response.status_code != 200:
                return False

            content_type = response.headers.get('content-type', '')
            if re.search(r'text/html', content_type):
                print(1)
                soup = BeautifulSoup(response.text, 'html.parser')

                for form in soup.find_all('form'):
                    if form.get('method', '').lower() == 'get':
                        form_url = urljoin(url, form.get('action'))
                        form_params = parse_qs(form.get('action'))
                        form_params.update(parse_qs(form.get('data', '')))
                        for param_name, param_values in form_params.items():
                            for param_value in param_values:
                                print("analyse form")
                                if self.test_idor_vulnerability(url, form_url, param_name, param_value, authorized_resources):
                                    return True

                for link in soup.find_all('a'):
                    href = link.get('href')
                    if href:
                        complete_url = urljoin(url, href)
                        if complete_url not in authorized_resources:
                            print("analyse link")
                            if self.test_idor_vulnerability(url, complete_url, None, None, authorized_resources):
                                return True
            elif re.search(r'application/json', content_type):
                json_data = json.loads(response.text)
                for key in json_data.keys():
                    print("analyse json")
                    if self.test_idor_vulnerability(url, url, key, json_data[key], authorized_resources,app):
                        return True
            print("Scan IDOR finished")
            return False
        except :
            app.webScanner.error.append("IDOR scan crash : "+traceback.format_exc())

    def test_idor_vulnerability(self,original_url, test_url, param_name, param_value, authorized_resources,app):
        #kiểm tra xem url có dễ bị IDOR không
        try:
            if not param_name or re.search(r'csrf|auth', param_name, re.IGNORECASE):
                return False

            modified_url = self.modify_url_parameter(test_url, param_name, 'INJECTED')
            modified_response = requests.get(modified_url)

            if modified_response.status_code == 404 or modified_response.url.startswith(tuple(authorized_resources)):
                return False

            if param_value and param_value in modified_response.text:
                return False

            unexpected_value_url = self.modify_url_parameter(original_url, param_name, 'INJECTED',app)
            unexpected_response = requests.get(unexpected_value_url)

            if unexpected_response.status_code != 404:
                return True

            return False
        except :
            app.webScanner.error.append("IDOR scan vulnerability crash : "+traceback.format_exc())

    def modify_url_parameter(self,url, param_name, new_value,app):
        try:
            parsed_url = urlparse(url)
            query_params = parse_qs(parsed_url.query)
            query_params[param_name] = new_value
            modified_query = urlencode(query_params, doseq=True)
            modified_url = parsed_url._replace(query=modified_query).geturl()
            return modified_url
        except:
            app.webScanner.error.append("IDOR scan crash in modify url parameters : "+traceback.format_exc())

    def get_authorized_resources(self,url,app):
        #get the authorized resources
        try:
            authorized_resources = [url]
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            for link in soup.find_all(['a', 'link', 'script']):
                href = link.get('href') or link.get('src')
                if href:
                    complete_url = urljoin(url, href)
                    authorized_resources.append(complete_url)

            return authorized_resources
        except :
            app.webScanner.error.append("IDOR scan crash in get authorized resources : "+traceback.format_exc())