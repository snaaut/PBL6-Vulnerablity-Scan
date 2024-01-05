from ensurepip import version
import re
import traceback
import requests
from bs4 import BeautifulSoup

class WordPess_Scanner():
    def __init__(self, page, app) -> None:
        try : 
            self.page = page
            self.vulnFound = None
            self.WordPressVersion = None
            self.startScan(app)
        except :
            app.webScanner.error.append("Due to a serious error the Word Press scan could not be executed."+traceback.format_exc())
            return

    def getVulnFound(self):
        return self.vulnFound

    def startScan(self,app):
        try : 
            print("Start WordPress scan")
            #xóa phần sau .com của /...
            compteurSlash=0
            compteurIndex=0
            for char in self.page :
                compteurIndex+=1
                if char == "/" :
                    compteurSlash+=1
                if compteurSlash == 3 :
                    self.page = self.page[:compteurIndex-1]
                    break
            self.WordPressVersion = self.get_wordpress_version(app)
            print("WordPress version : "+str(self.WordPressVersion))
            if self.WordPressVersion != None: 
                self.vulnFound="! Don't publicly expose the version of your WordPress CMS"
                self.actualVersion = self.get_actual_wordpress_version(app)
                if self.actualVersion != "" or self.actualVersion != None :
                    if self.actualVersion != self.WordPressVersion:
                        self.vulnFound="⚠ OBSOLETE WORDPRESS VERSION. High risk of vulnerability. Version of your site: "+str(self.WordPressVersion)+" However, the current version is: ", str(self.actualVersion)
                    else :
                        print("The site has the latest version of WordPress.")
            return
        except :
            app.webScanner.error.append("WordPress scan error : "+traceback.format_exc())
        

    def get_wordpress_version(self,app):
        #tìm phiên bản wordpress
        try:
            response = requests.get(self.page)
            soup = BeautifulSoup(response.content, 'html.parser')
            meta_tags = soup.find_all('meta', attrs={'name': 'generator', 'content': True})
            for tag in meta_tags:
                version_search = re.search(r'WordPress\s([\d\.]+)', tag['content'])
                if version_search:
                    print("detect with meta")
                    return version_search.group(1)

            # Tìm chuỗi "WordPress xx.x.x" trong mã HTML
            soup_str = str(soup)
            version_search = re.search(r'WordPress\s([\d\.]+)', soup_str)
            if version_search:
                print("detect with codesource")
                return version_search.group(1)

            # Truy cập tệp readme.html
            readme_url = self.page + "/readme.html"
            response = requests.get(readme_url)
            if response.status_code == 200:
                soup_readme = BeautifulSoup(response.content, 'html.parser')
                version_search = re.search(r'Version\s([\d\.]+)', str(soup_readme))
                if version_search:
                    print("detect with readme.html")
                    return version_search.group(1)

            rss_url = self.page + "/feed/"
            response = requests.get(rss_url)
            if response.status_code == 200:
                soup_rss = BeautifulSoup(response.content, 'html.parser')
                version_tag = soup_rss.find('generator')
                if version_tag:
                    version_tag= version_tag.string.strip()
                    print("detect with RSS")
                    if "=" in version_tag:
                        for char in version_tag :#xóa tham số tệp và đường dẫn:
                            if char == "=" :
                                return version_tag[version_tag.index(char)+1:]
                    else :
                        return version_tag

            #Kiểm tra xem ReadMe.txt
            for readme_file in ['readme.txt', 'README.txt', 'Readme.txt']:
                readme_url = self.page + "/" + readme_file
                response = requests.get(readme_url)
                if response.status_code == 200:
                    readme_content = response.content.decode('utf-8')
                    version_search = re.search(r'Stable tag:\s*([\d\.]+)', readme_content)
                    if version_search:
                        print("detect with readme.txt")
                        return version_search.group(1)
            
            # Phân tích wp-includes/version.php
            version_php_url = self.page + "/wp-includes/version.php"
            response = requests.get(version_php_url)
            if response.status_code == 200:
                version_php_content = response.content.decode('utf-8')
                version_search = re.search(r'\$wp_version\s*=\s*\'([\d\.]+)\';', version_php_content)
                if version_search:
                    print("detect with version.php")
                    return version_search.group(1)
                
            # Phân tích file ngôn ngữ
            response = requests.get(self.page + "/fr_FR.po")
            if response.status_code == 200:
                po_content = response.content.decode('utf-8')
                version_search = re.search(r'msgctxt "WordPress \d\.\d.*"', po_content)
                if version_search:
                    print("detect with language")
                    return re.sub(r'^.*?([\d\.]+).*?$', r'\1', version_search.group(0))
        except:
            app.webScanner.error.append("WordPress getting version error : "+traceback.format_exc())
            return None

        # Không tìm thấy phiên bản, trả về none
        return None

    def get_actual_wordpress_version(self,app):
        #lấy phiên bản hiện tại của wordpress trên trang web chính thức
        try :
            url = "https://wordpress.org/download/"
            response = requests.get(url)
            # Tìm dòng có chứa "Download WordPress x.x"
            for line in response.text.splitlines():
                if line.startswith('<div class="wp-block-button"') and "Download WordPress" in line:
                    print(line)
                    index = line.find("Download WordPress")+len("Download WordPress")
                    #lấy phiên phản
                    version = line[index:-10]
                    print("actual wordpress version is : ", version)
                    return version
        except :
            app.webScanner.error.append("WordPress getting actual version error : "+traceback.format_exc())
            return None