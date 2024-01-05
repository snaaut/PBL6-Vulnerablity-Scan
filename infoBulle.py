from time import time
import tkinter as tk

class infoBulle(tk.Toplevel):
    def __init__(self, wdgt, msg=None, msgFunc=None, delay=0.6, follow=True, forceTop=False):
        """
        Arguments:
          wdgt: The widget this ToolTip is assigned to
          tooltip_font: Font to be used
          msg:  A static string message assigned to the ToolTip
          msgFunc: A function that retrieves a string to use as the ToolTip text
          delay:   The delay in seconds before the ToolTip appears(may be float)
          follow:  If True, the ToolTip follows motion, otherwise hides
        """
        self.wdgt = wdgt
        self.forceTop = forceTop
        self.parent = self.wdgt.master
        tk.Toplevel.__init__(self, self.parent, bg='black', padx=1, pady=1)
        self.withdraw()
        self.overrideredirect(True)
        self.compteur = 0


        self.msgVar = tk.StringVar()
        if msg is None:
            self.msgVar.set('No message provided')
        else:
            self.msgVar.set(msg)
        self.msgFunc = msgFunc
        self.delay = delay
        self.follow = follow
        self.visible = 0
        self.lastMotion = 0
        tk.Message(self, textvariable=self.msgVar, aspect=1000).grid()


        self.wdgt.bind('<Enter>', self.spawn, '+')
        self.wdgt.bind('<Leave>', self.hide, '+')
        self.wdgt.bind('<Motion>', self.move, '+')

    def spawn(self, event=None):
        self.visible = 1
        # The after function takes a time argument in milliseconds
        self.after(int(self.delay * 1000), self.show)

    def show(self):
        if self.compteur > 5 : 
            if self.forceTop :
                self.parent.attributes("-topmost", False)
            if self.visible == 1 and time() - self.lastMotion > self.delay:
                self.visible = 2
            if self.visible == 2:
                self.deiconify()
        else :
            self.compteur += 1

    def move(self, event):
        self.lastMotion = time()
        if self.follow is False:
            self.withdraw()
            self.visible = 1

        # Offset the ToolTip 10x10 pixes southwest of the pointer
        self.geometry('+%i+%i' % (event.x_root+20, event.y_root-10))
        try:
            self.msgVar.set(self.msgFunc())
        except:
            pass
        self.after(int(self.delay * 1000), self.show)

    def hide(self, event=None):
        self.compteur =0
        """
        Hides the ToolTip.  Usually this is caused by leaving the widget
        Arguments:
          event: The event that called this function
        """
        if self.forceTop :
            self.parent.attributes("-topmost", True)
        self.visible = 0
        self.withdraw()

    def update(self, msg):
        """
        Updates the Tooltip with a new message. Added by Rozen
        """
        self.msgVar.set(msg)