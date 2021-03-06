from PyQt5 import QtWidgets, uic, QtGui
import sys
import numpy as np
import cv2

class MyApp(QtWidgets.QDialog):

    def __init__(self):
        super(MyApp, self).__init__()
        uic.loadUi('qt_test2.ui',self)

        self.count = 0

        #버튼
        self.loadBtn = self.findChild(QtWidgets.QPushButton, 'loadBtn')
        self.loadBtn.clicked.connect(self.loadBtnClicked)
        self.procBtn = self.findChild(QtWidgets.QPushButton, 'procBtn')
        self.procBtn.clicked.connect(self.procBtnClicked)

        #QLineEdit
        self.filePath = self.findChild(QtWidgets.QLineEdit, 'filePath')
        self.filePath.clear()

        #QLabel : 이미지 창
        self.src = self.findChild(QtWidgets.QLabel, 'imgSrc')
        self.dst = self.findChild(QtWidgets.QLabel, 'imgDst')
        self.thr_value = self.findChild(QtWidgets.QLabel, 'label_threshold')

        self.hSlider = self.findChild(QtWidgets.QSlider, 'hSlider')
        self.hSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.hSlider.setMinimum(0)
        self.hSlider.setMaximum(255)
        self.hSlider.setTickInterval(10)
        self.hSlider.valueChanged.connect(self.hSliderChanged)

        self.show()


    def hSliderChanged(self):
        self.filePath.setText(str(self.hSlider.value()))
        self.thr_value.setText("임계값 : "+str(self.hSlider.value()))

    def loadBtnClicked(self):
        path = './image'
        filter = "All Images(*.jpg; *.png; *.bmp);;JPG (*.jpg);;PNG(*.png);;BMP(*.bmp)"
        fname = QtWidgets.QFileDialog.getOpenFileName(self, "파일불러오기", path, filter)
        self.filename = str(fname[0])
        self.filePath.setText(self.filename)
        self.src.setPixmap(QtGui.QPixmap(self.filename))
        self.src.setScaledContents(True)
        self.count += 1

    def imread(self, filename, flags=cv2.IMREAD_COLOR, dtype=np.uint8):
        try:
            n = np.fromfile(filename, dtype)
            img = cv2.imdecode(n, flags)
            return img
        
        except Exception as e:
            print(e)
            return None

    def displayOutputImage(self, outImage):
        img_info = outImage.shape
        if outImage.ndim == 2:
            qImg = QtGui.QImage(outImage, img_info[1], img_info[0], img_info[1]*1, QtGui.QImage.Format_Grayscale8)
        else:
            qImg = QtGui.QImage(outImage, img_info[1], img_info[0], img_info[1]*img_info[2], QtGui.QImage.Format_RGB888)

        pixmap = QtGui.QPixmap.fromImage(qImg)
        self.imgDst.setPixmap(pixmap)
        self.imgDst.setScaledContents(True)

    def processingImage(self, img_rgb, img_gray):
        lower_blue = (100, 20, 20)
        upper_blue = (130, 255, 255)

        dst = img_rgb.copy()
        hsv = cv2.cvtColor(dst, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        contours,_ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        c = max(contours, key=cv2.contourArea)

        mask = np.zeros_like(dst)

        cv2.drawContours(mask, [c], 0, (255, 255, 255), -1)

        gray2 = np.zeros_like(dst)
        gray2[:,:,0] = img_gray
        gray2[:,:,1] = img_gray
        gray2[:,:,2] = img_gray

        gray2 = cv2.bitwise_and(gray2, mask)
        mask_inv = cv2.bitwise_not(mask)
        dst = cv2.bitwise_and(dst, mask_inv)
        img_gray = cv2.bitwise_or(dst, gray2)
        outImg = img_gray
        return outImg

    def procBtnClicked(self):
        if self.count != 0:
            img = self.imread(self.filename)
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            #싱글채널 그래이 영상 저장
            # print(img_gray.shape)
            # cv2.imwrite('img_gray.jpg', img_gray)
            outImg = self.processingImage(img, img_gray)
            outImg = cv2.cvtColor(outImg, cv2.COLOR_RGB2BGR)
            self.displayOutputImage(outImg)
        else:
            self.filename = "파일을 먼저 로드하세요"
            self.filePath.setText(self.filename)

    

app = QtWidgets.QApplication(sys.argv)
window = MyApp()
app.exec_()