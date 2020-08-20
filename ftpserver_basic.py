import os
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import socket  

hostname = socket.gethostname()    
IPAddr = socket.gethostbyname(hostname)     
print("\n\n\t\t========= WELCOME! ==========")
print("\t\tFTP Server starting....")
print("\t\tHost: " + IPAddr+ " ; Port: 21") 
print("\t\tBrowser URL: ftp://"+IPAddr+"/")
print("\t\t============================\n\n")

authorizer = DummyAuthorizer()
cwd = os.getcwd()
authorizer.add_anonymous(cwd)

handler = FTPHandler
handler.authorizer = authorizer

server = FTPServer((IPAddr, 21), handler)
server.serve_forever()
