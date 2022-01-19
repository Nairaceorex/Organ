from PyQt5.QtWidgets import QLineEdit, QLabel, QPushButton
from .Windows import State


class Login(State):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUi()


    def initUi(self):
        self.LLogin = QLabel("Login:", self)
        self.LLogin.move(10, 40)
        self.Email = QLineEdit(self)
        self.Email.setGeometry(120, 40, 100, 20)

        self.LPassword = QLabel("Password:", self)
        self.LPassword.move(10, 80)
        self.Password = QLineEdit(self)
        self.Password.setEchoMode(QLineEdit.Password)
        self.Password.setGeometry(120, 80, 100, 20)

        self.btnLogin = QPushButton("Login", self)
        self.btnLogin.setGeometry(120, 120, 100, 20)

        self.BtnCancel = QPushButton("Cancel", self)
        self.BtnCancel.clicked.connect(lambda: self.set_state(0))
        self.BtnCancel.setGeometry(230, 120, 100, 20)

        self.btnBack = QPushButton("Back", self)
        self.btnBack.clicked.connect(lambda: self.set_state(0))
        self.btnBack.setGeometry(0, 0, 100, 30)