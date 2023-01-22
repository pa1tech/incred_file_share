#pyinstaller --noconsole --icon=smiley.ico --add-data="smiley.ico;." --onefile ftp_http_tk_build.py

from os import path,getcwd
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from socket import gethostname,gethostbyname,getaddrinfo,AF_INET
import http.server,socketserver,ctypes
import tkinter as tk
from threading import Thread

myappid = 'pa1tech.ftpserver.3'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
    
class tkFTP():
	def __init__(self): 
		#Configuring window
		window = tk.Tk()
		window.title("!ncred File Share")
		window.geometry("400x210")
		window.resizable(width=False, height=False)
		window.grid_columnconfigure((0,1), weight=1, uniform="fred")
		window.iconbitmap(resource_path("smiley.ico"))

		#FTP variables
		cwd = getcwd(); authorizer = DummyAuthorizer(); authorizer.add_anonymous(cwd)
		self.ftphandler = FTPHandler; self.ftphandler.authorizer = authorizer
		self.httphandler = http.server.SimpleHTTPRequestHandler	

		self.IPAddr = [i[4][0] for i in getaddrinfo(gethostname(), None, family=AF_INET)]
		self.ftpserver = None; self.httpserver = None

		self.widgets()
		self.placeGrid()
		window.mainloop()

	def widgets(self):
		self.greeting = tk.Label(text="Welcome to !ncred File Share",font=("", 15, 'bold'))

		self.host_msg = tk.Label(text="Host IP's:",font=("", 12, 'italic'),anchor='e')
		self.host = tk.Label(text=str(self.IPAddr),font=("", 10, 'bold'))

		self.start = tk.Button(text="Start server",command=self.startServer,font=("", 11, 'bold'))
		self.stop = tk.Button(text="Stop server",command=self.stopServer,font=("", 11, 'bold'))

		self.link = tk.Label( text="Server stopped!", fg="blue", cursor="hand2",font=("", 11, 'bold'))

	def placeGrid(self):
		self.greeting.grid(row=0,column=0,columnspan=2,padx=15,pady=10)
		self.host_msg.grid(row=1,column=0,pady=5); self.host.grid(row=1,column=1,pady=5)
		self.start.grid(row=2,column=0,padx=15,pady=10); self.stop.grid(row=2,column=1,padx=15,pady=10)
		self.link.grid(row=3,column=0,columnspan=2,padx=15,pady=5)

	def startServer(self):
		self.ftpserver = FTPServer(('0.0.0.0',2121), self.ftphandler)
		self.httpserver =  socketserver.TCPServer(("0.0.0.0", 8080), self.httphandler)

		ftp = Thread(target=self.ftpserver.serve_forever,daemon=True)
		http = Thread(target=self.httpserver.serve_forever,daemon=True)
		ftp.start(); http.start()

		self.link['text'] = "FTP Server started @ ftp://<hostip>:2121 \n\n HTTP Server started @ http://<hostip>:8080"

	def stopServer(self):
		self.ftpserver.close_all()
		self.httpserver.shutdown(); self.httpserver.server_close()
		self.link['text'] = "Server stopped!"

if __name__ == '__main__':
	tkFTP()


