import sys
from PyQt5.QtWidgets import QApplication, QDialog

from mainSystem import mainSystem
from mainGUI import MainGui
from mainGUI import LoginGui

#빌드 경로 pyinstaller --onefile --noconsole --hidden-import=instaloader D:\Project\InstagramImageDownloader\main.py

def main():
    app = QApplication(sys.argv)

    mainsystem = mainSystem()
    #loginGui = LoginGui(mainsystem)
    
    #if loginGui.exec_() == QDialog.Accepted:
    mainGui = MainGui(mainsystem)
    mainsystem.SetGui(mainGui)

    mainGui.show()
    app.exit(app.exec_())
    #else:
         #app.exit()
    
    return


if __name__ == "__main__":
    main()