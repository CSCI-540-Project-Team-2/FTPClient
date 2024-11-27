from FTPClient import FTPBackend
client = FTPBackend('','','',False)
client.logon()
client.cliUI()
