from os import path,getcwd
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from socket import gethostname,gethostbyname
import tkinter as tk
from threading import Thread

class tkFTP():
	def __init__(self): 
		#Configuring window
		window = tk.Tk()
		window.title("FTP Server")
		window.geometry("320x180")
		window.resizable(width=False, height=False)
		window.grid_columnconfigure((0,1), weight=1, uniform="fred")
		window.iconbitmap("./smiley.ico")

		#FTP variables
		hostname = gethostname(); cwd = getcwd()
		authorizer = DummyAuthorizer(); authorizer.add_anonymous(cwd)
		self.handler = FTPHandler; self.handler.authorizer = authorizer

		self.IPAddr = gethostbyname(hostname); self.p = 21
		self.server = None

		self.widgets()
		self.placeGrid()
		window.mainloop()

	def widgets(self):
		self.greeting = tk.Label(text="Welcome to !ncredible Tech FTP Server",font=("", 10, 'bold'))

		self.host_msg = tk.Label(text="Host IP:",font=("", 10, 'italic'),anchor='e')
		self.port_msg = tk.Label(text="Port:",font=("", 10, 'italic'),anchor="e")

		self.host = tk.Label(text=self.IPAddr,font=("", 10, 'bold'))
		self.port = tk.Entry(width=10,font=("", 10, 'bold')); self.port.insert(0, "21")

		self.start = tk.Button(text="Start server",command=self.startServer,font=("", 11, 'bold'))
		self.stop = tk.Button(text="Stop server",command=self.stopServer,font=("", 11, 'bold'))

		self.link = tk.Label( text="Server stopped!", fg="blue", cursor="hand2",font=("", 11, 'bold'))

	def placeGrid(self):
		self.greeting.grid(row=0,column=0,columnspan=2,padx=15,pady=5)
		self.host_msg.grid(row=1,column=0,pady=0); self.host.grid(row=1,column=1,pady=0)
		self.port_msg.grid(row=2,column=0,pady=0); self.port.grid(row=2,column=1,pady=0)
		self.start.grid(row=3,column=0,padx=15,pady=10); self.stop.grid(row=3,column=1,padx=15,pady=10)
		self.link.grid(row=4,column=0,columnspan=2,padx=15,pady=5)

	def startServer(self):
		try:
			self.p = int(self.port.get())
		except:
			pass
		self.server = FTPServer((self.IPAddr,self.p), self.handler)
		srv = Thread(target=self.server.serve_forever,daemon=True)
		srv.start()
		self.link['text'] = "Server started @ ftp://"+str(self.IPAddr)+":"+str(self.p)

	def stopServer(self):
		self.link['text'] = "Server stopped!"
		self.server.close_all()

if __name__ == '__main__':
	tkFTP()
