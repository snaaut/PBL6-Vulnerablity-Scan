#!/usr/bin/env python3
# coding:utf-8
import time
import gevent
import re
import sys
import urllib
import urllib.request
import urllib.response
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import traceback
from bs4 import BeautifulSoup
#IMPORT VULN PRISE EN CHARGE :
import sql
import xss
import rfi_lfi
import wordPress
import CSP
import IDOR
import CSRF
import SSRF

start_time =0
class WebScanner:
    def __init__(self, url,avancedScan=False,browser="Firefox"):
        #khởi tạo trình quét web
        if not url.endswith("/") and not url.endswith(".php") and not url.endswith(".html"):#thêm dấu gạch chéo ở cuối
            self.url = url + "/"
        else:#nếu không thì lưu url như cũ
            self.url = url
        
        self.session = requests.Session()#tạo phiên cho trình thu thập thông tin 
        self.link_list = []
        self.analyseLink = []
        self.vulnFound=[]
        self.nbLink = 0
        self.stopped = True
        self.avancedScan =avancedScan
        self.error =set()
        
        self.scanStatus = "Waiting"
        if browser == "Firefox":
            self.user_agent ="Mozilla/5.0 (X11; Linux i686; rv:110.0) Gecko/20100101 Firefox/110.0"
        elif browser == "Chrome" : 
            self.user_agent ="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
        elif browser == "Safari" :
            self.user_agent ="Mozilla/5.0 (Macintosh; Intel Mac OS X 13_2_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15"
        elif browser == "Edge":
            self.user_agent ="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/110.0.1587.63"
    
    def getLinkList(self):
        return self.link_list

    def print_link_list(self):
        #print tous les liens
        for link in self.link_list:
            print(link)

    def forceScannerToStop(self,app):
        racine = self.url
        if self.url.endswith("/"):
            racine = self.url[:-1]
        if racine not in self.link_list:
            self.link_list.append(racine)
            app.treeLink.insert("",app.index,text=self.link_list[-1], values=self.link_list[-1])
            app.linkFoundLabel['text'] = "Links Founded : " + str(len(self.getLinkList())-1)
        self.stopped = True

    def get_page_source(self, page=None,app=None):
        #lấy mã nguồn của trang
        if page is None:
            page = self.url
        page = page.strip()
        user_agent = {"User-agent": self.user_agent}
    
        try:
                res = self.session.get(page, headers=user_agent)
        except :
            app.webScanner.error.add("Error for the page : " + page + " " + traceback.format_exc)
            return None
        return res.text

    def get_page_links(self, page=None,app=None):
        #Lấy tất cả link từ trang
        try :
            global start_time
            link_list = []  
            forbidden_pattern = r"https?://.*(trustpilot|youtube|facebook|amazon|twitter|github|google|linkedin|instagram|dailymotion|vimeo|pinterest|alibaba|tiktok|aliexpress).*"
            if page is None:
                page = self.url
            source = self.get_page_source(str(page))
            if source is not None: #nếu mã nguồn có thể truy cập được
                soup = BeautifulSoup(source, "html.parser") #trích xuất các thẻ html 
                uparse = urlparse(page)
                for link in soup.find_all("a"):#cho mỗi liên kết trên trang HTML
                    if not link.get("href") is None:#nếu không có liên kết 
                        href = link.get("href")#lấy liên kết
                        if "#" in href:  
                            href = href.split("#")[0]
                        new_link = urllib.parse.urljoin(page, href)#cho phép đính kèm url của trang với link tìm được để có link hoàn chỉnh
                        blockLink = False
                        if app.simplify.get():#nếu tùy chọn đơn giản hóa được kích hoạt thì sẽ xóa các liên kết chứa một số từ nhất định 
                            if re.search(forbidden_pattern,new_link):
                                    blockLink = True
                            if new_link.endswith(".pdf") or new_link.endswith(".js") :
                                blockLink = True
                            if new_link.endswith("/"):
                                new_link = new_link[:-1]   
                            if uparse.hostname in new_link and new_link not in link_list and not blockLink:
                                link_list.append(new_link)
                                if app.autoStop.get():
                                    start_time = time.time()
                        else :
                            link_list.append(new_link)
                            if app.autoStop.get():
                                    start_time = time.time()

                return link_list
            else:
                return []
        except :
            app.webScanner.error.add("Error when get link of a page : "+page+" "+traceback.format_exc())

    def _do_crawl(self,app):
        try:
            if app.url not in self.link_list and app.url == None:
                self.link_list.append(self.url)
                self.nbLink += 1
                app.mqueue_crawl.put(self.url)

            page_links = self.get_page_links(app.url.get(),app)
            for link in page_links:
                if self.stopped :
                    app.isScanning = False
                    app.statut['text'] = "Done !"
                    return
                if link not in self.link_list:
                    self.link_list.append(link)
                    self.nbLink += 1
                    app.treeLink.insert("",app.index,text=link, values=link)
                    app.linkFoundLabel['text'] = "Links Founded : " + str(len(self.getLinkList())-1)
                    app.root.update()
                    app.mqueue_crawl.put(link)
                    gevent.spawn(app.mqueue_crawl.put, link)
                    self._do_crawl(app)
        except KeyboardInterrupt:
            print("\nProgram terminated by the user.")
            sys.exit(1)
        except Exception as e:
            app.webScanner.error.add("Error when crawler scan the link: " +app.url.get()+" "+ str(e))

    def crawl(self, app):
        global start_time
        start_time = time.time()
        self.link_list.append(self.url)
        app.treeLink.insert("",app.index,text=self.url, values=self.url)
        try:
            if self.stopped == False:
                crawl_greenlet = gevent.spawn(self._do_crawl,app)
            else : 
                return

            while self.stopped == False:
                if app.autoStop.get():
                    elapsed_time = time.time() - start_time
                    if elapsed_time > 3:
                        break
                gevent.idle()
            app.btn_stop_click()
            return
        except :
            print("Error when crawling a page : "+traceback.format_exc())
        finally:
            app.mqueue_crawl.put("END")

    #VULNERABILITE

    def check_vuln(self,link_list, app):
        try:
            self.scanStatus = "Analyse : Initialisation... "
            app.updateStatut(self.scanStatus)
            filters = app.getFilters(returned=True)
            self.vulnFound=[]
            app.updateTreeVuln()

            for link in link_list:#tìm lỗ hổng trong từng liên kết
                champsSaisie = False 
                response = requests.get(link)
                soup = BeautifulSoup(response.text, "html.parser")
                inputs = soup.find_all("input") 
                textareas = soup.find_all("textarea")
                selects = soup.find_all("select")
                if len(inputs) > 0 or len(textareas) > 0 or len(selects) > 0:
                    champsSaisie = True
                #nếu liên kết bắt đầu bằng http:// thì đưa ra cảnh báo không an toàn
                if link.startswith("http://") :
                    self.vulnFound.append("! The site is not secure because it is in http. "+link)
                    app.updateTreeVuln()
                #XSS
                if filters[0][1] == True and champsSaisie:
                    self.scanStatus = "Analyse : XSS "
                    app.updateStatut(self.scanStatus)
                    XSSScanner=xss.XSS_Scanner(link,app)
                    trouveXSS =XSSScanner.getVulnFound()
                    if trouveXSS != None:
                        self.vulnFound.append(trouveXSS)
                    del XSSScanner
                    app.updateTreeVuln()
                #SQL
                if filters[1][1] == True and champsSaisie:
                    self.scanStatus = "Analyse : SQL "
                    app.updateStatut(self.scanStatus)
                    SQLScanner=sql.SQL_Scanner(link,app)
                    trouveSQL =SQLScanner.getVulnFound()
                    if trouveSQL != None:
                        self.vulnFound.append(trouveSQL)
                    del SQLScanner
                    app.updateTreeVuln()
                #WordPress
                if filters[2][1] == True:
                    self.scanStatus = "Analyse : WordPress "
                    app.updateStatut(self.scanStatus)
                    WordPressScanner=wordPress.WordPess_Scanner(link,app)
                    trouveWordPress =WordPressScanner.getVulnFound()
                    if trouveWordPress != None:
                        self.vulnFound.append(trouveWordPress)
                    del WordPressScanner
                    app.updateTreeVuln()
                #LFI/RFI
                if filters[3][1] == True:
                    self.scanStatus = "Analyse : LFI/RFI " 
                    app.updateStatut(self.scanStatus)
                    LFI_RFI_Scanner=rfi_lfi.LFI_RFI_Scanner(link,app)
                    trouve_LFI_RFI =LFI_RFI_Scanner.getVulnFound()
                    if trouve_LFI_RFI != None:
                        self.vulnFound.append(trouve_LFI_RFI)
                    del LFI_RFI_Scanner
                    app.updateTreeVuln()
                #CSP 
                if filters[4][1] == True:
                    self.scanStatus = "Analyse : CSP " 
                    app.updateStatut(self.scanStatus)
                    CSP_Scanner=CSP.CSP_Scanner(link,app)
                    trouve_CSP =CSP_Scanner.getVulnFound()
                    if trouve_CSP != None:
                        self.vulnFound.append(trouve_CSP)
                    del CSP_Scanner
                    app.updateTreeVuln()
                #IDOR
                if filters[5][1] == True:
                    self.scanStatus = "Analyse : IDOR "
                    app.updateStatut(self.scanStatus)
                    IDOR_Scanner=IDOR.IDOR_Scanner(link,app)
                    trouve_IDOR =IDOR_Scanner.getVulnFound()
                    if trouve_IDOR != None:
                        self.vulnFound.append(trouve_IDOR)
                    del IDOR_Scanner
                    app.updateTreeVuln()
                #CSRF
                if filters[6][1] == True:
                    self.scanStatus = "Analyse : CSRF "
                    app.updateStatut(self.scanStatus)
                    CSRF_Scanner=CSRF.CSRF_Scanner(link,app)
                    trouve_CSRF =CSRF_Scanner.getVulnFound()
                    if trouve_CSRF != None:
                        self.vulnFound.append(trouve_CSRF)
                    del CSRF_Scanner
                    app.updateTreeVuln()
                #SSRF
                if filters[7][1] == True and champsSaisie:
                    self.scanStatus = "Analyse : SSRF "
                    app.updateStatut(self.scanStatus)
                    SSRF_Scanner=SSRF.SSRF_Scanner(link,app)
                    trouve_SSRF =SSRF_Scanner.getVulnFound()
                    if trouve_SSRF != None:
                        self.vulnFound.append(trouve_SSRF)
                    del SSRF_Scanner
                    app.updateTreeVuln()
            print("Scan of vulnerability finished !")
            return
        except KeyboardInterrupt:
            print("\nProgram stopped by user.")
            sys.exit(1)
        except :
            app.webScanner.error.append("Error execution analyse : "+traceback.format_exc())
    


