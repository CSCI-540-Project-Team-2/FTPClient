import ftplib
class FTPBackend:
    GUILaunch = False
    def __init__(self, server, user, passwd, isGUI):
        self.serverURL = server
        self.user = user
        self.passwd = passwd
        self.GUILaunch = isGUI
        self.secure = False

    def upload(self, fileName):
        # filename to upload
        if(fileName != ''):
            try:
                with open(fileName, 'rb') as file:
                    self.server.storbinary(f'STOR {fileName}', file)
                    return
            except ValueError:
                print('still dunno')
                return
        filename = input('Enter filename to upload: ')
        try:
            with open(filename, 'rb') as file:
                self.server.storbinary('STOR {filename}', file)
        except ValueError:
            print('ERROR: Could not upload file!')
            self.server.quit()


    def view(self):
        # view contents of server
        self.server.dir()

    def download(self, fileName, location):
        # filename to retrieve
        if(fileName != ''):
            try:
                destination = location + fileName
                with open(destination, 'wb') as file:
                    self.server.retrbinary(f'RETR {fileName}', file.write)
                    return
            except ValueError:
                return
        filename = input('Enter filename to download: ')
        try:
            with open(filename, 'wb') as file:
                self.server.retrbinary(f'RETR {filename}', file.write)
        except ValueError:
            print('ERROR: Could not download file!')
            self.server.quit()
        else:
            print(filename + ' downloaded successfully!')
            self.server.quit()


    def cd(self,fileName):
        if(fileName != ''):
            try:
                self.server.cwd(fileName)
            except ftplib.error_perm:
                pass
        else:
            # change working directory
            directory = input('Enter directory to go to: ')
            try:
                self.server.cwd(directory)
            except ValueError:
                print('ERROR: Directory not found!')

    def logon(self):
        if(self.GUILaunch):
            try:
                self.server = ftplib.FTP_TLS(host=self.serverURL, user=self.user, passwd=self.passwd,timeout=10)
                self.server.prot_p()
                self.secure = True
            except:
                self.server = ftplib.FTP(self.serverURL, self.user, self.passwd,'',10)
        else:
            while True:
                # credentials
                try:
                    host = input('Enter URL of FTP server: ')
                    anonymous = input('Is a username and password required y/n?: ')
                    # connect to server
                    if anonymous.lower() == 'y':
                        try:
                            user = input('Username: ')
                            passwd = input('Password: ')
                            self.server = ftplib.FTP(host, user, passwd,'',10)
                            self.server.encoding = 'utf-8'
                            break
                        except ValueError:
                            print('Incorrect URL, Username, or Password!')
                    elif anonymous.lower() == 'n':
                        try:
                            self.server = ftplib.FTP(host,'Anonymous','','',10)
                            self.server.encoding = 'utf-8'
                            break
                        except ValueError:
                            print('Incorrect URL, or a username/password is required!')
                    else:
                        print('Please enter y or n!')
                except TimeoutError:
                    print('Connection timed out. Please check URL and verify internet connection.')
    def cliUI(self):
        while True:
            print('Welcome to FTP Client!')
            userInput = input('Input upload, download, view, cd, or quit: ')
            if userInput.lower() == 'upload':
                self.upload('')
            elif userInput.lower() == 'download':
                self.download('','')
            elif userInput.lower() == 'view':
                self.view()
            elif userInput.lower() == 'cd':
                self.cd('')
            elif userInput.lower() == 'quit':
                self.server.quit()
            else:
                print('Command not recognized!')
