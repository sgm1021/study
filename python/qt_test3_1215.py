import sys
from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QSlider


import cv2
import numpy as np

class MyApp(QtWidgets.QDialog):

    def __init__(self):
        super(MyApp, self).__init__()
        uic.loadUi('qt_test3_1215.ui',self)

        self.count = 0
        self.filename = ''
        self.threshold_option = 0
        #버튼
        self.loadBtn = self.findChild(QtWidgets.QPushButton,'loadBtn')
        self.loadBtn.clicked.connect(self.loadBtnClicked)
        self.procBtn = self.findChild(QtWidgets.QPushButton,'procBtn')
        self.procBtn.clicked.connect(self.procBtnClicked)

        self.src = self.findChild(QtWidgets.QLabel,'imgSrc')     
        self.src.setPixmap(QtGui.QPixmap("image/1.jpg"))
        self.src.setScaledContents(True)
        self.dst = self.findChild(QtWidgets.QLabel,'imgDst')     
        self.filePath = self.findChild(QtWidgets.QLineEdit,'filePath')
        self.filePath.clear()

        self.comboThr = self.findChild(QtWidgets.QComboBox, 'comboThr')
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
            _, binary = cv2.threshold(img_gray, self.hSlider.value(), 255, self.threshold_option)
            self.displayOutputImage(binary, 'dst')
        else :
            self.filePath.setText("예외발생 : 파일을 선택해 주세요!!!!") 

   
    
    # 이미지 로드(Image load)
    def loadBtnClicked(self):
        path = './02_PCB_Image2/PCB2/good'
        filter = "All Images(*.jpg; *.png; *.bmp);;JPG (*.jpg);;PNG(*.png);;BMP(*.bmp)"
        fname = QFileDialog.getOpenFileName(self, "파일 불러오기", path, filter)
        self.filename = str(fname[0])
        if fname[0] !='' : # 파일로드시 파일 선택하지 않고 취소할 때 예외처리
            filename = str(fname[0])
            self.filePath.setText(filename)
            self.img = self.imread(filename) #cv2.imread가 한글경로를 지원하지 않음
            img_rgb = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
            self.displayOutputImage(img_rgb, 'src') # 'src'(왼쪽) or 'dst'(오른쪽) 창
            self.count += 1
        else :
            self.filePath.setText("예외발생 : 파일을 선택해 주세요!!!!") 

    def procBtnClicked(self):
        if self.count != 0:
            # img = self.imread(self.filename) #opencv는 한글 지원 안함
            img_rgb = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
            # img_bgr = self.img.copy()
            img_gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
            outImg = self.processingImage(img_rgb, img_gray)
            self.displayOutputImage(outImg,'dst')
        else:
            self.filename = "파일을 로드 하세요"
            self.filePath.setText(self.filename)

    # 결과이미지 출력
    def displayOutputImage(self, outImage, position):
        img_info = outImage.shape
        if outImage.ndim == 2 : # 그래이 영상
            qImg = QtGui.QImage(outImage, img_info[1], img_info[0], 
                            img_info[1]*1, QtGui.QImage.Format_Grayscale8)
        else :
            qImg = QtGui.QImage(outImage, img_info[1], img_info[0], 
                            img_info[1]*img_info[2], QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(qImg)
            
        if position == 'src' :
            self.src.setPixmap(pixmap)
            self.src.setScaledContents(True)
        else :
            self.dst.setPixmap(pixmap)
            self.dst.setScaledContents(True)


    #한글 포함된 이미지 파일 읽어오기
    def imread(self, filename, flags=cv2.IMREAD_COLOR, dtype=np.uint8):
        try:
            n = np.fromfile(filename, dtype)
            img = cv2.imdecode(n, flags)
            return img
        except Exception as e:
            print(e)
            return None

    def processingImage(self, img_rgb, img_gray):
        #여기에 여러분이 작성할 코드를 넣으시면 됩니다.
        outImg = img_gray
        return outImg



app = QtWidgets.QApplication(sys.argv)
window = MyApp()
app.exec_()