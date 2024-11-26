from FTPClient import FTPBackend
from tkinter import *
from tkinter import ttk

def anonDisable(var, a, b):
    if(var.get() == 1):
        a.config(state='disabled')
        b.config(state='disabled')
        a.pack()
    else:
        a.config(state='normal')
        b.config(state='normal')
def login_window():
    login = Toplevel()
    login.transient(root)
    login.title('Login to Server')
    s_label= ttk.Label(login, text='Server: ')
    s_label.pack()
    s_entry= ttk.Entry(login)
    s_entry.pack()
    u_entry= ttk.Entry(login)
    p_entry= ttk.Entry(login)
    anon= IntVar()
    anon_check= ttk.Checkbutton(login, text='Anonymous', command=lambda:anonDisable(anon,u_entry,p_entry), variable=anon, onvalue=1, offvalue=0)
    anon_check.pack()
    u_label= ttk.Label(login, text='Username: ')
    u_label.pack()
    u_entry.pack()
    p_label = ttk.Label(login, text='Password: ')
    p_label.pack()
    p_entry.pack()
    print(anon.get())
    

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
root.config(menu=menubar)
login_window()
root.mainloop()
