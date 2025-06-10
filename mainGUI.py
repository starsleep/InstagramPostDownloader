import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QDialog, QMessageBox, QSizePolicy,
    QTextEdit, QFileDialog, QVBoxLayout, QHBoxLayout, QMainWindow, QProgressBar
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QGuiApplication

#Const
WINDOW_WITDH = 1000
WINDOW_HEIGHT = 550

class RootGui(QWidget):
    def setCenter(self, width , height):
        self.resize(width, height)

        screen = QGuiApplication.primaryScreen()
        screen_rect = screen.availableGeometry()
        
        x = (screen_rect.width() - self.width()) // 2
        y = (screen_rect.height() - self.height()) // 2
        
        self.move(x, y)

    def InitGui(self):
        pass

    def MessageInfo(self, msg):
        QMessageBox.information(self, "Info", msg)

    def MessageWarning(self, msg):
        QMessageBox.warning(self, "Warning", msg)


class MainGui(QMainWindow, RootGui):
    def __init__(self, mainSystem):
        super().__init__()
        self.mainsystem = mainSystem

        self.setWindowTitle("Instagram Post Downloder")
        self.setCenter(WINDOW_WITDH,WINDOW_HEIGHT)
        self.InitGui()

        #Thread 생성


    def InitGui(self):
        central_widget = QWidget()
        main_layout = QVBoxLayout()

        # ===== [1] 파일 경로 입력 =====
        file_label = QLabel("Instagram URL txt 파일 경로")
        self.txt_path_input = QLineEdit()
        file_btn = QPushButton(".txt 파일 선택")
        file_btn.clicked.connect(self.SeleteFile)

        file_layout = QHBoxLayout()
        file_layout.addWidget(self.txt_path_input)
        file_layout.addWidget(file_btn)

        main_layout.addWidget(file_label)
        main_layout.addLayout(file_layout)

        # ===== [2] 저장 폴더 입력 =====
        folder_label = QLabel("저장할 폴더 경로")
        self.folder_path_input = QLineEdit()
        folder_btn = QPushButton("저장 폴더 선택")
        folder_btn.clicked.connect(self.SeleteFolder)

        folder_layout = QHBoxLayout()
        folder_layout.addWidget(self.folder_path_input)
        folder_layout.addWidget(folder_btn)

        main_layout.addWidget(folder_label)
        main_layout.addLayout(folder_layout)

        # ===== [3] 다운로드 버튼 =====
        download_btn = QPushButton("▶ 다운로드 시작")
        download_btn.setStyleSheet("background-color: #4CAF50; color: white; height: 30px;")
        download_btn.clicked.connect(self.startdownload)

        main_layout.addWidget(download_btn, alignment=Qt.AlignCenter)

        # ===== [3] 프로그래스 바바 =====
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        main_layout.addWidget(self.progress_bar)

        # ===== [4] 결과 출력창 =====
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        main_layout.addWidget(self.log_output)

        # ===== [5] 하단 라벨 =====
        footer = QLabel("Made by winwoo Park for One Melody")
        footer.setAlignment(Qt.AlignLeft)
        main_layout.addWidget(footer)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        return
    
    def SeleteFile(self):
        if self.mainsystem is None: return

        path = self.mainsystem.SeleteFile()

        if len(path) == 0 : return

        self.txt_path_input.setText(path)

        return

    def SeleteFolder(self):
        if self.mainsystem is None: return

        path = self.mainsystem.SeleteFolder()

        if len(path) == 0 : return

        self.folder_path_input.setText(path)

        return

    def startdownload(self):
        if self.mainsystem is None: return

        self.mainsystem.init_thread(self.wirteLog , self.setprogress)

    def wirteLog(self,msg):
        if len(msg) == 0 : return

        self.log_output.append(msg)

    def setprogress(self, cur, total):
        present = round((cur / total) * 100)
        self.progress_bar.setValue(present)
        



LOGIN_WIDTH = 300
LOGIN_HEIGH = 150

class LoginGui(QDialog, RootGui):
    def __init__(self, mainSystem):
        super().__init__()
        self.mainsystem = mainSystem
        
        self.setWindowTitle("Login")
        self.setCenter(LOGIN_WIDTH,LOGIN_HEIGH)
        self.InitGui()

    def InitGui(self):
        self.id_input = QLineEdit(self)
        self.pw_input = QLineEdit(self)
        self.pw_input.setEchoMode(QLineEdit.Password)

        self.login_btn = QPushButton("Login")
        self.login_btn.clicked.connect(self.checklogin)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("ID:"))
        layout.addWidget(self.id_input)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.pw_input)
        layout.addWidget(self.login_btn)
        self.setLayout(layout)

        return super().InitGui()
        
    def checklogin(self):
        if self.mainsystem is None : 
            RootGui.MessageWarning("mainsystem is None")
        
        username = self.id_input.text()
        password = self.pw_input.text()

        Loginflag , errMsg = self.mainsystem.checkLogin(username,password)

        if Loginflag:
            QMessageBox.information(self, "Info", "로그인 성공")
            self.accept()
        else :
            QMessageBox.warning(self, "Warning", errMsg)
            

