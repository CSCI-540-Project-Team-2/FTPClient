import ftplib


def upload():
    # filename to upload
    filename = input('Enter filename to upload: ')
    try:
        with open(filename, 'rb') as file:
            server.storbinary(f'STOR {filename}', file)
    except ValueError:
        print('ERROR: Could not upload file!')
        server.quit()


def view():
    # view contents of server
    server.dir()


def download():
    # filename to retrieve
    filename = input('Enter filename to download: ')
    try:
        with open(filename, 'wb') as file:
            server.retrbinary(f'RETR {filename}', file.write)
    except ValueError:
        print('ERROR: Could not download file!')
        server.quit()
    else:
        print(filename + ' downloaded successfully!')
        server.quit()


def cd():
    # change working directory
    directory = input('Enter directory to go to: ')
    try:
        server.cwd(directory)
    except ValueError:
        print('ERROR: Directory not found!')


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
                server = ftplib.FTP(host, user, passwd,'','',10)
                server.encoding = 'utf-8'
                break
            except ValueError:
                print('Incorrect URL, Username, or Password!')
        elif anonymous.lower() == 'n':
            try:
                server = ftplib.FTP(host,'Anonymous','','',10)
                server.encoding = 'utf-8'
                break
            except ValueError:
                print('Incorrect URL, or a username/password is required!')
        else:
            print('Please enter y or n!')
    except TimeoutError:
        print('Connection timed out. Please check URL and verify internet connection.')


while True:
    print('Welcome to FTP Client!')
    userInput = input('Input upload, download, view, cd, or quit: ')
    if userInput.lower() == 'upload':
        upload()
    elif userInput.lower() == 'download':
        download()
    elif userInput.lower() == 'view':
        view()
    elif userInput.lower() == 'cd':
        cd()
    elif userInput.lower() == 'quit':
        quit()
    else:
        print('Command not recognized!')


