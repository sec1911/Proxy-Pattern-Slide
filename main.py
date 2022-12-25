from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *

from typing import Union
import sys

###############################################
# ApiInterface class is SUBJECT INTERFACE
###############################################
class ApiInterface:
    # This class is the common interface that both proxy and the real object
    # will implement.

    def fetchResource(self, user: str) -> str:
        raise NotImplementedError()

###############################################
# RealApi class is REAL SUBJECT
###############################################
class RealApi(ApiInterface):
    # This class is the real object that has not protection on its resources
    # whatsoever.
    def __init__(self) -> None:
        pass

    def fetchResource(self, user: str) -> str:
        return (f'I am serving a resource to the client: "{user}"\n')

###############################################
# Proxy class is PROTECTION PROXY
###############################################
class Proxy(ApiInterface):

    def __init__(self) -> None:
        self.real_subject = RealApi()

    def fetchResource(self, user: str) -> str:
        print(f'Client "{user}" has requested to access a resource...\n')

        if user == "Authorized User":
            return self.real_subject.fetchResource(user)
        else:
            return f"Sorry, only \"Authorized User\" can access my resource.\nYou called me as \"{user}\"\n"

#######################################################################################

def clientAction(server: Union[RealApi, Proxy], user: str) -> str:
    return server.fetchResource(user=user)

#######################################################################################


#print(clientAction(server = proxy1, user="anonymous"))
#print(clientAction(server = proxy1, user="Authorized User"))
#print(clientAction(server = proxy1, user="Authorized User"))


class Win(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Protected API application.")
        self.setGeometry(10, 10, 400, 300)
        self._proxy = Proxy()
        self._real_api = RealApi()


        self.formGroupBox = QGroupBox("Api Fetch:")
        self.serverTypeComboBox = QComboBox()
        self.serverTypeComboBox.addItems(["Real Api", "Proxy Server"])
        self.userNameLineEdit = QLineEdit()
        self.createForm()
        self.buttonBox = QPushButton('Fetch Resource')
        self.buttonBox.clicked.connect(self.doClientAction)
        self.outputBox = QTextBrowser()

        layout = QVBoxLayout()
        layout.addWidget(self.formGroupBox)
        layout.addWidget(self.buttonBox)
        layout.addWidget(self.outputBox)
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.show()


    def createForm(self):
        layout = QFormLayout()
        layout.addRow(QLabel("User Credentials:"), self.userNameLineEdit)
        layout.addRow(QLabel("Server to fetch:"), self.serverTypeComboBox)
        self.formGroupBox.setLayout(layout)

    def doClientAction(self):
        #self.outputBox.insertPlainText(self.userNameLineEdit.text())
        #self.outputBox.insertPlainText(self.serverTypeComboBox.currentText())
        username = self.userNameLineEdit.text()
        if self.serverTypeComboBox.currentText() == "Real Api":
            self.outputBox.insertPlainText(clientAction(self._real_api, user=username))
        else:
            self.outputBox.insertPlainText(clientAction(self._proxy, user=username))
        self.outputBox.insertPlainText("~~~~~~ END OF TRANSACTION ~~~~~~\n")
#######################################################################################
if __name__ == '__main__':

    app = QApplication([])
    win = Win()
    sys.exit(app.exec())





