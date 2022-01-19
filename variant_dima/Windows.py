from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QWidget, QPushButton, QLineEdit, QLabel, QComboBox, \
    QMessageBox, QHBoxLayout, QVBoxLayout, QTableWidget, QSizePolicy

from mysql_connection import MySQLServer

session = {}

class MyMainWindow(QMainWindow):
    def __init__(self, widget_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.window = widget_list
        for i in self.window:
            i.change_state[int].connect(self.change_state)
        self.initUi()

    def initUi(self):
        self.stackedWidget = QStackedWidget(self)
        for i in self.window:
            self.stackedWidget.addWidget(i)
        self.stackedWidget.resize(500, 600)
        self.stackedWidget.setCurrentWidget(self.window[0])

    def change_state(self, state):
        self.stackedWidget.setCurrentIndex(state)

    def get_session(self) -> dict:
        return self.session


class State(QWidget):
    change_state = pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def set_state(self, state):
        self.change_state.emit(state)

    def session(self) -> dict:
        return self.get_session()

    def clear_session(self):
        self.session = {}


class MainWindow(State):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUi()

    def initUi(self):
        self.btnReg = QPushButton("Регистрация", self)
        self.btnReg.clicked.connect(lambda: self.set_state(1))
        self.btnReg.setGeometry(170, 70, 200, 30)

        self.btnAuth = QPushButton("Авторизация", self)
        self.btnAuth.clicked.connect(lambda: self.set_state(2))
        self.btnAuth.setGeometry(170, 110, 200, 30)


class Registration(State):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUi()

    def initUi(self):
        self.btnBack = QPushButton("Назад", self)
        self.btnBack.clicked.connect(lambda: self.set_state(0))
        self.btnBack.setGeometry(0, 0, 100, 30)

        self.LLogin = QLabel("Логин:", self)
        self.LLogin.move(10, 40)
        self.Login = QLineEdit(self)
        self.Login.setGeometry(120, 40, 100, 20)

        self.LPassword = QLabel("Пароль:", self)
        self.LPassword.move(10, 80)
        self.Password = QLineEdit(self)
        self.Password.setEchoMode(QLineEdit.Password)
        self.Password.setGeometry(120, 80, 100, 20)

        server = MySQLServer('127.0.0.1', 'root', 'root', 'company', 3307)
        self.rows = server.select('role', ['name', 'id'])
        server.close()
        arr = []
        for name in self.rows:
            arr.append(name['name'])
        self.LRole = QLabel("Роль:", self)
        self.LRole.move(10, 120)
        self.Role = QComboBox(self)
        self.Role.addItems(arr)
        self.Role.setGeometry(120, 120, 100, 20)

        self.BtnReg = QPushButton("Зарегистрироваться", self)
        self.BtnReg.setGeometry(110, 150, 120, 20)
        self.BtnReg.clicked.connect(lambda: self.ApplyReg())

        self.BtnReg = QPushButton("Отмена", self)
        self.BtnReg.setGeometry(250, 150, 100, 20)
        self.BtnReg.clicked.connect(lambda: self.set_state(0))

    def ApplyReg(self):
        login: str = str(self.Login.text())
        password: str = str(self.Password.text())
        role: str = str(self.Role.currentText())
        role_id = 0
        for r in self.rows:
            if r['name'] == role:
                role_id = r['id']
                break
        data = {'login': login, 'password': password, 'role_id': role_id}
        server = MySQLServer('127.0.0.1', 'root', 'root', 'company', 3307)
        result = server.insert('user', data)
        if result == 1:
            QMessageBox.critical(self, "Регистрация", "Ошибка!")
        else:
            server.close()
            self.set_state(0)
            QMessageBox.information(self, "Регистрация", "Успешно зарегистрирован новый пользователь")


class Login(State):
    open_signal = pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUi()

    def initUi(self):
        self.LLogin = QLabel("Логин:", self)
        self.LLogin.move(10, 40)
        self.Login = QLineEdit(self)
        self.Login.setGeometry(120, 40, 100, 20)

        self.LPassword = QLabel("Пароль:", self)
        self.LPassword.move(10, 80)
        self.Password = QLineEdit(self)
        self.Password.setEchoMode(QLineEdit.Password)
        self.Password.setGeometry(120, 80, 100, 20)

        self.btnLogin = QPushButton("Войти", self)
        self.btnLogin.setGeometry(120, 120, 100, 20)
        self.btnLogin.clicked.connect(lambda: self.auth())

        self.BtnCancel = QPushButton("Отмена", self)
        self.BtnCancel.clicked.connect(lambda: self.set_state(0))
        self.BtnCancel.setGeometry(230, 120, 100, 20)

        self.btnBack = QPushButton("Назад", self)
        self.btnBack.clicked.connect(lambda: self.set_state(0))
        self.btnBack.setGeometry(0, 0, 100, 30)

    def auth(self):
        login: str = str(self.Login.text())
        password: str = str(self.Password.text())
        server = MySQLServer('127.0.0.1', 'root', 'root', 'company', 3307)
        condition = f'`login`="{login}" AND `password`="{password}"'
        is_exists = server.is_exists('user', condition)
        if is_exists:
            data = server.select('user', ['role_id'], condition)[0]
            session['login'] = login
            session['password'] = password
            role = data['role_id']+2
            self.set_state(role)
        else:
            QMessageBox.critical(self, "Ошибка!", "Неверный логин и(или) пароль")
        server.close()


class WinAcc(State):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def initUI(self):
        self.btnBack = QPushButton("Назад", self)
        self.btnBack.clicked.connect(lambda: self.exit())
        self.btnBack.setGeometry(0, 0, 100, 30)

    def init_director(self):
        self.name_widget = QLabel("Директор", self)
        self.name_widget.move(10, 80)

    def init_manager(self):
        self.name_widget = QLabel("Менеджер", self)
        self.name_widget.move(10, 80)

    def init_keeper(self):
        self.name_widget = QLabel("Кладовщик", self)
        self.name_widget.move(10, 80)

    def init_customer(self):
        self.name_widget = QLabel("Заказчик", self)
        self.name_widget.move(10, 80)

    def open_signal(self, role):
        print(role)
        self.initUI()
        if role == 1: self.init_director()
        elif role == 2: self.init_manager()
        elif role == 3: self.init_keeper()
        else: self.init_customer()

    def exit(self):
        session = {}
        self.set_state(0)


class Director(State):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUI()

    def initUI(self):
        self.btnBack = QPushButton("Назад", self)
        self.btnBack.clicked.connect(lambda: self.exit())
        self.btnBack.setGeometry(0, 0, 100, 30)

        self.name_widget = QLabel("Директор", self)
        self.name_widget.move(10, 80)

    def exit(self):
        session = {}
        self.set_state(0)


class Manager(State):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUI()

    def initUI(self):
        self.btnBack = QPushButton("Назад", self)
        self.btnBack.clicked.connect(lambda: self.exit())
        self.btnBack.setGeometry(0, 0, 100, 30)

        self.name_widget = QLabel("Менеджер", self)
        self.name_widget.move(10, 80)

    def exit(self):
        session = {}
        self.set_state(0)


class Keeper(State):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUI()

    def initUI(self):
        self.setMinimumSize(QtCore.QSize(0, 12))
        self.setMaximumSize(QtCore.QSize(1920, 1080))

        btnBack = QPushButton("Назад")
        btnBack.clicked.connect(lambda: self.exit())

        name_widget = QLabel("Экран кладовщика")
        name_widget.setFont(QFont('Arial', 10))

        hbox = QHBoxLayout()
        hbox.addWidget(btnBack)
        hbox.addWidget(name_widget)
        hbox.setAlignment(Qt.AlignLeft)
        hbox.setAlignment(Qt.AlignTop)

        table = QTableWidget()
        table.setColumnCount(3)
        table.setRowCount(1)

        table.setMinimumSize(QtCore.QSize(0, 12))
        table.setMaximumSize(QtCore.QSize(1920, 1080))

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addWidget(table, stretch=1)

        vbox.addStretch(1)
        self.setLayout(vbox)






    def exit(self):
        session = {}
        self.set_state(0)


class Customer(State):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUI()

    def initUI(self):
        self.btnBack = QPushButton("Назад", self)
        self.btnBack.clicked.connect(lambda: self.exit())
        self.btnBack.setGeometry(0, 0, 100, 30)

        self.name_widget = QLabel("Заказчик", self)
        self.name_widget.move(10, 80)

    def exit(self):
        session = {}
        self.set_state(0)