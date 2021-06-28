from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import os,socket,http.server,socketserver
import threading

hostname = socket.gethostname()    
IPAddr = socket.gethostbyname(hostname)    


#HTTP
handler = http.server.SimpleHTTPRequestHandler
httpd =  socketserver.TCPServer(("0.0.0.0", 5000), handler)

#FTP
authorizer = DummyAuthorizer()
cwd = os.getcwd()
authorizer.add_anonymous(cwd)
handler = FTPHandler
handler.authorizer = authorizer
ftpd = FTPServer(("0.0.0.0", 2121), handler)

t1 = threading.Thread(target=httpd.serve_forever)
t2 = threading.Thread(target=ftpd.serve_forever)
 
t1.start(); t2.start()

print("\n\n===== WELCOME =====")
print("FTP Server starting....")
print("Host: " + IPAddr) 
print("Port: 2121")
print("===================\n\n")
print("HTTP Server starting....")
print("Host: " + IPAddr) 
print("Port: 5000")
print("===================\n\n")

t1.join(); t2.join()