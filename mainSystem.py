import instaloader
import os
import time
import random
from PyQt5.QtCore import QThread, QObject, pyqtSignal
from PyQt5.QtWidgets import ( QFileDialog)

class mainSystem(QObject):
    log_signal = pyqtSignal(str)        # 로그 메시지 전달
    progress_signal = pyqtSignal(int,int)   # 진행률 전달
    finished = pyqtSignal() 
    
    def __init__(self):
        super().__init__()
        
        #Instagram 다운로더 객체 생성
        self.Instagram = instaloader.Instaloader(download_videos=True, save_metadata=False,)
        self.Loggedin = False
        self.UserName = None
        self.Password = None

        self.MainGUI = None
        self.txtPath = None
        self.savePath = None
        self.logcallback = None

        #비동기 객체
        self.thread = None
        self.worker = None
    
    def SetGui(self, gui):
        self.MainGUI = gui
        self.logcallback = gui.wirteLog

    def SeleteFile(self):
        path, _ = QFileDialog.getOpenFileName(
            self.MainGUI,
            "텍스트 파일 선택",
            "",
            "Text Files (*.txt);;All Files (*)"
        )
        self.txtPath = path
        return path
        

    def SeleteFolder(self):
        path = QFileDialog.getExistingDirectory(
            self.MainGUI,
            "폴더 선택",
            ""
        )
        self.savePath = path
        self.Instagram.dirname_pattern = path
        return path

    def checkLogin(self, username, password):
        if self.Instagram is None: return False
        if len(username) == 0 or len(password) == 0: return
        
        errMsg = None

        try:
            self.Instagram.login(username,password)
            self.UserName = username
            self.Password = password
            self.loggedin = True

        except Exception as e:
            self.loggedin = False
            errMsg = str(e)

        return self.loggedin , errMsg

    def cleanup_thread(self):
        if self.thread:
            self.thread.deleteLater()  # QThread 객체 제거
            self.thread = None         # 참조 제거
        self.log_signal.emit(f"[INFO] 작업자 Thread 종료 완료.")


    def init_thread(self, log_callback, progress_callback):
        
        if self.thread is not None and self.thread.isRunning(): return
        
        self.thread = QThread()
        self.moveToThread(self.thread)
        
        # UI 객체와 시그널 연결
        self.thread.started.connect(self.run_async)
        self.log_signal.connect(log_callback)
        self.progress_signal.connect(progress_callback)

         # 스레드 종료 후 정리
        self.finished.connect(self.thread.quit)  # QThread 종료
        self.thread.finished.connect(self.cleanup_thread)  # 스레드 정리

        self.thread.start()

    def run_async(self):
        try:
            with open(self.txtPath, "r") as f:
                urls = [line.strip() for line in f if line.strip()]

                if len(urls) == 0 : return

            total_count = len(urls)
            self.log_signal.emit(f"[INFO] {total_count}개 다운로드 작업 시작")
            
            for idx, url in enumerate(urls, 1):
                try:
                    shortcode = url.split("/")[-2]
                    post = instaloader.Post.from_shortcode(self.Instagram.context, shortcode)
                    username = post.owner_username
                    
                    save_name = os.path.join(self.savePath,f"{idx:03} ID {username}")
                    self.Instagram.dirname_pattern = save_name
                    
                    # 다운로드
                    self.Instagram.download_post(post,target = save_name)

                    # 10~ 30 초 대기기
                    sleep_sec = random.randint(20, 50)

                    # Log 및 실행 경로 분석
                    self.log_signal.emit(f"[INFO] 인스타 계정 : {username} 다운로드 완료 - {sleep_sec}초 다운로드 대기")
                    self.progress_signal.emit(idx, total_count)
                    
                    if idx != total_count:
                        time.sleep(sleep_sec)

                except Exception as e:
                    self.log_signal.emit(f"[WARNING] 작업이 중단되었습니다. : {e}")
                    break
                
                # 너무 빠른 요청 방지
                if idx % 10 == 0:
                    long_sleep = random.randint(60 * 5 , 60 * 10)
                    self.log_signal.emit(f"[INFO] 10개 다운로드 완료, {long_sleep//60}분 대기")
                    time.sleep(long_sleep)

        except:
            self.log_signal.emit(f"[WARNING] txt 파일의 Url 목록을 읽어오는데 실패 했습니다")
            return
        
        self.log_signal.emit(f"[INFO] 다운로드 완료 작업이 종료 됩니다.")
        self.finished.emit()
        return
    