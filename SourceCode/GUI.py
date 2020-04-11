from AtndnsReprt import Ui_MainWindow1
from PyQt5 import QtCore, QtGui, QtWidgets
from tkinter import *
import numpy as np
import cv2
import pickle
import datetime
import os
from PIL import ImageTk,Image
import pyzbar.pyzbar as pyzbar

global staff
global sub
global div

def QR_read(image):
    qr = "00000000000000"
    f2 = open("Attendance_logs\\qr\\QR_present.txt", "a")
    decodedObjects = pyzbar.decode(image)
    for obj in decodedObjects:
        qr = (str(obj.data))[2:-1:]
        f2.write(qr+"\n")
    f2.close()

class Ui_MainWindow(object):

    def report(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow1()
        self.ui.setupUi(self.window)
        self.window.show()

    def train(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        image_dir = os.path.join(BASE_DIR, "Training-People")
        face_cascade = cv2.CascadeClassifier('Necessary_Data\Face_Cascade_Meghaj.xml')
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        current_id = 0
        label_ids = {}
        x_train = []
        y_labels = []
        for root, dirs, files in os.walk(image_dir):
                for file in files:
                        if file.endswith("png") or file.endswith("jpg") or file.endswith("jpeg"):
                                path = os.path.join(root, file)
                                #print(path)
                                #label = os.path.basename(root).replace(" ", "-").lower()
                                label = os.path.basename(root).replace(" ", "-")
                                if not label in label_ids:
                                        label_ids[label] = current_id
                                        current_id += 1
                                id_ = label_ids[label]
                                #print(label_ids)
                                #y_labels.append(label) # some number
                                #x_train.append(path) # verify this image, turn into a NUMPY arrray, GRAY
                                pil_image = Image.open(path).convert("L") # converts to grayscale
                                size = (550, 550)
                                final_image = pil_image.resize(size, Image.ANTIALIAS)
                                image_array = np.array(final_image, "uint8")
                                #print(image_array)
                                faces = face_cascade.detectMultiScale(image_array, scaleFactor=1.5, minNeighbors=5)
                                for (x,y,w,h) in faces:
                                        roi = image_array[y:y+h, x:x+w]
                                        x_train.append(roi)
                                        y_labels.append(id_)
        
        with open("Necessary_Data/face-labels.pickle", 'wb') as f:
	        pickle.dump(label_ids, f)
        recognizer.train(x_train, np.array(y_labels))
        recognizer.save("Necessary_Data/face-trainner.yml")


    def take_attendance(self):
            path = "Attendance_logs//temp"
            os.makedirs(path)
            path = "Attendance_logs//qr"
            os.makedirs(path)
            global staff
            global sub
            global div
            staff = self.textEdit.toPlainText()
            sub = str(self.comboBox.currentText())
            div = str(self.comboBox_2.currentText())
            self.textEdit.setText("")
            self.comboBox.setCurrentIndex(0)
            self.comboBox_2.setCurrentIndex(0)
            date_time = str(datetime.datetime.now())
            dr = str(datetime.datetime.now())[0:9]
            f = open("Attendance_logs"+"\\"+"temp\\"+div+"_"+sub+"_"+staff+"_"+dr+".txt", "a")
            f.write(staff+"\n")
            f.write(div+"\n")
            f.write(sub+"\n")
            f.write("Date and Time :"+date_time+"\n")
            f.close()
            face_cascade = cv2.CascadeClassifier('Necessary_Data\Face_Cascade_Meghaj.xml')
            recognizer = cv2.face.LBPHFaceRecognizer_create()
            recognizer.read("Necessary_Data/face-trainner.yml")
            labels = {"person_name": 1}
            with open("Necessary_Data/face-labels.pickle", 'rb') as f:
                    og_labels = pickle.load(f)
                    labels = {v:k for k,v in og_labels.items()}
            cap = cv2.VideoCapture(0)
            f = open("Attendance_logs"+"\\"+"temp\\"+div+"_"+sub+"_"+staff+"_"+dr+".txt", "a")
            while(True):
                # Capture frame-by-frame
                ret, frame = cap.read()
                QR_read(frame)
                gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
                for (x, y, w, h) in faces:
                    #print(x,y,w,h)
                    roi_gray = gray[y:y+h, x:x+w] #(ycord_start, ycord_end)
                    roi_color = frame[y:y+h, x:x+w]
                    id_, conf = recognizer.predict(roi_gray)
                    if conf>=80:
                            f.write(str(labels[id_])+"\n")
                            font = cv2.FONT_HERSHEY_SIMPLEX
                            name = labels[id_]
                            color = (255, 255, 255)
                            stroke = 2
                            cv2.putText(frame, name, (x,y), font, 1, color, stroke, cv2.LINE_AA)

                    img_item = "Necessary_Data/Compare_data.png"
                    cv2.imwrite(img_item, roi_color)
                    color = (255, 0, 0) #BGR 0-255 
                    stroke = 2
                    end_cord_x = x + w
                    end_cord_y = y + h
                    cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)
                    os.remove("Necessary_Data/Compare_data.png")

                cv2.imshow('frame',frame)
                if cv2.waitKey(20) & 0xFF == ord('q'):
                    f.close()
                    # When everything done, release the capture
                    cap.release()
                    cv2.destroyAllWindows()
                    break
    
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(773, 600)
        MainWindow.setStyleSheet("background-color: rgb(170, 255, 255);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(-14, 0, 851, 81))
        font = QtGui.QFont()
        font.setFamily("Sitka Heading")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("background-color: rgb(0, 170, 255);")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(-10, 531, 821, 20))
        self.label_2.setStyleSheet("background-color: rgb(170, 170, 255);")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(0, 510, 801, 21))
        self.label_3.setStyleSheet("background-color: rgb(0, 255, 255);")
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(430, 170, 281, 31))
        self.textEdit.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.textEdit.setObjectName("textEdit")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(60, 170, 281, 31))
        self.label_4.setStyleSheet("background-color: rgb(170, 170, 255);")
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(60, 240, 281, 31))
        self.label_5.setStyleSheet("background-color: rgb(170, 170, 255);")
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(60, 310, 281, 31))
        self.label_6.setStyleSheet("background-color: rgb(170, 170, 255);")
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(430, 240, 281, 31))
        self.comboBox.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox_2 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_2.setGeometry(QtCore.QRect(430, 310, 281, 31))
        self.comboBox_2.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(40, 390, 191, 41))
        self.pushButton.setStyleSheet("background-color: rgb(0, 255, 127);")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.train)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(290, 390, 191, 41))
        self.pushButton_2.setStyleSheet("background-color: rgb(0, 255, 127);")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.take_attendance)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(540, 390, 191, 41))
        self.pushButton_3.setStyleSheet("background-color: rgb(0, 255, 127);")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.report)
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(360, 50, 101, 20))
        font = QtGui.QFont()
        font.setFamily("Sitka Heading")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("background-color: rgb(0, 170, 255);")
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 773, 21))
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

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Face Recognition Attendance System"))
        self.label.setText(_translate("MainWindow", "Face Recognition Attendance System"))
        self.label_2.setText(_translate("MainWindow", "Project by: Meghaj Barhate, Kewal Barhate, Videhi Bavishi, Asawari Bapat, Rohit Barbhai."))
        self.label_3.setText(_translate("MainWindow", "Click on the Life-feed window named \'frame\' and press q to Exit Live Feed."))
        self.textEdit.setStatusTip(_translate("MainWindow", "Enter Name of Staff."))
        self.textEdit.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\';\"><br /></p></body></html>"))
        self.label_4.setText(_translate("MainWindow", "Enter Faculty Name :"))
        self.label_5.setText(_translate("MainWindow", "Select Subject:"))
        self.label_6.setText(_translate("MainWindow", "Select Division"))
        self.comboBox.setStatusTip(_translate("MainWindow", "Select Subject "))
        self.comboBox.setItemText(0, _translate("MainWindow", "*Select Subject*"))
        self.comboBox.setItemText(1, _translate("MainWindow", "Mathematics"))
        self.comboBox.setItemText(2, _translate("MainWindow", "Mathematics Tutorial"))
        self.comboBox.setItemText(3, _translate("MainWindow", "Mechatronics"))
        self.comboBox.setItemText(4, _translate("MainWindow", "Mechatronics Tutorial"))
        self.comboBox.setItemText(5, _translate("MainWindow", "Mechatronics Lab"))
        self.comboBox.setItemText(6, _translate("MainWindow", "Python Programming"))
        self.comboBox.setItemText(7, _translate("MainWindow", "Python Lab"))
        self.comboBox.setItemText(8, _translate("MainWindow", "SDP"))
        self.comboBox.setItemText(9, _translate("MainWindow", "Professional Development"))
        self.comboBox_2.setStatusTip(_translate("MainWindow", "Select division"))
        self.comboBox_2.setItemText(0, _translate("MainWindow", "*Select Division*"))
        self.comboBox_2.setItemText(1, _translate("MainWindow", "A"))
        self.comboBox_2.setItemText(2, _translate("MainWindow", "B"))
        self.comboBox_2.setItemText(3, _translate("MainWindow", "C"))
        self.comboBox_2.setItemText(4, _translate("MainWindow", "D"))
        self.comboBox_2.setItemText(5, _translate("MainWindow", "E"))
        self.comboBox_2.setItemText(6, _translate("MainWindow", "F"))
        self.comboBox_2.setItemText(7, _translate("MainWindow", "G"))
        self.comboBox_2.setItemText(8, _translate("MainWindow", "H"))
        self.comboBox_2.setItemText(9, _translate("MainWindow", "I"))
        self.comboBox_2.setItemText(10, _translate("MainWindow", "J"))
        self.comboBox_2.setItemText(11, _translate("MainWindow", "K"))
        self.comboBox_2.setItemText(12, _translate("MainWindow", "L"))
        self.comboBox_2.setItemText(13, _translate("MainWindow", "M"))
        self.comboBox_2.setItemText(14, _translate("MainWindow", "N"))
        self.comboBox_2.setItemText(15, _translate("MainWindow", "O"))
        self.comboBox_2.setItemText(16, _translate("MainWindow", "P"))
        self.comboBox_2.setItemText(17, _translate("MainWindow", "Q"))
        self.comboBox_2.setItemText(18, _translate("MainWindow", "R"))
        self.comboBox_2.setItemText(19, _translate("MainWindow", "S"))
        self.comboBox_2.setItemText(20, _translate("MainWindow", "T"))
        self.pushButton.setStatusTip(_translate("MainWindow", "Trains face recognizer for new students."))
        self.pushButton.setText(_translate("MainWindow", "Train Recognizer"))
        self.pushButton_2.setStatusTip(_translate("MainWindow", "Starts the life feed face recognition."))
        self.pushButton_2.setText(_translate("MainWindow", "Take Attendance"))
        self.pushButton_3.setStatusTip(_translate("MainWindow", "Generates a dialogue box containing names of Absent Students."))
        self.pushButton_3.setText(_translate("MainWindow", "Generate Report"))
        self.label_7.setText(_translate("MainWindow", "v1.0.0"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionAbout.setText(_translate("MainWindow", "About"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


















'''
ikde for loop ahe
self.tableWidget.setItem()
'''