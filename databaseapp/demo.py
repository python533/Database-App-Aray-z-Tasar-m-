import sys
import os
import time
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QLabel, QGridLayout, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtSql import QSqlDatabase, QSqlQuery


class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(800, 600)
        label = QLabel('Main App', parent=self)


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Giriş Yap')
        self.setWindowIcon(QIcon(''))
        self.window_width, self.window_height = 600, 200
        self.setFixedSize(self.window_width, self.window_height)

        layout = QGridLayout()
        self.setLayout(layout)

        labels = {}
        self.lineEdits = {}

        labels['Kullanıcı Adı'] = QLabel('Kullanıcı Adı')
        labels['Şifre'] = QLabel('Şifre')
        labels['Kullanıcı Adı'].setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        labels['Şifre'].setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.lineEdits['Kullanıcı Adı'] = QLineEdit()
        self.lineEdits['Şifre'] = QLineEdit()
        self.lineEdits['Şifre'].setEchoMode(QLineEdit.EchoMode.Password)

        layout.addWidget(labels['Kullanıcı Adı'], 0, 0, 1, 1)
        layout.addWidget(self.lineEdits['Kullanıcı Adı'], 0, 1, 1, 3)

        layout.addWidget(labels['Şifre'], 1, 0, 1, 1)
        layout.addWidget(self.lineEdits['Şifre'], 1, 1, 1, 3)

        button_login = QPushButton('&Giriş Yap', clicked=self.checkCredential)
        layout.addWidget(button_login, 2, 3, 1, 1)

        self.status = QLabel('')
        self.status.setStyleSheet('font-size: 25px; color: red;')
        layout.addWidget(self.status, 3, 0, 1, 3)

        self.connectToDB()

    def connectToDB(self):
        # https://doc.qt.io/qt-5/sql-driver.html
        db = QSqlDatabase.addDatabase('QODBC')
        db.setDatabaseName('<connection string>')

        if not db.open():
            self.status.setText('VeriTabanına Bağlanılamadı!')

    def checkCredential(self):
        username = self.lineEdits['Kullanıcı Adı'].text()
        password = self.lineEdits['Şifre'].text()

        query = QSqlQuery()
        query.prepare('SELECT * FROM Users WHERE Username=:username')
        query.bindValue(':username', username)
        query.exec()

        if query.first():
            if query.value('Password') == password:
                time.sleep(1)
                self.mainApp = MainApp()
                self.mainApp.show()
                self.close()
            else:
                self.status.setText('Şifreniz Yanlış')
        else:
            self.status.setText('Kullanıcı Adı Bulunamadı!')


if __name__ == '__main__':
    # don't auto scale when drag app to a different monitor.
    # QApplication.setAttribute(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    app = QApplication(sys.argv)
    app.setStyleSheet('''
        QWidget {
            font-size: 25px;
        }
        QLineEdit {
            height: 200px;
        }
    ''')

    loginWindow = LoginWindow()
    loginWindow.show()

    try:
        sys.exit(app.exec())
    except SystemExit:
        print('Closing Window...')