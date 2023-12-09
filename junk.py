import tkinter as tk
from tkinter import ttk, messagebox
import os
import os.path
import threading
from ttkthemes import ThemedStyle

rubbishExt = ['.tmp',
                '.bak',
                '.old',
                '.wbk',
                '.xlk',
                '_mp',
                '.gid',
                '.chk',
                '.syd',
                '.$$$',
                '.@@@',
                ".~*"]

def GetDrives():
    drives = [f"{chr(i)}:/" for i in range(65, 91) if os.path.isdir(f"{chr(i)}:/")]
    return tuple(drives)

class Window:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Junk Cleaner")
        self.root.geometry("720x512")

        # Apply a themed style
        self.style = ThemedStyle(self.root)
        self.style.set_theme("adapta")  # You can try different themes

        # Create menu.
        menu_bar = tk.Menu(self.root, font=('Arial', 13))

        system_menu = tk.Menu(menu_bar, tearoff=0, font=('Arial', 13))
        clean_menu = tk.Menu(menu_bar, tearoff=0, font=('Arial', 13))

        clean_menu.add_command(label="Scan…", command=self.MenuScanRubbish)
        """system_menu.add_separator()"""
        clean_menu.add_command(label="Clean…", command=self.MenuDelRubbish)
        menu_bar.add_cascade(label="Junk", menu=clean_menu)
        
        system_menu.add_command(label="About", command=self.MenuAbout)
    
        system_menu.add_command(label="Exit", command=self.MenuExit)
        menu_bar.add_cascade(label="Info", menu=system_menu)
        
        self.root.config(menu=menu_bar)

        # Create labels to show info
        self.progress_var = tk.StringVar()
        self.progress_var.set(' Status…')
        self.progress = ttk.Label(self.root, textvariable=self.progress_var, anchor=tk.W)
        self.progress.place(x=10, y=370, width=720, height=25)

        # Create text box to show file list
        self.flist = tk.Text(self.root, wrap="none", font=('Arial', 15))
        self.flist.place(x=10, y=10, width=720, height=350)

        # Create scroll bar for text box
        self.vscroll = ttk.Scrollbar(self.root, command=self.flist.yview)
        self.vscroll.place(x=700, y=10, height=350)
        self.flist['yscrollcommand'] = self.vscroll.set

    def MainLoop(self):
        self.root.mainloop()

    def MenuAbout(self):
        messagebox.showinfo("Junk Cleaner", "Scan and delete trash from your PC")

    def MenuExit(self):
        self.root.quit()

    def MenuScanRubbish(self):
        result = messagebox.askquestion("Junk Cleaner", "Scan now?")
        if result == 'no':
            return
        self.drives = GetDrives()
        t = threading.Thread(target=self.ScanRubbish, args=(self.drives,))
        t.start()

    def MenuDelRubbish(self):
        result = messagebox.askquestion("Junk Cleaner", "Delete all junk?")
        if result == 'no':
            return
        self.drives = GetDrives()
        t = threading.Thread(target=self.DeleteRubbish, args=(self.drives,))
        t.start()

    def ScanRubbish(self, scanpath):
        global rubbishExt
        total = 0
        filesize = 0
        for drive in scanpath:
            for root, dirs, files in os.walk(drive):
                try:
                    for fil in files:
                        filesplit = os.path.splitext(fil)
                        if filesplit[1] in rubbishExt:
                            fname = os.path.join(os.path.abspath(root), fil)
                            filesize += os.path.getsize(fname)
                            if total % 20 == 0:
                                self.flist.delete(1.0, tk.END)
                            self.flist.insert(tk.END, fname + '\n')
                            l = len(fname)
                            if l > 60:
                                self.progress_var.set(fname[:30] + '...' + fname[l-30:l])
                            else:
                                self.progress_var.set(fname)
                            total += 1
                except Exception as e:
                    print(e)
                    pass
        self.progress_var.set(f"Found {total} junk files, occupying {filesize/1024/1024:.2f} MB disk space!")

    def DeleteRubbish(self, scanpath):
        global rubbishExt
        total = 0
        filesize = 0
        for drive in scanpath:
            for root, dirs, files in os.walk(drive):
                try:
                    for fil in files:
                        filesplit = os.path.splitext(fil)
                        if filesplit[1] in rubbishExt:
                            fname = os.path.join(os.path.abspath(root), fil)
                            filesize += os.path.getsize(fname)
                            try:
                                os.remove(fname)
                                l = len(fname)
                                if l > 50:
                                    fname = fname[:25] + "..." + fname[l-25:l]
                                if total % 15 == 0:
                                    self.flist.delete(1.0, tk.END)
                                self.flist.insert(tk.END, 'Deleted ' + fname + '\n')
                                self.progress_var.set(fname)
                                total += 1
                            except:
                                pass
                except Exception as e:
                    print(e)
                    pass
        self.progress_var.set(f"Deleted {filesize/1024/1024:.2f} MB junk files = Recovered {filesize/1024/1024:.2f} MB disk space.")

if __name__ == "__main__":
    window = Window()
    window.MainLoop()
