import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import sv_ttk
import multiprocessing
import re
import sys
from urllib.parse import urlparse
import webbrowser
import web_scanner
from infoBulle import infoBulle
import pyperclip
from tkinter import messagebox
import utils
import json
import login
import traceback
import logs
import driver
class App:
    #Principal class of the software Security Scan
    def __init__(self, language,isfirstStart=True):
        try :
            self.language = language
            self.isfirstStart=isfirstStart
            #create root window 
            self.root = tk.Tk()#create root
            sv_ttk.set_theme("dark")
            self.root.geometry("1250x720")
            
            #liscencing
            self.licenceRefused = False
            self.liscence =""
            if self.isfirstStart == True : 
                if self.language=="fr":
                    self.liscence = """CONTRAT UTILISATEUR DE SECURITY SCAN : \n\nAcceptation des conditions :\nEn utilisant le logiciel Security Scan (ci-après dénommé "le Logiciel"), vous acceptez d'être lié par les termes et conditions de ce Contrat Utilisateur (ci-après dénommé "le Contrat"). \nSi vous n'acceptez pas les termes de ce Contrat, vous devez cesser immédiatement toute utilisation du Logiciel.\n\nLicence d'utilisation : \nSous réserve de votre acceptation et du respect des termes de ce Contrat, le développeur du Logiciel (ci-après dénommé "le Développeur") vous accorde une licence limitée, non exclusive, pour utiliser le Logiciel à des fins légitimes de sécurité et d'administration de sites Web.\n\nRestrictions d'utilisation : \nVous vous engagez à ne pas utiliser le Logiciel à des fins illégales ou malveillantes, y compris, sans s'y limiter, l'accès non autorisé, la modification ou la destruction de données, ou la perturbation du fonctionnement normal d'un site Web.\nVous êtes seul responsable de toutes les actions entreprises en utilisant le Logiciel.\n\nAvertissement de responsabilité : \nLe Logiciel est fourni "en l'état" et "tel que disponible", sans garantie d'aucune sorte, expresse ou implicite, y compris, sans s'y limiter, les garanties de qualité marchande, d'adéquation à un usage particulier et de non-contrefaçon.\nLe Développeur ne garantit pas que le Logiciel sera exempt d'erreurs, de bugs ou d'interruptions, ni que les résultats obtenus en utilisant le Logiciel seront exacts ou fiables.\n\nLimitation de responsabilité : \nDans la mesure permise par la loi applicable, le Développeur ne pourra être tenu responsable de tout dommage direct, indirect, accessoire, spécial, exemplaire ou consécutif (y compris, sans s'y limiter, la perte de profits, de données ou d'interruption d'activité) résultant de l'utilisation ou de l'impossibilité d'utiliser le Logiciel, même si le Développeur a été informé de la possibilité de tels dommages.\n\nLicence open source : \nLe Développeur accorde une licence open source pour le code du Logiciel. Vous êtes autorisé à copier, modifier, améliorer et utiliser le Logiciel à des fins commerciales, sous réserve de votre acceptation et du respect des termes de ce Contrat.\n En utilisant le Logiciel, vous acceptez également de vous conformer à la licence open source applicable, qui régit l'utilisation, la modification et la distribution du code source du Logiciel.\n\nCollecte de données : \nLe Développeur s'engage à ne collecter aucune donnée personnelle sur les utilisateurs du Logiciel. Le Développeur s'engage à respecter les lois et réglementations applicables en matière de protection des données personnelles, y compris, sans s'y limiter, le Règlement général sur la protection des données (RGPD) et la Loi Informatique et Libertés, l'analyse du code open source permet de s'en assurer.\n\nModifications du Contrat\nLe Développeur se réserve le droit de modifier les termes de ce Contrat à tout moment et à sa seule discrétion. Il vous incombe de consulter régulièrement ce Contrat pour vous assurer que vous êtes informé des modifications apportées. Votre utilisation continue du Logiciel après la publication de modifications constitue votre acceptation de ces modifications."""
                    print("Bienvenue dans Security Scan !")
                elif self.language=="en":
                    self.liscence = """SECURITY SCAN USER AGREEMENT : \n\nAcceptance of conditions :\nBy using the Security Scan software (the "Software"), you agree to be bound by the terms and conditions of this User Agreement (the "Agreement").\nIf you do not agree with the terms of this Agreement, you must immediately cease all use of the Software.\n\nLicense to use\nSubject to your acceptance of and compliance with the terms of this Agreement, the developer of the Software (hereinafter referred to as "Developer") grants you a limited, non-exclusive license to use the Software for legitimate website security and administration purposes.\n\nRestrictions on use\nYou agree not to use the Software for any illegal or malicious purpose, including but not limited to unauthorized access, alteration or destruction of data, or disruption of the normal operation of a website.\nYou are solely responsible for all actions taken while using the Software.\n\nDisclaimer of liability\nThe Software is provided "as is" and "as available" without warranty of any kind, either express or implied, including, but not limited to, the warranties of merchantability, fitness for a particular purpose and non-infringement.\nThe Developer does not warrant that the Software will be free of errors, bugs or interruptions, or that the results obtained by using the Software will be accurate or reliable.\n\nLimitation of liability\nTo the extent permitted by applicable law, Developer shall not be liable for any direct, indirect, incidental, special, exemplary or consequential damages (including, without limitation, loss of profits, data or business interruption) arising out of the use of or inability to use the Software, even if Developer has been advised of the possibility of such damages.\n\nOpen source licence\nThe Developer grants an open source license to the code of the Software. You are permitted to copy, modify, enhance and use the Software for commercial purposes, subject to your acceptance and compliance with the terms of this Agreement.\n By using the Software, you also agree to comply with the applicable open source license, which governs the use, modification and distribution of the source code of the Software. The Developer undertakes to comply with the applicable laws and regulations regarding the protection of personal data, including, but not limited to, the General Data Protection Regulation (RGPD) and the French Data Protection Act (Loi Informatique et Libertés), as the analysis of the open source code makes it possible to ascertain.\n\nChanges to the Contract\nThe Developer reserves the right to change the terms of this Agreement at any time in its sole discretion. It is your responsibility to review this Agreement regularly to ensure that you are aware of any changes. Your continued use of the Software following the posting of changes constitutes your acceptance of those changes."""
                    print("Welcome to Security Scan !")
            self.root.geometry("1250x720")
            screen_width = self.root.winfo_screenwidth()
            screen_height =self.root.winfo_screenheight()
            x = int(((screen_width - self.root.winfo_reqwidth()) // 2)*0.40)
            y = int(((screen_height - self.root.winfo_reqheight()) // 2)*0.30)
            self.root.geometry("+{}+{}".format(x, y))
            self.root.title("Security Scan")
            imgIcon= Image.open('data/icon.ico')
            imgIcon = ImageTk.PhotoImage(imgIcon)
            self.root.wm_iconphoto(True, imgIcon)
            self.root.resizable(False, False)
            self.root.iconphoto(True, imgIcon)

            #VARIABLES :
            self.url = tk.StringVar()
            self.simplify = tk.BooleanVar(value=True)
            self.autoStop = tk.BooleanVar(value=True)
            self.avancedScan = tk.BooleanVar(value=False)
            self.webScanner=None
            self.isScanning = False
            self.statut = ""
            self.statutVuln = ""
            self.inputURL = ttk.Entry(self.root, width=50,textvariable=self.url)#creation de la zone de saisie de l'URL
            self.mqueue_crawl = multiprocessing.Queue()
            self.mqueue_check_vuln = multiprocessing.Queue()
            self.simplify = tk.BooleanVar(value=True)
            self.autoStop = tk.BooleanVar(value=True)
            self.avancedScan = tk.BooleanVar(value=False)
            self.cookiesRoot =None
            self.lienFoundLabel = ""
            self.treeError = None
            self.index=0
            #filters
            self.filtrerScan_window=None
            self.errors_window=None
            self.filters  =[["XSS",True],["SQL",True],["WordPress",True],["LFI/RFI",True],["CSP",True],["IDOR",True],["CSRF",True],["SSRF",False]]#nom/etat
            self.defaultFilters = [["XSS",True],["SQL",True],["WordPress",True],["LFI/RFI",True],["CSP",True],["IDOR",True],["CSRF",True],["SSRF",False]]
            self.filtersInfo = ["Cross Site Scripting", "SQL Injection", "WordPress version", "Local File Inclusion/Remote File Inclusion", "Content Security Policy", "Insecure Direct Object Reference", "Cross Site Request Forgery", "Server Side Request Forgery" ]
            self.settings_window=None
            #driver
            self.varBrowser="Firefox"
            self.settingsFirstStart = True
            #speed scan :
            #self.speedScanTEXT=""
            #self.speedScanVar=4
            self.firstAlertSpeedScan = True
            #error :
            self.trashPhoto=""
            #login : 
            self.username_entry=""
            self.password_entry=""
            self.url_login_entry=""


            #WIDGETS :
            # if self.language=="fr":
            #     self.startScan = ttk.Button(self.root, text="start scan", style="Accent.TButton",command=self.btn_scan_click)#creation du bouton sde démarrage du scan
            #     infoBulle(self.startScan, "Démarre la recherche de lien. ATTENTION : optenez d'abord l'autorisations de l'administrateur du site avant de scanner celui-ci.")
            #     self.stopScan = ttk.Button(self.root, text="stop scan", style="Accent.TButton",command=self.btn_stop_click)#creation du bouton sde démarrage du scan
            #     infoBulle(self.inputURL, '''URL au format http(s)://[...]''')
            #     self.linkFoundLabel=ttk.Label(self.root, text="Lien(s) trouvé(s) :")
            #     self.vulnFoundLabel=ttk.Label(self.root, text="Vulnérabilité(s) trouvé(s) :")
            #     self.statut=ttk.Label(self.root, text="Scan non démarré")
            #     self.statutVuln=ttk.Label(self.root, text="Scan de vulnérabilité non démarré")
            #     self.warningLabel = ttk.Label(self.root,text="ATTENTION : DEMANDEZ L'AUTORISATION DE L'ADMINISTRATEUR DU SITE AVANT DE LE SCANNER" )
            #     self.errors_button = ttk.Button(self.root, text="Erreurs", command=self.show_errors)
            # elif self.language=="en":
            self.startScan = ttk.Button(self.root, text="start scan", style="Accent.TButton",command=self.btn_scan_click)
            infoBulle(self.startScan, "Start the search for links. WARNING: first get the site administrator's permission before scanning it.")
            self.stopScan = ttk.Button(self.root, text="stop scan", style="Accent.TButton",command=self.btn_stop_click)
            infoBulle(self.inputURL, '''URL in http(s)://[...] format''')
            self.linkFoundLabel=ttk.Label(self.root, text="Link(s) found :")
            self.vulnFoundLabel=ttk.Label(self.root, text="Vulnerability(ies) found :")
            self.statut=ttk.Label(self.root, text="Scan not started")
            self.statutVuln=ttk.Label(self.root, text="Vulnerability scan not started")
            self.warningLabel = ttk.Label(self.root,text="WARNING : ASK THE ADMINISTRATOR OF THE SITE FOR PERMISSION BEFORE SCANNING IT" )
            self.errors_button = ttk.Button(self.root, text="Errors", command=self.show_errors)
                
            self._NotifIMG = Image.open('data/notificationAlert.png')
            self._NotifIMG2 = ImageTk.PhotoImage(self._NotifIMG)
            self.notificationAlert = ttk.Label(self.root, image=self._NotifIMG2)
            self.notificationAlertActive = False

            self._logoScanIMG = Image.open('data/logo.png')
            self._logoScanIMG = ImageTk.PhotoImage(self._logoScanIMG)
            self.logoScan=tk.Label(self.root, image=self._logoScanIMG)

            #create treeview for link :
            self.scrollbarLink = ttk.Scrollbar()
            self.scrollbarLink.pack(side="right", fill="y")
            self.treeLink = ttk.Treeview(height=11,selectmode="extended",show=("tree"),yscrollcommand=self.scrollbarLink.set,)
            infoBulle(self.inputURL, "Right click to search for vulnerabilities on the selected link(s).")
            self.scrollbarLink.config(command=self.treeLink.yview)
            self.treeLink.column("#0", anchor="w", width=140)

            self.tree_link = []
            if self.tree_link != []:
                for item in self.tree_link:
                    parent, iid, text, values = item
                    self.treeLink.insert(parent=parent, index="end", iid=iid, text=text, values=values)
                self.treeLink.selection_set(1)

            self.treeLink.bind('<Button-3>', lambda e: self.popupSelectALink(e,1))
            self.treeLink.bind('<Button-2>', lambda e: self.popupSelectALink(e,1))

            #create treeview for vulnerability :
            self.scrollbarVuln = ttk.Scrollbar()
            self.scrollbarVuln.pack(side="right", fill="y")
            self.treeVuln = ttk.Treeview(height=11,selectmode="browse",show=("tree",),yscrollcommand=self.scrollbarVuln.set)
            self.scrollbarVuln.config(command=self.treeVuln.yview)
            self.treeVuln.column("#0", anchor="w", width=140)

            self.tree_Vuln = []
            if self.tree_Vuln != []:
                for item in self.tree_Vuln:
                    parent, id, text, values = item
                    self.treeVuln.insert(parent=parent, index="end", id=id, text=text, values=values)
                self.treeLink.selection_set(1)


            #create setting button : 
            self.imageSettingsButton = Image.open("data/settings.png")
            self.imageSettingsButton2 = ImageTk.PhotoImage(self.imageSettingsButton)
            self.settings_button = ttk.Button(self.root, image=self.imageSettingsButton2, command=self.show_settings)

            self.imageSettingsButton = Image.open('data/settings.png')
            self.imageSettingsButton = ImageTk.PhotoImage(self.imageSettingsButton)
            self.settings_button=ttk.Button(self.root, image=self.imageSettingsButton, command=self.show_settings)

            #placement widgets :
            self.startScan.place(x=840, y=20, width=150, height=50)
            self.stopScan.place(x=1000, y=20, width=150, height=50)
            self.inputURL.place(x=180, y=20, width=650, height=50)
            self.logoScan.place(x=20, y=-20)
            self.settings_button.place(x=1165, y=23)

            self.linkFoundLabel.place(x=85, y=115)
            self.vulnFoundLabel.place(x=85, y=515)

            self.errors_button.place(x=1115, y=685)

            self.statut.place(x=860, y=70)
            self.statutVuln.place(x=900, y=515)

            self.warningLabel.place(x=300,y=695)

            self.treeLink.place(relx=0.071, rely=0.20, relheight=0.5, relwidth=0.853)
            self.scrollbarLink.place(relx=0.924, rely=0.20, relheight=0.5, relwidth=0.026)
            self.treeVuln.place(relx=0.071, rely=0.75, relheight=0.2, relwidth=0.853)
            self.scrollbarVuln.place(relx=0.924, rely=0.75, relheight=0.2, relwidth=0.026)

            self.root.protocol("WM_DELETE_WINDOW", self.quit)
            self.loadSave()
            if self.isfirstStart == True :
                self.root.withdraw()
                self.licencing()
            if self.root != None:
                self.root.mainloop()
        except :
            print("Critical error, the software will stop.", traceback.format_exc())

    def quit(self):
        try :
            if self.webScanner != None:
                logs.updateLog(self.webScanner.error)
            data = {
                "url": self.url.get() if self.url.get() else "",
                "browser": self.varBrowser.get() if self.varBrowser.get() else "Firefox",
                "filters": self.getFilters(True),
                "speed": self.speedScanVar if isinstance(self.speedScanVar, int) else self.speedScanVar.get(),
                "firstStart": self.isfirstStart
            }
            with open("caches/save.json", "w+") as fichier:
                json.dump(data, fichier)
            fichier.close()
            self.root.destroy()
            self.root = None
        except :
            if self.language == "fr":
                print("Suite a une grave erreur de sauvegarde des paramètres, le logiciel va s'arrêter de façon prématurer",traceback.format_exc())
                self.root.destroy()
                
            elif self.language == "en":
                print("Due to a serious error in saving the settings, the software will stop prematurely",traceback.format_exc())
                self.root.destroy()
        return

    def loadSave(self):
        try:
            valueBrowser = self.varBrowser
            self.varBrowser = tk.StringVar()
            self.varBrowser.set(valueBrowser)
            with open("caches/save.json", "r") as fichier:
                try :
                    data = json.load(fichier)
                except :
                    data = None
                if not data or data == None:
                    return
                self.url.set(data["url"])
                self.varBrowser.set(data["browser"])
                for i, filter in enumerate(data["filters"]):
                    if i >= len(self.filters):
                        break
                    self.filters[i][1] = utils.convertToBool(filter[1])
                self.speedScanVar = int(data["speed"]) if isinstance(data["speed"], int) else tk.IntVar(value=data["speed"])
            fichier.close()
        except Exception as e:
            if self.language == "fr":
                print("Erreur lors de la lecture du fichier de sauvegarde :", e)
            elif self.language == "en":
                print("Error reading the save file :", e)
        return
    
    def renit(self):
        self.settings_window.attributes("-topmost", False)
        if self.language == "fr":
            validation =messagebox.askokcancel("Attention : ","La rénitialisation rétablira les réglages par défaut de Security Scan. Cette action est irréversible ! Voulez-vous vraiment continuer ?")
        elif self.language == "en":
            validation =messagebox.askokcancel("Warning : ","The reset will restore the default settings of Security Scan. This action is irreversible! Do you really want to continue?")
        self.settings_window.attributes("-topmost", True)
        try : 
            if validation : 
                data = {
                "url": "",
                "browser":"Firefox",
                "filters": self.defaultFilters,
                "speed": 3,
                "firstStart": True 
                }
                with open("caches/save.json", "w+") as fichier:
                    json.dump(data, fichier)
                fichier.close()
                self.on_closingError()
                self.on_closingSettings()#verifier si ca marche vraiment
                self.root.destroy()
        except :
            print("Error when resetting the settings", traceback.format_exc())
        return
    
    def btn_scan_click(self):
        try :
 
            target = self.url.get()
            target =target.replace(" ", "")
            regex = re.compile(
                r'^(?:http|ftp)s?://'  
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domaine...
                r'localhost|' 
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  
                r'(?::\d+)?'  # port optionnel
                r'(?:/?|[/?]\S+)$', re.IGNORECASE)

            if not re.match(regex, target):
                self.inputURL.state(["invalid"])
                messagebox.showerror("URL error", "The URL entered is not valid !")
                return
            print(self.varBrowser.get())
            if self.webScanner is None:
                self.webScanner = web_scanner.WebScanner(target,avancedScan=self.avancedScan,browser=self.varBrowser.get())

            elif urlparse(self.webScanner.url).netloc not in target: 
                self.webScanner.stopped = True
                self.webScanner = web_scanner.WebScanner(target,avancedScan=self.avancedScan,browser=self.varBrowser.get())

            if self.isScanning:
                rep = messagebox.askquestion("Scan in progress", "A scan is already in progress, do you want to overwrite it ?")
                if rep == "yes":
                    self.webScanner.stopped = True

                    self.statut['text'] = "Scan stopped !"
                    self.switchNotification() 
                    self.isScanning = False
                    sys.stdout.flush()#vide le tampon mémoire
                    return self.btn_scan_click()
                else : 
                    return
            self.webScanner.stopped = False
            self.webScanner.link_list=[]
            for child in self.treeLink.get_children():
                self.treeLink.delete(child)
            self.linkFoundLabel['text'] = "Links found : " + str(len(self.webScanner.getLinkList())-1)
            self.statut['text'] = "Scan in progress..."
            self.inputURL.state(["!invalid"])
            self.isScanning = True
            self.webScanner.crawl(self)
            self.root.after(1000,self.process_queue_crawl)
        except :
            print(traceback.format_exc()) 
            logs.updateLog([traceback.format_exc()])
    
    def btn_stop_click(self):
        try :
            #stop the crawler
            if self.webScanner != None and self.webScanner.stopped == False :
                print("Scan finished")
                self.webScanner.forceScannerToStop(self)
                self.statut['text'] = "Done !"
                self.linkFoundLabel['text'] = "Link found : " + str(len(self.webScanner.getLinkList())-1)
                self.isScanning = False
        except :
            print(traceback.format_exc()) 
            logs.updateLog([traceback.format_exc()])
    def process_queue_crawl(self):
        try:
            try :
                link = self.mqueue_crawl.get(0)
            except :
                return
            if link == "END":
                self.statut["text"] = "Scan done !"
                self.linkFoundLabel['text'] = "Link found : " + str(len(self.webScanner.getLinkList())-1)
                self.isScanning = False
                self.webScanner.stopped = True
            else:
                self.root.after(1000,self.process_queue_crawl)#relance la fonction après 1 seconde
        except :
            self.webScanner.error.append("Critical multithreading error unable to start analysis due to problem in process_queue_crawl :"+traceback.format_exc())

    def updateStatut(self, scanStatut):
        try :
            #update the statut label of the vulnerability scan 
            self.statutVuln['text'] =str(scanStatut)
            self.switchNotification() 
            self.root.update()
        except :
            print(traceback.format_exc()) 
            logs.updateLog([traceback.format_exc()])

    def btn_check_vuln(self):
        try :
            self.webScanner.error =[]
            selectedItem = self.treeLink.selection()
            selectedLinks = []
            try: 
                for i in range(len(self.filters)):
                    self.filters[i][1]=self.filters[i][0].get()
            except:
                pass
            for item in selectedItem:
                selectedLinks.append(self.treeLink.item(item)['text'])
            self.statutVuln['text'] = "Vulnerability search in progress..."
            self.webScanner.check_vuln(link_list=selectedLinks,app=self)
            self.statutVuln['text'] = "Vulnerability search done !"
        except :
            print(traceback.format_exc()) 
            logs.updateLog([traceback.format_exc()])

    def process_queue_check_vuln(self):
        try:
            self.index=0
            link = self.mqueue_check_vuln.get(0)
            while link != "END":
                self.treeVuln.insert("",self.index,text=link, values=link)#parent, index, id, text, values
                self.root.update()
                link = self.mqueue_check_vuln.get(0)#recupere le prochain lien de la queue
                self.index+=1
                if self.index>=len(self.webScanner.analyseLink):
                    print("All links have been browsed stop scanning")
                    self.mqueue_check_vuln.put("END")
            if link == "END":
                self.statutVuln["text"] = "Vulnerability check finished"
                self.isScanning = False
                self.webScanner.stopped = True
        except :
            self.root.after(self.process_queue_check_vuln)

    def updateTreeVuln(self):
        for child in self.treeVuln.get_children():
            self.treeVuln.delete(child)
        index=len(self.treeVuln.get_children())
        for vuln in self.webScanner.vulnFound:
            if vuln and vuln != "-values":
                self.treeVuln.insert(parent="", index=index, id=index, text=vuln, values=vuln)
                index+=1

    def updateVulnStatut(self,scanStatut):
        try :
            self.statutVuln['text'] =str(scanStatut)
            self.root.update()
        except :
            print(traceback.format_exc()) 
            logs.updateLog([traceback.format_exc()])
        
    def copyLink(self):
        try :
            selectedItem = self.treeLink.selection()
            selectedLinks = ""
            for item in selectedItem:
                selectedLinks+=" "+ str(self.treeLink.item(item)['text'])
            pyperclip.copy(str(selectedLinks))
            print("Copied link : "+selectedLinks)
        except :
            print(traceback.format_exc()) 
            logs.updateLog([traceback.format_exc()])
        
    def copyError(self):
        try : 
            selectedItem = self.treeError.selection()
            selectedErrors = ""
            for item in selectedItem:
                selectedErrors+=" "+ str(self.treeError.item(item)['text'])
            pyperclip.copy(str(selectedErrors))
            print("Error copied : "+selectedErrors)
        except :
            print(traceback.format_exc()) 
            logs.updateLog([traceback.format_exc()])
    
    def copyVuln(self):
        try : 
            #copy the vulnerability to the clipboard
            selectedItem = self.treeVuln.selection()#verifier treeError defini sur None dans le init
            selectedVuln = ""
            for item in selectedItem:
                selectedVuln+=" "+ str(self.treeVuln.item(item)['text'])
            pyperclip.copy(str(selectedVuln))
            print("Error copied : "+selectedVuln)
        except :
            print(traceback.format_exc()) 
            logs.updateLog([traceback.format_exc()])


    def popupSelectALink(self,event, *args, **kwargs):
        Popupmenu = tk.Menu(self.root, tearoff=0)
        Popupmenu.configure(activebackground="black")
        Popupmenu.add_command(command=self.btn_check_vuln,label="Search for vulnerabilities")
        Popupmenu.add_command(command=self.copyLink,label="Copy")
        Popupmenu.post(event.x_root, event.y_root)


    def popupSelectAVuln(self,event, *args, **kwargs):
        try : 
            Popupmenu = tk.Menu(self.root, tearoff=0)
            Popupmenu.configure(activebackground="black")
            Popupmenu.add_command(command=self.copyVuln,label="Copy")
            Popupmenu.post(event.x_root, event.y_root)
        except :
            print(traceback.format_exc())
            logs.updateLog([traceback.format_exc()])
    
    def popupErrorTree(self,event, *args, **kwargs):
        try :
            Popupmenu = tk.Menu(self.root, tearoff=0)
            Popupmenu.configure(activebackground="black")
            if self.language == "fr":
                Popupmenu.add_command(command=self.copyError,label="Copier")
            elif self.language == "en":
                Popupmenu.add_command(command=self.copyError,label="Copy")
            Popupmenu.post(event.x_root, event.y_root) 
        except :
            print(traceback.format_exc()) 
            logs.updateLog([traceback.format_exc()])

    def show_errors(self):
        try : 
            if self.errors_window :
                self.errors_window.lift()
            else :
                self.errors_window = tk.Toplevel()
                self.errors_window.title("Errors")
                self.errors_window.geometry("500x300")
                imgIcon= Image.open('data/icon.ico')
                imgIcon = ImageTk.PhotoImage(imgIcon)
                self.errors_window.wm_iconphoto(False, imgIcon)

                trashIMG = Image.open('data/trash.png')
                self.trashPhoto = ImageTk.PhotoImage(trashIMG)
                self.trashButton=ttk.Button(self.errors_window, image=self.trashPhoto, command=self.deleteError)
                self.treeError = ttk.Treeview(self.errors_window,height=10,selectmode="browse",show=("tree",))
                self.treeError.column("#0", anchor="w", width=160)
                if self.webScanner !=None:
                    if self.webScanner.error !=[]:
                        self.tree_Error =self.webScanner.error
                    else : 
                        self.tree_Error = ["Nothing to report for the moment..."]
                else :
                    self.tree_Error = ["Nothing to report for the moment..."]
                if self.tree_Error != []:
                    if len(self.tree_Error) > 10:
                        while len(self.tree_Error) > 10:
                            self.tree_Error.pop(0)
                    if (len(self.tree_Error) >=2 and "Rien a signaler pour le moment..." in self.tree_Error) or (len(self.tree_Error) >=2 and "Nothing to report for the moment..." in self.tree_Error):
                        self.tree_Error.pop(0)
                    index=1
                    for error in self.tree_Error:
                        self.treeError.insert(parent="", index=index, id=index, text=error)
                        index+=1
                        self.treeError.selection_set(1)
                self.treeError.place(relx=0.037, rely=0.10, relheight=0.855, relwidth=0.93)
                self.trashButton.place(relx=0, rely=0)

                self.treeError.bind('<Button-2>', lambda e: self.popupErrorTree(e,1))
                self.treeError.bind('<Button-3>', lambda e: self.popupErrorTree(e,1))
                self.errors_window.protocol("WM_DELETE_WINDOW", self.on_closingError)
        except :
            print(traceback.format_exc())
            logs.updateLog([traceback.format_exc()])

    def deleteError(self):
        try : 
            #delete the first error in the error tree
            self.treeError.delete(self.treeError.get_children()[0])
            if self.webScanner !=None and self.webScanner.error !=[]:
                self.webScanner.error.pop(0)
            if self.treeError.get_children() == ():
                self.treeError.insert(parent="", index=1, id=1, text="Nothing to report for the moment...")
            self.switchNotification()
        except : 
            print(traceback.format_exc())
            logs.updateLog([traceback.format_exc()])
    
    def on_closingError(self):
        try : 
            #close the error window
            if self.errors_window != None:
                self.errors_window.destroy()
                self.errors_window = None
        except : 
            print(traceback.format_exc())
            logs.updateLog([traceback.format_exc()])
    
    def switchNotification(self):
        try : 
            #switch notification error to on/off
            if self.webScanner != None:
                if len(self.webScanner.error) !=0 :
                    self.notificationAlertActive = True
                    self.notificationAlert.place(x=1170, y=685)
                    return
            self.notificationAlertActive =False
            self.notificationAlert.place_forget()
        except : 
            print(traceback.format_exc())
            logs.updateLog([traceback.format_exc()])
    
    #SETTINGS WINDOW : 

    def show_settings(self):
        try : 
            #show the settings window
            if self.settings_window :
                self.settings_window.lift()
            else :
                self.settings_window = tk.Toplevel()
                self.settings_window.title("Settings")
                self.settings_window.geometry("475x720")
                screen_width = self.settings_window.winfo_screenwidth()
                screen_height =self.settings_window.winfo_screenheight()
                x = int(((screen_width - self.settings_window.winfo_reqwidth()) // 2)*0.85)
                y = int(((screen_height - self.settings_window.winfo_reqheight()) // 2)*0.30)
                self.settings_window.geometry("+{}+{}".format(x, y))
                imgIcon= Image.open('data/icon.ico')
                imgIcon = ImageTk.PhotoImage(imgIcon)
                self.settings_window.attributes("-topmost", True)


                crawlerTEXT=ttk.Label(self.settings_window,text="Crawler :")
                simplifyCrawl = ttk.Checkbutton(self.settings_window, text="Only analyze useful links", variable=self.simplify, command=self.updateSimplifyScan)
                autoStopButton = ttk.Checkbutton(self.settings_window, text="Stop when the delay is exceeded.", variable=self.autoStop, command=self.updateAutoStop)
                scanTEXT=ttk.Label(self.settings_window,text="Scan :")
                avancedScanButton = ttk.Checkbutton(self.settings_window, text="Advanced scan (not available )", variable=self.avancedScan, command=self.updateAvancedScan)
                browserSetingsTEXT = ttk.Label(self.settings_window,text="Browser : FireFox")
                infoBulle(simplifyCrawl, '''In order to reduce the scan time, Security Scan avoids scanning unnecessary links (youtube, twitter, google, etc.). If you think Security Scan should scan them or scan more links you can disable this option.''')
                infoBulle(autoStopButton, """The scan will automatically stop after a few seconds if no links have been found. Disable it to scan an extremely slow site.""")

                
                #filters :
                filtersCheckButton=[]
                for i in range(len(self.filters)):
                    if self.settingsFirstStart:
                        value = self.filters[i][1]
                        self.filters[i][1] = tk.BooleanVar(value=value)
                        self.filters[i][1].set(value)
                    filtersCheckButton.append(ttk.Checkbutton(self.settings_window, text=self.filters[i][0], variable=self.filters[i][1], command=self.getFilters))
                    infoBulle(filtersCheckButton[i], self.filtersInfo[i], forceTop=True)

                if type(self.speedScanVar) == int:
                    self.speedScanVar = tk.IntVar(value=self.speedScanVar)
                if self.language == "fr":
                    self.speedScanTEXT = ttk.Label(self.settings_window,text="Vitesse : "+str(self.speedScanVar.get()))
                    infoBulle(self.speedScanTEXT, '''Augmentez le nombre de lien testé simultanément = plus de vitesse. Attention consomme plus de ressources.''')
                elif self.language == "en":
                    self.speedScanTEXT = ttk.Label(self.settings_window,text="Speed : "+str(self.speedScanVar.get()))
                    infoBulle(self.speedScanTEXT, '''Increase the number of links tested simultaneously = more speed. Warning consumes more resources.''')

                
                applyButton = ttk.Button(self.settings_window,text="Apply",command=self.on_closingSettings)


                crawlerTEXT.place(x=20,y=20)
                simplifyCrawl.place(x=40, y=40)
                autoStopButton.place(x=40, y=70)

                scanTEXT.place(x=20,y=150)

                for i in range (len(self.filters)):
                    filtersCheckButton[i].place(x=40,y=200+(i*30))

                applyButton.place(x=380,y=680)



                self.settings_window.wm_iconphoto(False, imgIcon)
                self.settingsFirstStart = False
                self.settings_window.protocol("WM_DELETE_WINDOW", self.on_closingSettings)
        except : 
                print(traceback.format_exc())
                logs.updateLog([traceback.format_exc()])


    def on_closingSettings(self):
        try : 
            self.settings_window.grab_release()
            if self.settings_window != "":
                self.settings_window.destroy()
                self.settings_window = None
        except :
            print(traceback.format_exc()) 
            logs.updateLog([traceback.format_exc()])
        
    def getFilters(self,returned=False):
        try : 
            newliste = []
            for i in range(len(self.filters)):
                newliste.append([self.filters[i][0],self.filters[i][1].get()])
            if returned:
                return newliste
        except:
            return self.filters
        
    def updateSimplifyScan(self):
        try :
            if self.simplify.get():
                self.simplify.set(True)
            else:
                self.simplify.set(False)
        except :
            print(traceback.format_exc()) 
            logs.updateLog([traceback.format_exc()])

    def updateAutoStop(self):
        try : 
            if self.autoStop.get():
                self.autoStop.set(True)
            else:
                self.settings_window.attributes("-topmost", False)
                messagebox.showwarning("Warning : ", "It is not recommended to disable this option. If the delay is exceeded, the scan will stop automatically. If you disable this option, the scan can last a very long time or not stop at all.")
                self.autoStop.set(False)
                self.settings_window.attributes("-topmost", True)
        except :
            print(traceback.format_exc()) 
            logs.updateLog([traceback.format_exc()])

    def updateAvancedScan(self):
        self.settings_window.attributes("-topmost", False)
        messagebox.showinfo("Warning : ", "Advanced analysis is long and is only recommended if you need a high scan accuracy. Advanced analysis is not available for all vulnerabilities (see readme). A normal scan will be performed in these cases.")
        if self.avancedScan.get():
            self.avancedScan.set(True)
        else:
           self.avancedScan.set(False)
        self.settings_window.attributes("-topmost", True)
    
    def restart_alert(self):
        try : 
            self.settings_window.attributes("-topmost", False)
            messagebox.showinfo("A restart is required : ","To apply the modifications Security Scan will now turn off, we invite you to restart it later.")
            self.on_closingError()
            self.on_closingSettings()
            self.quit()
        except :
            print(traceback.format_exc()) 
            logs.updateLog([traceback.format_exc()])
    
    def getSpeedScan(self):
        try :
            if type(self.speedScanVar) != int:
                return self.speedScanVar.get()
            else:
                return self.speedScanVar
        except :
            print(traceback.format_exc()) 
            logs.updateLog([traceback.format_exc()])
    def updateSpeedScan(self,event):
        try :
            self.speedScanTEXT.config(text="Vitesse :"+str(self.speedScanVar.get()))
            if self.firstAlertSpeedScan:
                if self.speedScanVar.get() >= 10:
                    self.settings_window.attributes("-topmost", False)
                    self.firstAlertSpeedScan = False
                    messagebox.showwarning("Warning : ", "Beyond 10, the scan speed although higher can cause very high performance problems or extreme. We advise you not to exceed 10 unless your hardware allows you to. You may also be blocked because you will send too many simultaneous requests. Finally, it is possible depending on the type of scan that the increase in scan speed is not significant or does not imply a speed gain.")
                    self.settings_window.attributes("-topmost", True)
        except :
            print(traceback.format_exc()) 
            logs.updateLog([traceback.format_exc()])


    def loginDriver(driver, url):
        try :
            #connexion au site web si besoin pour le scanner
            driver.get(url)
            #a compléter manque sureant l'enregistrement du cookie 
            return  driver
        except :
            print(traceback.format_exc()) 
            logs.updateLog([traceback.format_exc()])

    def licencing(self):
        #create a window with the user agreement at first launch of Security Scan
        try :
            self.liscenceWindow = tk.Toplevel()
            if self.language == "fr" :
                self.liscenceWindow.title("CONTRAT UTILISATEUR DE SECURITY SCAN")
            else :
                self.liscenceWindow.title("SECURITY SCAN USER AGREEMENT")

            self.liscenceWindow.resizable(False, False)
            scrollbar = ttk.Scrollbar(self.liscenceWindow)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            text_box = tk.Text(self.liscenceWindow, yscrollcommand=scrollbar.set, width=150, height=30)
            text_box.insert(tk.END, self.liscence)
            text_box.config(state=tk.DISABLED)
            text_box.pack()
            scrollbar.config(command=text_box.yview)
            if self.language == "fr" :
                accept_button =ttk.Button(self.liscenceWindow, text="Accepter", width=10, command=self.acceptLiscence, style="Accent.TButton") 
                refuse_button = ttk.Button(self.liscenceWindow, text="Refuser", width=10, command=self.refuseLiscence)
            else :
                accept_button = ttk.Button(self.liscenceWindow, text="Accept", width=10, command=self.acceptLiscence, style="Accent.TButton") 
                refuse_button = ttk.Button(self.liscenceWindow, text="Refuse", width=10, command=self.refuseLiscence)

            refuse_button.pack(side=tk.RIGHT, padx=10, pady=10)
            accept_button.pack(side=tk.LEFT, padx=10, pady=10)

            screen_width = self.liscenceWindow.winfo_screenwidth()
            screen_height = self.liscenceWindow.winfo_screenheight()
            x = int(((screen_width - self.liscenceWindow.winfo_reqwidth()) // 2)*0.50)
            y = int(((screen_height - self.liscenceWindow.winfo_reqheight()) // 2)*0.60)
            self.liscenceWindow.geometry("+{}+{}".format(x, y))
            self.liscenceWindow.mainloop()
        except :
            self.liscenceWindow.destroy()
            exit("error in according licence"+traceback.format_exc())   

    def refuseLiscence(self):
        self.licenceRefused = True
        self.isfirstStart = True
        self.quit()
        exit("You have refused the licence.")


    def acceptLiscence(self):
        #accept the licence 
        try :
            self.liscenceWindow.destroy()
            self.isfirstStart = False
            self.liscenceWindow = None
            self.licenceRefused = False
            self.welcomeWindow = tk.Toplevel()
            imgIcon= Image.open('data/icon.ico')
            imgIcon = ImageTk.PhotoImage(imgIcon)
            self.root.wm_iconphoto(True, imgIcon)
            self.welcomeWindow.wm_iconphoto(True, imgIcon)
            self.welcomeWindow.iconphoto(True, imgIcon)
            
            if self.language == "fr" :
                self.welcomeWindow.title("Bienvenue dans Security Scan")
            else :
                self.welcomeWindow.title("Welcome to Security Scan")
            self.welcomeWindow.geometry("1000x556")

            # Charger l'image
            imgIcon = Image.open('data/welcome.jpeg')
            imgIcon2 = ImageTk.PhotoImage(imgIcon)
            label = tk.Label(self.welcomeWindow, image=imgIcon2)
            label.pack()

            # Centrer la fenêtre
            self.welcomeWindow.overrideredirect(True)
            screen_width = self.welcomeWindow.winfo_screenwidth()
            screen_height = self.welcomeWindow.winfo_screenheight()
            x = int(((screen_width - self.welcomeWindow.winfo_reqwidth())/2)*0.50)
            y = int(((screen_height - self.welcomeWindow.winfo_reqheight())/2)*0.60)
            self.welcomeWindow.geometry("+{}+{}".format(x, y))
            self.welcomeWindow.after(2000, self.closeWelcomWindow)
            self.welcomeWindow.mainloop()
            print("licence accepted")
            return
        except :
            print("error in starting : ", traceback.format_exc())

    def closeWelcomWindow(self):
        self.welcomeWindow.destroy()
        self.welcomeWindow = None
        self.root.deiconify()