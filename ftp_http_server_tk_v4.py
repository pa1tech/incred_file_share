#pyinstaller --icon=smiley.ico --add-data="smiley.ico;." --onefile ftp_http_server_tk.py 

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from socket import gethostname,getaddrinfo,AF_INET
from http.server import SimpleHTTPRequestHandler
import socketserver,ctypes
import tkinter as tk
from threading import Thread
import sys,os
from tkinter import filedialog
import functools

myappid = 'pa1tech.ftpserver.4'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
cwd = os.path.dirname(os.path.realpath(__file__))

def hideConsole():
  whnd = ctypes.windll.kernel32.GetConsoleWindow()
  if whnd != 0:
     ctypes.windll.user32.ShowWindow(whnd, 0)

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

class tkFTP():
	def __init__(self): 
		#Configuring window
		window = tk.Tk()
		window.title("!ncred File Share")
		window.geometry("450x250")
		window.resizable(width=False, height=False)
		window.grid_columnconfigure((0,1), weight=1, uniform="fred")
		window.iconbitmap(resource_path("smiley.ico"))

		self.IPAddr = [i[4][0] for i in getaddrinfo(gethostname(), None, family=AF_INET)]
		self.ftpserver = None; self.httpserver = None

		self.widgets()
		self.placeGrid()
		hideConsole()
		window.mainloop()

	def widgets(self):
		self.greeting = tk.Label(text="Welcome to !ncred File Share",font=("", 15, 'bold'))

		self.host_msg = tk.Label(text="Host IP's:",font=("", 12, 'italic'),anchor='e')
		self.host = tk.Label(text=str(self.IPAddr),font=("", 10, 'bold'))

		global cwd
		self.dir = tk.Label(text=cwd,font=("", 10))
		self.browse = tk.Button(text="Browse",command=self.changeDir,font=("", 10, 'bold'))

		self.start = tk.Button(text="Start server",command=self.startServer,font=("", 11, 'bold'))
		self.stop = tk.Button(text="Stop server",command=self.stopServer,font=("", 11, 'bold'))

		self.link = tk.Label( text="Server stopped!", fg="blue", cursor="hand2",font=("", 11, 'bold'))

	def placeGrid(self):
		self.greeting.grid(row=0,column=0,columnspan=2,padx=15,pady=10)
		self.host_msg.grid(row=1,column=0,pady=5); self.host.grid(row=1,column=1,pady=5)

		self.dir.grid(row=2,column=0,columnspan=2,sticky="w",padx=[30,0],pady=5)
		self.browse.grid(row=2,column=0,columnspan=2,padx=[325,0],pady=5)

		self.start.grid(row=3,column=0,padx=15,pady=10); self.stop.grid(row=3,column=1,padx=15,pady=10)
		self.link.grid(row=4,column=0,columnspan=2,padx=15,pady=5)

	def startServer(self):
		global cwd
		authorizer = DummyAuthorizer(); authorizer.add_anonymous(cwd)

		ftphandler = FTPHandler; ftphandler.authorizer = authorizer
		httphandler = functools.partial(SimpleHTTPRequestHandler, directory=cwd)

		self.httpserver =  socketserver.TCPServer(("0.0.0.0", 8080), httphandler)
		self.ftpserver = FTPServer(('0.0.0.0',2121), ftphandler)

		ftp = Thread(target=self.ftpserver.serve_forever,daemon=True)
		http = Thread(target=self.httpserver.serve_forever,daemon=True)
		http.start(); ftp.start()


		self.link['text'] = "FTP Server started @ ftp://<hostip>:2121 \n\n HTTP Server started @ http://<hostip>:8080"

	def stopServer(self):
		self.ftpserver.close_all()
		self.httpserver.shutdown()
		self.httpserver.server_close()

		self.link['text'] = "Server stopped!"
	
	def changeDir(self):
		global cwd
		cwd = filedialog.askdirectory()
		self.dir['text'] = cwd

if __name__ == '__main__':
	tkFTP()


