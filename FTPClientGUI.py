from FTPClient import *
from tkinter import *
from tkinter import ttk
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
    
def populateLocal():
    pass
def populateRemote():
    pass
def serverLogout():
    pass
root = Tk()
root.attributes('-zoomed', True)
root.title('FTP Client')
root.iconphoto(False, PhotoImage(file = 'icon.png'))
frm = ttk.Frame(root, padding = 10)
frm.grid()
menubar = Menu(root)
file = Menu(menubar, tearoff = 0)
menubar.add_cascade(label='File', menu=file)
file.add_command(label = 'Quit', command = root.destroy)
server = Menu(menubar, tearoff=0)
server.add_command(label = 'Logout', command = serverLogout())
menubar.add_cascade(label='Server', menu= server)
root.config(menu=menubar)
login_window()
remoteFiles = Listbox(root)
remoteFiles.grid(row=0, column=0, sticky='W')
localFiles = Listbox(root)
localFiles.grid(row=0, column=2, sticky='E')
recieve = ttk.Button(root, text='Download', command=lambda:ftpobject.download(remoteFiles.get(remoteFiles.curselection())))
recieve.grid(row=1, column=1, sticky='N S')
transmit = ttk.Button(root, text='Upload', command=lambda:ftpobject.upload(localFiles.get(localFiles.curselection())))
transmit.grid(row=2, column=1, sticky='N S')
populateRemote()
populateLocal()
root.mainloop()