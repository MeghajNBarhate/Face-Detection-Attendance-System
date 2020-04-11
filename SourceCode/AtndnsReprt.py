from PyQt5 import *
from PyQt5 import QtCore, QtGui, QtWidgets
import os
import shutil

class Ui_MainWindow1(object):
    def setupUi(self, MainWindow):

        prsnt_data = ["Present_peple"]
        
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        log_dir = os.path.join(BASE_DIR, "Attendance_logs\\temp")
        for filename in os.listdir('C:\\Users\\megha\Desktop\\ACP\Attendance_logs\\temp'):
                if filename.endswith('.txt'):
                        with open(os.path.join('C:\\Users\\megha\Desktop\\ACP\Attendance_logs\\temp', filename)) as f:
                                content = f.read()

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        log_dir = os.path.join(BASE_DIR, "Attendance_logs\\qr")
        for filename in os.listdir('C:\\Users\\megha\Desktop\\ACP\Attendance_logs\\qr'):
                if filename.endswith('.txt'):
                        with open(os.path.join('C:\\Users\\megha\Desktop\\ACP\Attendance_logs\\qr', filename)) as f2:
                                content2 = f2.read()
                                
        data = content.split("\n")
        qr_raw = content2.split("\n")
        list(qr_raw)
        #print(qr_raw)
        raw_data = set(data[4::])
        list(raw_data)
        raw_data.remove('')
        qr_raw.remove('')
        std_rec = dict([["Meghaj","11911130"],["Videhi","11911131"],["Kewal","11911132"],["Rohit","11911133"],["Asawari","11911134"],["Pranav","11911135"],["Bhavesh","11911136"],["Ishan","11911137"],["Rajabhau","11911138"],["Rambhau","11911139"]])
        #print(std_rec)
        std_list = ["Meghaj", "Videhi", "Kewal", "Rohit", "Asawari", "Pranav", "Bhavesh", "Ishan", "Rambhau", "Rajabhau"]
        std_list = set(std_list)
        for man in raw_data:
                if std_rec[man] in qr_raw:
                        prsnt_data.append(man)
                
        absent_list = list(std_list.difference(prsnt_data))
        absent_list.sort()
        f.close()
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(804, 637)
        MainWindow.setStyleSheet("background-color: rgb(0, 255, 127);\n"
"background-color: rgb(170, 255, 127);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 10, 801, 51))
        font = QtGui.QFont()
        font.setFamily("Tw Cen MT")
        font.setPointSize(17)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(30, 280, 741, 301))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.tableWidget.setFont(font)
        self.tableWidget.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.tableWidget.setGridStyle(QtCore.Qt.SolidLine)
        self.tableWidget.setRowCount(100)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(1)
        self.faculty = QtWidgets.QLabel(self.centralwidget)
        self.faculty.setGeometry(QtCore.QRect(100, 90, 261, 41))
        font = QtGui.QFont()
        font.setFamily("Rockwell")
        font.setPointSize(11)
        self.faculty.setFont(font)
        self.faculty.setStyleSheet("background-color: rgb(0, 170, 127);")
        self.faculty.setAlignment(QtCore.Qt.AlignCenter)
        self.faculty.setObjectName("faculty")
        self.divisin = QtWidgets.QLabel(self.centralwidget)
        self.divisin.setGeometry(QtCore.QRect(100, 150, 261, 41))
        font = QtGui.QFont()
        font.setFamily("Rockwell")
        font.setPointSize(11)
        self.divisin.setFont(font)
        self.divisin.setStyleSheet("background-color: rgb(0, 170, 127);")
        self.divisin.setAlignment(QtCore.Qt.AlignCenter)
        self.divisin.setObjectName("divisin")
        self.subject = QtWidgets.QLabel(self.centralwidget)
        self.subject.setGeometry(QtCore.QRect(100, 210, 261, 41))
        font = QtGui.QFont()
        font.setFamily("Rockwell")
        font.setPointSize(11)
        self.subject.setFont(font)
        self.subject.setStyleSheet("background-color: rgb(0, 170, 127);")
        self.subject.setAlignment(QtCore.Qt.AlignCenter)
        self.subject.setObjectName("subject")
        self.teacher = QtWidgets.QTextEdit(self.centralwidget)
        self.teacher.setGeometry(QtCore.QRect(450, 90, 261, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.teacher.setFont(font)
        self.teacher.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.teacher.setObjectName("teacher")
        self.classdiv = QtWidgets.QTextEdit(self.centralwidget)
        self.classdiv.setGeometry(QtCore.QRect(450, 150, 261, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.classdiv.setFont(font)
        self.classdiv.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.classdiv.setObjectName("classdiv")
        self.subj = QtWidgets.QTextEdit(self.centralwidget)
        self.subj.setGeometry(QtCore.QRect(450, 210, 261, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.subj.setFont(font)
        self.subj.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.subj.setObjectName("subj")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 804, 21))
        self.menubar.setObjectName("menubar")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuHelp.menuAction())
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.teacher.setText(data[0])
        self.subj.setText(data[2])
        self.classdiv.setText(data[1])
        numrows = len(absent_list)  
        numcols = 1
        for row in range(numrows):
                for column in range(numcols):
                        self.tableWidget.setItem(row, column, QtWidgets.QTableWidgetItem((absent_list[row])))
        shutil.rmtree("Attendance_logs")

        

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Attendance Report"))
        self.label.setText(_translate("MainWindow", "Attendance Report\n"
"List of Absentees:"))
        self.faculty.setText(_translate("MainWindow", "Name of Faculty:"))
        self.divisin.setText(_translate("MainWindow", "Division:"))
        self.subject.setText(_translate("MainWindow", "Subject:"))
        self.teacher.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:8.25pt;\"><br /></p></body></html>"))
        self.classdiv.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:8.25pt;\"><br /></p></body></html>"))
        self.subj.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:8.25pt;\"><br /></p></body></html>"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionAbout.setText(_translate("MainWindow", "About"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow1()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
