import sys
from PySide2.QtWidgets import * 
from PySide2.QtGui import QIcon
import os
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import socket  
import threading

class Form(QDialog):

    def __init__(self): 
        super(Form, self).__init__()

        self.setWindowTitle("FTP Server")

        # Top Message
        self.message = QLabel()
        hostname = socket.gethostname()    
        self.IPAddr = socket.gethostbyname(hostname)
        msg = "Welcome! \n"+"Host IP: " + self.IPAddr
        self.message.setText(msg)

        self.start = QPushButton("Start")
        self.stop = QPushButton("Stop")

        # Top Message
        self.log = QLabel()
        self.log.setOpenExternalLinks(True)
        self.log.setText("Server Stopped!")
        
        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(self.message)
        layout.addWidget(self.start)
        layout.addWidget(self.stop)
        layout.addWidget(self.log)
        self.setLayout(layout)

        # Add button signal to greetings slot
        self.start.clicked.connect(self.stratServer)
        self.stop.clicked.connect(self.stopServer)
        

    def stratServer(self):
        authorizer = DummyAuthorizer()
        cwd = os.getcwd()
        authorizer.add_anonymous(cwd)
        handler = FTPHandler
        handler.authorizer = authorizer
        self.server = FTPServer((self.IPAddr, 21), handler)
        srv = threading.Thread(target=self.server.serve_forever,daemon=True)
        srv.start()
        link = "ftp://"+self.IPAddr
        self.log.setText("FTP server started @ " + '''<a href=%s>%s</a>'''%(link,link) )

    def stopServer(self):
        self.server.close_all()
        self.log.setText("Server Stopped!")

if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./smiley.ico"))
    
    # Create and show the form
    form = Form()
    form.show()

    # Run the main Qt loop
    app.exec_()

#Links
#https://pyinstaller.readthedocs.io/en/stable/usage.html
#https://www.learnpyqt.com/courses/packaging-and-distribution/packaging-pyqt5-pyside2-applications-windows-pyinstaller/
#https://stackoverflow.com/questions/7674790/bundling-data-files-with-pyinstaller-onefile