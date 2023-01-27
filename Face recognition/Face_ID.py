from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QMainWindow
from PyQt5.QtGui import QPixmap
import sys
import cv2
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from PyQt5 import QtWidgets

import time
import os
from os import listdir
from os.path import isfile, join

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load the face classifier from OpenCV
face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


# Collecting train images
class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)
    def __init__(self):
        super().__init__()
        self._run_flag = True
        
    def face_extractor(self, img):
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) 
        faces = face_classifier.detectMultiScale(gray,1.3,5) 
        if faces is(): 
            return None 
        for(x,y,w,h) in faces: 
            cropped_face = img[y:y+h, x:x+w]
        return cropped_face
    
    def draw_rectangular_box(self, img):
        # cv_image + a box drawing
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray,1.3,5)
        for(x,y,w,h) in faces:
            cv2.rectangle(img, (x,y),(x+w,y+h),(255,0,0),2)
        return img   
    
    def visual_effect(self, img):
        # cv_image + a box drawing
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray,1.3,5)
        for(x,y,w,h) in faces:
            cv2.rectangle(img, (x,y),(x+w,y+h),(0,0,255),4)
        return img
    
    def get_files_count(self, folder_path):
    	dirListing = os.listdir(folder_path)
    	return len(dirListing)    

    def run(self):
        # capture from web cam
        self._run_flag = True
        self.cap = cv2.VideoCapture(0)
        count = 0     
        
        while self._run_flag:
            ret, cv_img = self.cap.read()     
            count+=1
            #color = (0,255,255)
            if self.face_extractor(cv_img) is not None:
                # add a rectangular box showing a face: new "cv_img" is needed with a rectangular box.
                self.draw_rectangular_box(cv_img)
                
                if count % 10 == 0:
                    # visual effect 
                    time.sleep(1)
                    self.visual_effect(cv_img)
                    time.sleep(1)                    
                    # take a picture
                    try:
                        face = cv2.resize(self.face_extractor(cv_img),(200,200))
                    except Exception as e:
                        print(str(e))
                    face_gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                    file_name_path = './dataset/data_'+str(count)+'.jpg'
                    cv2.imwrite(file_name_path,face_gray)
                    print("save a image")
                    pass                
                
                # running a video
                self.change_pixmap_signal.emit(cv_img)                
            else: 
                print("Face not Found") 
                pass
            
            if cv2.waitKey(1)==13 or self.get_files_count("./dataset/")==3:
                # stop a video running
                self._run_flag = False
                pass
        # shut down capture system
        self.cap.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False

        
# Unlock        
class VideoThread_unlock(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True
    
    def face_detector(self, img, size = 0.5):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray,1.3,5) 
        if faces is():
            return img,[]
        for(x,y,w,h) in faces:
            cv2.rectangle(img, (x,y),(x+w,y+h),(0,255,255),2)
            roi = img[y:y+h, x:x+w]
            roi = cv2.resize(roi, (200,200))
        return img,roi

    def run(self):
        # capture from web cam
        self._run_flag = True
        self.cap = cv2.VideoCapture(0)
        model = MyWindow.ClickStartTrain(self)
        
        while self._run_flag:
            ret, cv_img = self.cap.read()     
            if self.face_detector(cv_img) is not None:         
                # running a video
                self.change_pixmap_signal.emit(cv_img)
                # identification
                image, face = self.face_detector(cv_img)                                     

                try:
                    face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                    result = model.predict(face)
                    print(result[1])                                        
                    if result[1] < 500:
                        confidence = int(100*(1-(result[1])/300))
                        display_string = str(confidence)+'% Confidence it is user'
                        print(display_string)
                        cv2.putText(image,display_string,(100,120), cv2.FONT_HERSHEY_COMPLEX,1,(250,120,255),2)              
                    if confidence > 75:
                        print("Unlocked")
                        cv2.putText(image, "Unlocked", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)       
                    else:
                        cv2.putText(image, "Locked", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)      
                        print("Locked")
                except:
                    cv2.putText(image, "Face Not Found", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
                    print("Error")
                    pass                                                 
            else: 
                print("Face not Found") 
                pass
        # shut down capture system
        self.cap.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        

# GUI
class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.available_cameras = QCameraInfo.availableCameras()  # Getting available cameras
        cent = QDesktopWidget().availableGeometry().center()  # Finds the center of the screen
        self.setStyleSheet("background-color: white;")
        self.resize(1400, 800)
        self.frameGeometry().moveCenter(cent)
        self.setWindowTitle('Face ID')
        self.initWindow()
        
    def initWindow(self):        
        # create the video capture thread
        self.thread = VideoThread()
        self.thread_unlock = VideoThread_unlock()

        # Label with the name of the co-founders
        self.label = QtWidgets.QLabel(self)  # Create label
        self.label.move(30, 550)  # Allocate label in window
        self.label.resize(300, 20)  # Set size for the label
        self.label.setAlignment(Qt.AlignCenter)  # Align text in the label

        # Button to start video
        self.ss_video = QtWidgets.QPushButton(self)
        self.ss_video.setText('Start')
        self.ss_video.move(769, 100)
        self.ss_video.resize(300, 100)
        self.ss_video.clicked.connect(self.ClickStartVideo)
        
        # Button for train iamges
        self.btn_train = QtWidgets.QPushButton(self)
        self.btn_train.setText('Train')
        self.btn_train.move(769, 250)
        self.btn_train.resize(300, 100)
        self.btn_train.clicked.connect(self.ClickStartTrain)
        
        # Button to unlock
        self.btn_unlock = QtWidgets.QPushButton(self)
        self.btn_unlock.setText('Unlock')
        self.btn_unlock.move(769, 400)
        self.btn_unlock.resize(300, 100)
        self.btn_unlock.clicked.connect(self.ClickUnlock)

        # Status bar
        self.status = QStatusBar()
        self.status.setStyleSheet("background : lightblue;")  # Setting style sheet to the status bar
        self.setStatusBar(self.status)  # Adding status bar to the main window
        self.status.showMessage('Ready to start')
        self.image_label = QLabel(self)
        self.disply_width = 669
        self.display_height = 501
        self.image_label.resize(self.disply_width, self.display_height)
        self.image_label.setStyleSheet("background : black;")
        self.image_label.move(0, 0)
    
    # Activate when unlock button is clicked (btn_unlock)
    def ClickUnlock(self):
        # Change label color to light blue
        self.btn_unlock.clicked.disconnect(self.ClickUnlock)
        self.status.showMessage('Video Running...')
        
        # Change button to stop
        self.btn_unlock.setText('Unlocking')
        self.thread = VideoThread_unlock()
        self.thread.change_pixmap_signal.connect(self.update_image)

        # start the thread
        self.thread.start()
        self.btn_unlock.clicked.connect(self.thread.stop)
        self.btn_unlock.clicked.connect(self.ClickStopVideo_unlock)
        
    def ClickStopVideo_unlock(self):
        self.thread.change_pixmap_signal.disconnect()
        self.btn_unlock.setText('Start video')
        self.status.showMessage('Ready to unlock')
        self.btn_unlock.clicked.disconnect(self.ClickStopVideo_unlock)
        self.btn_unlock.clicked.disconnect(self.thread.stop)
        self.btn_unlock.clicked.connect(self.ClickUnlock)
        
    # Activate when Train button is clicked
    def ClickStartTrain(self):
        data_path = './dataset/'
        onlyfiles = [f for f in listdir(data_path) if isfile(join(data_path,f))]
        Training_Data, Labels = [], []
        for i, files in enumerate(onlyfiles):    
            image_path = data_path + onlyfiles[i]
            images = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            if images is None:
                continue    
            Training_Data.append(np.asarray(images, dtype=np.uint8))
            Labels.append(i)
        if len(Labels) == 0:
            print("There is no data to train.")
            exit()
        Labels = np.asarray(Labels, dtype=np.int32)
        model = cv2.face.LBPHFaceRecognizer_create()
        model.train(np.asarray(Training_Data), np.asarray(Labels))
        print("Model Training Complete!!!!!")
        return model
        
    # Activates when Start/Stop video button is clicked to Start (ss_video)
    def ClickStartVideo(self):
        # Change label color to light blue
        self.ss_video.clicked.disconnect(self.ClickStartVideo)
        self.status.showMessage('Video Running...')
        
        # Change button to stop
        self.ss_video.setText('Stop')
        self.thread = VideoThread()
        self.thread.change_pixmap_signal.connect(self.update_image)

        # start the thread
        self.thread.start()
        self.ss_video.clicked.connect(self.thread.stop)  # Stop the video if button clicked
        self.ss_video.clicked.connect(self.ClickStopVideo)

    # Activates when Start/Stop video button is clicked to Stop (ss_video)
    def ClickStopVideo(self):
        self.thread.change_pixmap_signal.disconnect()
        self.ss_video.setText('Start video')
        self.status.showMessage('Ready to start')
        self.ss_video.clicked.disconnect(self.ClickStopVideo)
        self.ss_video.clicked.disconnect(self.thread.stop)
        self.ss_video.clicked.connect(self.ClickStartVideo)
        
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)
        #p = convert_to_Qt_format.scaled(801, 801, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec())