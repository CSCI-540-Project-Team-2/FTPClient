from FTPClient import *
from tkinter import *
from tkinter import ttk
import os
#nt is windows, posix is linux/macos
if(os.name == 'nt'):
    import string
    from ctypes import windll
ftpobject = None
def anonDisable(var, a, b):
    if(var.get() == 1):
        a.config(state='disabled')
        b.config(state='disabled')
    else:
        a.config(state='normal')
        b.config(state='normal')
def errMsg(title, message):
    errorMessage = Toplevel()
    errorMessage.transient(root)
    errorMessage.title(title)
    wrongMess = ttk.Label(errorMessage, text=message)
    wrongMess.pack()
    credOk = ttk.Button(errorMessage, text='Ok', command=lambda:errorMessage.destroy())
    credOk.pack()

def attemptLogin(window, toggle, s, u, p):
    global ftpobject
    if(s.get() == ''):
        errMsg('Empty Server', 'Please enter a server address.')
        return
    if(toggle.get()==1):
        ftpobject = FTPBackend(s.get(),'Anonymous', '', True)
    elif(u.get() == '' or p.get() == ''):
        errMsg('Empty Fields', 'Please enter a username and password or select Anonymous.')
        return
    else:
        ftpobject = FTPBackend(s.get(),u.get(),p.get(), True)
    try:
        ftpobject.logon()
        #print(ftpobject.server.getresp())
        window.destroy()
    except ftplib.error_perm:
        errMsg('Permission Error', 'Incorrect credentials or server only accepts Anonymous connections.')
    except TimeoutError:
        errMsg('Timeout Error', 'Connection to the server timed out. Make sure you entered the right server and you are connected to the internet.')
        
        
def login_window():
    login = Toplevel()
    login.resizable(False, False)
    login.protocol("WM_DELETE_WINDOW", lambda:root.destroy())
    login.transient(root)
    login.title('Login to Server')
    s_label= ttk.Label(login, text='Server: ')
    s_label.pack()
    s_entry= ttk.Entry(login)
    s_entry.pack()
    u_entry= ttk.Entry(login)
    p_entry= ttk.Entry(login, show='*')
    anon= IntVar()
    anon_check= ttk.Checkbutton(login, text='Anonymous?', command=lambda:anonDisable(anon,u_entry,p_entry), variable=anon, onvalue=1, offvalue=0)
    anon_check.pack()
    u_label= ttk.Label(login, text='Username: ')
    u_label.pack()
    u_entry.pack()
    p_label = ttk.Label(login, text='Password: ')
    p_label.pack()
    p_entry.pack()
    submit = ttk.Button(login, text='Login', command =lambda:attemptLogin(login,anon,s_entry,u_entry,p_entry))
    submit.pack()
    login.grab_set()
    root.wait_window(login)
def directoryChange(location):
    if(location == 'local' and os.path.isdir(localFiles.get(localFiles.curselection()))):
        if(os.path.abspath(os.curdir) == (os.path.abspath(os.curdir)[0] + ':\\') and localFiles.get(localFiles.curselection()) == '..'):
            WinDevs()
        else:
            os.chdir(localFiles.get(localFiles.curselection()))
            populateLocal()
    elif(location == 'remote'):
        ftpobject.cd(remoteFiles.get(remoteFiles.curselection()))
        populateRemote()
def WinDevs():
    drives = []
    bitmask = windll.kernel32.GetLogicalDrives()
    print(bitmask)
    for letter in string.ascii_uppercase:
        if bitmask & 1:
            drives.append(letter)
        bitmask >>= 1
    localFiles.delete(0,END)
    for d in drives:
        localFiles.insert(END, d + ':\\')

def populateLocal():
    templist = os.listdir()
    templist.sort()
    localFiles.delete(0, END)
    if(os.path.abspath(os.curdir) != '/'):
        localFiles.insert(END, '..')
    for f in templist:
        localFiles.insert(END, f)

def populateRemote():
    templist = ftpobject.server.nlst()
    remoteFiles.delete(0,END)
    remoteFiles.insert(END, '..')
    for f in templist:
        remoteFiles.insert(END, f)

def serverLogout():
    localFiles.delete(0, END)
    remoteFiles.delete(0, END)
    global ftpobject
    ftpobject.server.quit()
    ftpobject = None
    login_window()
    
root = Tk()
if(os.name == 'posix'):
    root.attributes('-zoomed', True)
else:
    root.state('zoomed')
root.title('FTP Client')
root.iconphoto(False, PhotoImage(file = 'icon.png'))
textframe = ttk.Frame(root)
mainframe = ttk.Frame(root)
buttonframe = ttk.Frame(mainframe)
recieve = ttk.Button(buttonframe, text='Download', command=lambda:ftpobject.download(remoteFiles.get(remoteFiles.curselection())))
transmit = ttk.Button(buttonframe, text='Upload', command=lambda:ftpobject.upload(localFiles.get(localFiles.curselection())))
recieve.pack()
transmit.pack()
remoteFiles = Listbox(mainframe)
remoteScroll = ttk.Scrollbar(mainframe, orient='vertical')
remoteFiles.config(yscrollcommand=remoteScroll.set)
remoteScroll.config(command=remoteFiles.yview)
localFiles = Listbox(mainframe)
localScroll = ttk.Scrollbar(mainframe, orient='vertical')
localFiles.config(yscrollcommand=localScroll.set)
localScroll.config(command=localFiles.yview)
log = Text(textframe, height=5)
logScroll = ttk.Scrollbar(textframe, orient='vertical')
log.config(yscrollcommand=logScroll.set)
logScroll.config(command=log.yview)
#remoteFiles.grid(row=0, column=0, sticky='W')
#remoteScroll.grid(row=0, column=1)
remoteFiles.pack(side='left', expand=True, fill='both')
remoteScroll.pack(side='left', fill='y')
buttonframe.pack(side='left')
localFiles.pack(side='left',expand=True,  fill='both')
localScroll.pack(side='left', fill='y')
log.pack(side='left', expand='True', fill='both')
logScroll.pack(side='left', fill='y')
root.rowconfigure(0, weight=9)
root.rowconfigure(1, weight=1)
root.columnconfigure(0, weight=1)
mainframe.grid(row=0, column=0, sticky='nsew')
textframe.grid(row=1,column=0, sticky='nsew')
menubar = Menu(root)
file = Menu(menubar, tearoff = 0)
menubar.add_cascade(label='File', menu=file)
file.add_command(label = 'Quit', command = root.destroy)
server = Menu(menubar, tearoff=0)
server.add_command(label = 'Logout', command = lambda:serverLogout())
menubar.add_cascade(label='Server', menu= server)
root.config(menu=menubar)
login_window()
populateRemote()
os.chdir(os.path.expanduser("~"))
populateLocal()
localFiles.bind('<Double-Button-1>', lambda x:directoryChange('local'))
remoteFiles.bind('<Double-Button-1>', lambda x:directoryChange('remote'))
root.mainloop()