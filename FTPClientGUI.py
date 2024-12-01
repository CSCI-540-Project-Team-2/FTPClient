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
def down():
    filetoget = remoteFiles.get(remoteFiles.curselection())
    if (filetoget[len(filetoget)-1]== '/'):
        log('Can\'t download a directory.')
    else:
        try:
            ftpobject.download(filetoget, os.path.abspath(os.curdir) + ('/' if os.name == 'posix' else '\\'))
            log('Downloaded ' + filetoget)
            populateLocal()
        except ftplib.error_perm:
            log('Could not download the file.')

def up():
    filetoupload = localFiles.get(localFiles.curselection())
    if (filetoupload[len(filetoupload)-1]== '/'):
        log('Can\'t upload a directory.')
    else:
        try:
            ftpobject.upload(filetoupload)#os.path.abspath(os.curdir) + ('/' if os.name == 'posix' else '\\')+filetoupload)
            log('Uploaded ' + filetoupload)
            populateRemote()
        except ftplib.error_perm:
            log('Could not upload the file')

def errMsg(parent, title, message):
    errorMessage = Toplevel()
    errorMessage.transient(parent)
    errorMessage.title(title)
    wrongMess = ttk.Label(errorMessage, text=message)
    wrongMess.pack()
    credOk = ttk.Button(errorMessage, text='Ok', command=lambda:errorMessage.destroy())
    credOk.pack()
    errorMessage.grab_set()
    parent.wait_window(errorMessage)

def attemptLogin(window, toggle, s, u, p):
    global ftpobject
    if(s.get() == ''):
        errMsg(window, 'Empty Server', 'Please enter a server address.')
        return
    if(toggle.get()==1):
        ftpobject = FTPBackend(s.get(),'Anonymous', '', True)
    elif(u.get() == '' or p.get() == ''):
        errMsg(window, 'Empty Fields', 'Please enter a username and password or select Anonymous.')
        return
    else:
        ftpobject = FTPBackend(s.get(),u.get(),p.get(), True)
    try:
        ftpobject.logon()
        #print(ftpobject.server.getresp())
        window.destroy()
    except ftplib.error_perm:
        errMsg(window, 'Permission Error', 'Incorrect credentials or server only accepts Anonymous connections.')
    except TimeoutError:
        errMsg(window, 'Timeout Error', 'Connection to the server timed out. Make sure you entered the right server and you are connected to the internet.')
        
def log(text):
    logBox.config(state='normal')
    logBox.insert(END, text + '\n')
    logBox.config(state='disabled')

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
        if(remoteFiles.get(remoteFiles.curselection())=='..'):
            log('Entered previous directory')
        else: 
            log('Entered ' + remoteFiles.get(remoteFiles.curselection()))
        populateRemote()

def WinDevs():
    drives = []
    bitmask = windll.kernel32.GetLogicalDrives()
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
        if(os.path.isdir(f)):
            localFiles.insert(END, f + '/')
        else:
            localFiles.insert(END, f)

def populateRemote():
    templist = ftpobject.server.nlst()
    remoteFiles.delete(0,END)
    remoteFiles.insert(END, '..')
    isdir = []
    ftpobject.server.dir(isdir.append)
    isdir = [d[0] for d in isdir]
    for i in range(len(isdir)):
        if(isdir[i]=='d' or isdir[i] == 'l'):
            isdir[i]= '/'
        else:
            isdir[i] = ''
    for i in range(len(templist)):
        remoteFiles.insert(END, templist[i] + isdir[i])


def serverLogout():
    localFiles.delete(0, END)
    remoteFiles.delete(0, END)
    global ftpobject
    ftpobject.server.quit()
    ftpobject = None
    log('Logged out.')
    login_window()
    postLogin()

def postLogin():
    log('Successful login to ' + ftpobject.serverURL)
    if(ftpobject.secure):
        log('This connection is secured with FTPS!')
    populateRemote()
    os.chdir(os.path.expanduser("~"))
    populateLocal()

def credits():
    creditPopup = Toplevel()
    creditPopup.title('About FTPClient')
    creditPopup.resizable(False,False)
    creditPopup.transient(root)
    names = ttk.Label(creditPopup, text='Authors: Erin Rodriguez, Jerome Benoit, Ryan Brewster, James Gregg, Gabriel Herron')
    group = ttk.Label(creditPopup, text='This was a collaborative effort by Team 5.')
    classtext = ttk.Label(creditPopup, text='CSCI 540 - USC Upstate 2024')
    exitbutton = ttk.Button(creditPopup, text='Cool!', command = lambda:creditPopup.destroy())
    names.pack()
    group.pack()
    classtext.pack()
    exitbutton.pack()
    creditPopup.grab_set()
    root.wait_window(creditPopup)
   
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
recieve = ttk.Button(buttonframe, text='Download', command=lambda:down())
transmit = ttk.Button(buttonframe, text='Upload', command=lambda:up())
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
logBox = Text(textframe, height=5, state='disabled', bg='grey')
logScroll = ttk.Scrollbar(textframe, orient='vertical')
logBox.config(yscrollcommand=logScroll.set)
logScroll.config(command=logBox.yview)
remoteFiles.pack(side='left', expand=True, fill='both')
remoteScroll.pack(side='left', fill='y')
buttonframe.pack(side='left')
localFiles.pack(side='left',expand=True,  fill='both')
localScroll.pack(side='left', fill='y')
logBox.pack(side='left', expand='True', fill='both')
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
server.add_command(label ='Security Status' , command = lambda:errMsg(root, 'Security Status', 'This server is '+ ('secured' if ftpobject.secure else 'not secured') + ' with FTPS'))
menubar.add_cascade(label='Server', menu= server)
menubar.add_command(label = 'About', command=lambda:credits())
root.config(menu=menubar)
login_window()
postLogin()
localFiles.bind('<Double-Button-1>', lambda x:directoryChange('local'))
remoteFiles.bind('<Double-Button-1>', lambda x:directoryChange('remote'))
root.mainloop()