import sys
from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QSlider
import cv2
import numpy as np

class MyApp(QtWidgets.QDialog):
    def __init__(self):
        super(MyApp, self).__init__()
        uic.loadUi('qt_test4_1.ui', self)

        self.filename = ''
        self.count = 0
        self.threshold_option = 0

        self.loadBtn = self.findChild(QtWidgets.QPushButton,'loadBtn')
        self.loadBtn.clicked.connect(self.loadBtnClicked)
        self.procBtn = self.findChild(QtWidgets.QPushButton,'procBtn')
        self.procBtn.clicked.connect(self.procBtnClicked)
        self.src = self.findChild(QtWidgets.QLabel,'imgSrc')     
        self.thr = self.findChild(QtWidgets.QLabel,'imgThr') 
        self.dst = self.findChild(QtWidgets.QLabel,'imgDst') 
        self.filePath = self.findChild(QtWidgets.QLineEdit,'filePath')
        self.filePath.clear()

        self.comboThr = self.findChild(QtWidgets.QComboBox, 'comboBox')
        self.thrList = ["THRESH_BINARY : 0",
                    "THRESH_BINARY_INV : 1",
                    "THRESH_TRUNC : 2",
                    "THRESH_TOZERO : 3",
                    "THRESH_TOZERO_INV : 4",
                    "THRESH_MASK : 5",
                    "THRESH_OTSU : 8",
                    "THRESH_TRIANGLE : 16"]
        self.comboThr.addItems(self.thrList)
        self.comboThr.activated[str].connect(self.comboBoxEvent)

        self.thr_value = self.findChild(QtWidgets.QLabel, 'label_threshold')

        self.hSlider = self.findChild(QtWidgets.QSlider, 'hSlider')
        self.hSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.hSlider.setMinimum(0)
        self.hSlider.setMaximum(255)
        self.hSlider.setTickInterval(10)
        self.hSlider.valueChanged.connect(self.hSliderChanged)

        self.show()

    def comboBoxEvent(self, text):
        self.threshold_option = self.thrList.index(text)
        if self.threshold_option == 6:
            self.threshold_option = 8
        elif self.threshold_option == 7:
            self.threshold_option = 16
        self.hSliderChanged()
    
    def hSliderChanged(self):
        if self.filename !='':
            self.thr_value.setText("임계값 : "+str(self.hSlider.value()))
            img_gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
            _, binary = cv2.threshold(img_gray, self.hSlider.value(), 255, 0)
            self.displayOutputImage(binary, 'thr')
        else :
            self.filePath.setText("예외발생 : 파일을 선택해 주세요!!!!") 

    def loadBtnClicked(self):
        path = './image'
        filter = "All Images(*.jpg; *.png; *.bmp);;JPG (*.jpg);;PNG(*.png);;BMP(*.bmp)"
        fname = QFileDialog.getOpenFileName(self, "파일 불러오기", path, filter)
        self.filename = str(fname[0])
        if fname[0] != '':
            filename = str(fname[0])
            self.filePath.setText(filename)
            self.img = self.imread(filename)
            img_rgb = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
            self.displayOutputImage(img_rgb, 'src')
            self.count +=1
        else:
            self.filePath.setText("파일 선택")

    def procBtnClicked(self):
        if self.count != 0:
            img_rgb = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
            img_gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
            outImg = self.processingImageThr(img_rgb, img_gray)
            self.displayOutputImage(outImg,'thr')
            outImg = self.processingImageDst(img_rgb, img_gray)
            self.displayOutputImage(outImg,'dst')
        else:
            self.filename = "파일을 로드 하세요"
            self.filePath.setText(self.filename)

    
    def displayOutputImage(self, outImage, position):
        img_info = outImage.shape
        if outImage.ndim == 2:
            qImg = QtGui.QImage(outImage, img_info[1], img_info[0], 
                        img_info[1]*1, QtGui.QImage.Format_Grayscale8)
        else :
            qImg = QtGui.QImage(outImage, img_info[1], img_info[0], 
                        img_info[1]*img_info[2], QtGui.QImage.Format_RGB888)
        
        pixmap = QtGui.QPixmap.fromImage(qImg)

        if position == 'src' :
            self.src.setPixmap(pixmap)
            self.src.setScaledContents(True)
        elif position == 'thr' :
            self.thr.setPixmap(pixmap)
            self.thr.setScaledContents(True)
        else:
            self.dst.setPixmap(pixmap)
            self.dst.setScaledContents(True)
    
    def imread(self, filename, flags=cv2.IMREAD_COLOR, dtype=np.uint8):
        try:
            n = np.fromfile(filename, dtype)
            img = cv2.imdecode(n, flags)
            return img
        except Exception as e:
            print(e)
            return None

    def processingImageThr(self, img_rgb, img_gray):
        #여기에 여러분이 작성할 코드를 넣으시면 됩니다.
        outImg = img_gray
        return outImg
    
    def processingImageDst(self, img_rgb, img_gray):
        #여기에 여러분이 작성할 코드를 넣으시면 됩니다.
        img_rgb = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
        lower_blue = (100, 20, 20)
        upper_blue = (130, 255, 255)

        dst = img_rgb.copy()
        hsv = cv2.cvtColor(dst, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        contours,_ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        c = max(contours, key=cv2.contourArea)
        mask = np.zeros_like(dst)
        cv2.drawContours(mask, [c], 0, (255, 255, 255), -1)
        gray2 = cv2.merge((img_gray, img_gray, img_gray))
        gray2 = cv2.bitwise_and(gray2, mask)
        dst = np.where(gray2 != 0, gray2, dst)
        dst = cv2.cvtColor(dst, cv2.COLOR_BGR2RGB)
        outImg = dst
        return outImg

app = QtWidgets.QApplication(sys.argv)
window = MyApp()
app.exec_()