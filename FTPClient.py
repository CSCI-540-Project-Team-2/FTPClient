import ftplib
class FTPBackend:
    GUILaunch = False
    def __init__(self, server, user, passwd, isGUI):
        self.server = server
        self.user = user
        self.passwd = passwd
        self.GUILaunch = isGUI

    def upload(self, fileName):
        # filename to upload
        if(fileName != ''):
            try:
                with open(fileName, 'rb') as file:
                    self.server.storbinary('STOR {fileName}', file)
            except ValueError:
                print('still dunno')
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

    def download(self, fileName):
        # filename to retrieve
        if(fileName != ''):
            try:
                with open(fileName, 'wb') as file:
                    self.server.retrbinary('RETR {fileName}', file.write)
            except ValueError:
                print('i dunno')
        filename = input('Enter filename to download: ')
        try:
            with open(filename, 'wb') as file:
                self.server.retrbinary('RETR {filename}', file.write)
        except ValueError:
            print('ERROR: Could not download file!')
            self.server.quit()
        else:
            print(filename + ' downloaded successfully!')
            self.server.quit()


    def cd(self):
        # change working directory
        directory = input('Enter directory to go to: ')
        try:
            self.server.cwd(directory)
        except ValueError:
            print('ERROR: Directory not found!')

    def logon(self):
        if(self.GUILaunch):
            self.server = ftplib.FTP(self.server, self.user, self.passwd,'',10)
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
                self.download('')
            elif userInput.lower() == 'view':
                self.view()
            elif userInput.lower() == 'cd':
                self.cd()
            elif userInput.lower() == 'quit':
                self.server.quit()
            else:
                print('Command not recognized!')