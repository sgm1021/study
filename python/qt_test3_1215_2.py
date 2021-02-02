import sys
from PyQt5 import QtWidgets, uic, QtGui
import cv2
import numpy as np
from win32api import GetSystemMetrics

class MyApp(QtWidgets.QDialog):

    def __init__(self):
        super(MyApp, self).__init__()
        uic.loadUi('qt_test3_1215_2.ui',self)
        self.initUI()
    
    def initUI(self):
        self.count = 0
        self.filename=''
        self.threshold_option = 0
        #버튼
        self.loadBtn = self.findChild(QtWidgets.QPushButton,'loadBtn')
        self.loadBtn.clicked.connect(self.loadBtnClicked)
        self.procBtn = self.findChild(QtWidgets.QPushButton,'procBtn')
        self.procBtn.clicked.connect(self.procBtnClicked)
        self.circleBtn = self.findChild(QtWidgets.QPushButton,'circleBtn')
        self.circleBtn.clicked.connect(self.circleBtnClicked)

        self.src = self.findChild(QtWidgets.QLabel,'imgSrc')     
        self.src.setPixmap(QtGui.QPixmap("image/2.jpg"))
        self.src.setScaledContents(True)
        self.dst = self.findChild(QtWidgets.QLabel,'imgDst')     
        self.filePath = self.findChild(QtWidgets.QLineEdit,'filePath')
        self.filePath.clear()

        #QComboBox
        self.comboThr = self.findChild(QtWidgets.QComboBox, 'comboThr')
                
        # # 이진화 옵션번호가 0~5 OTSU가 8 TRIANGLE이16인 이유는 여러개를 같이 쓸수 있으므로.
        # # 숫자를 더해서 같은 값이 나오면 안된다.
        self.thrList = ["BINARY",
                    "BINARY_INV",
                    "TRUNC",
                    "TOZERO",
                    "TOZERO_INV",
                    "MASK",
                    "OTSU",
                    "TRIANGLE",
                    "ADAPTIVE_MEAN",
                    "ADAPTIVE_GAUSSIAN"]
        
        self.modelist = [cv2.THRESH_BINARY,
                         cv2.THRESH_BINARY_INV,
                         cv2.THRESH_TRUNC,
                         cv2.THRESH_TOZERO,
                         cv2.THRESH_TOZERO_INV,
                         cv2.THRESH_MASK,
                         cv2.THRESH_OTSU,
                         cv2.THRESH_TRIANGLE,
                         cv2.ADAPTIVE_THRESH_MEAN_C,
                         cv2.ADAPTIVE_THRESH_GAUSSIAN_C]

        self.comboThr.addItems(self.thrList) 
        self.comboThr.activated[str].connect(self.ComboBoxEvent)  

        #QLabel
        self.thr_value = self.findChild(QtWidgets.QLabel, 'label_threshold')
        
        #QSlider
        self.hSlider = self.findChild(QtWidgets.QSlider, 'hSlider')
        self.hSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.hSlider.setMinimum(0)
        self.hSlider.setMaximum(255)
        self.hSlider.setTickInterval(10)
        self.hSlider.valueChanged.connect(self.hSliderChanged)
        self.show()
    
    def ComboBoxEvent(self, text):
        index = self.thrList.index(text)
        self.threshold_option = self.modelist[index]
        self.hSliderChanged()
        # self.filePath.adjustSize()

    def hSliderChanged(self):
        # self.filePath.setText(str(self.hSlider.value()))
        if self.filename !='':
            self.thr_value.setText("임계값 : "+str(self.hSlider.value()))
            img_gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
            _, binary = cv2.threshold(img_gray, self.hSlider.value(), 255, self.threshold_option)
            self.displayOutputImage(binary, 'dst')
        else :
            self.filePath.setText("예외발생 : 파일을 선택해 주세요!!!!") 
   
    
    # 이미지 로드(Image load)
    def loadBtnClicked(self):
        path = './04_top'
        filter = "All Images(*.jpg; *.png; *.bmp);;JPG (*.jpg);;PNG(*.png);;BMP(*.bmp)"
        fname = QtWidgets.QFileDialog.getOpenFileName(self, "파일 불러오기", path, filter)
        self.filename = str(fname[0])
        if self.filename != '' : # 파일로드시 파일 선택하지 않고 취소할 때 예외처리
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
            
            # opencv imshow
            out_bgr = cv2.cvtColor(outImg, cv2.COLOR_RGB2BGR)
            out_bgr = self.FitToWindowSize(out_bgr)
            cv2.imshow("src", out_bgr)
        else:
            self.filename = "파일을 로드 하세요"
            self.filePath.setText(self.filename)
        
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def circleBtnClicked(self):
        if self.count != 0:
            # img = self.imread(self.filename) #opencv는 한글 지원 안함
            img_rgb = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
            # img_bgr = self.img.copy()
            img_gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
            outImg = self.findCircle(img_rgb, img_gray)
            self.displayOutputImage(outImg,'dst')
            
            # opencv imshow
            out_bgr = cv2.cvtColor(outImg, cv2.COLOR_RGB2BGR)
            out_bgr = self.FitToWindowSize(out_bgr)
            cv2.imshow("src", out_bgr)
        else:
            self.filename = "파일을 로드 하세요"
            self.filePath.setText(self.filename)
        
        cv2.waitKey(0)
        cv2.destroyAllWindows()

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
        # 작성할 코드 
        # 결과를 그릴 이미지(컬러) 복사
        outImg = img_rgb.copy()
        
        #이진화
        _, binary = cv2.threshold(img_gray, 172, 255, cv2.THRESH_BINARY)

        # 만약 추출된 영상이 검은색이라면 반전이 필요함 / 흰색이면 필요없음
        # binary = cv2.bitwise_not(binary) #이미지 반전 흑 <---> 백

        #모폴로지 변환
        kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (9, 9))
        binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=1)

        #OPENCV binary 화면 출력
        binary2 = binary.copy()
        binary2 = self.FitToWindowSize(binary2) #화면크기에 영상 맞추기
        cv2.imshow('binary',binary2)
        
        #Contour 찾기
        contours,_ = cv2.findContours(binary, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)

        #찾은 Contour개수만큼 반복하여 그리기
        for i in range(len(contours)):
            
            # Contour 면적구하기
            area = cv2.contourArea(contours[i])
            if area > 200 :
                M = cv2.moments(contours[i])
                cX = int(M['m10'] / M['m00'] + 1e-5)
                cY = int(M['m01'] / M['m00'] + 1e-5)
                # Contour 그리기
                cv2.drawContours(outImg, [contours[i]], 0, (0,255, 0), 2)
                # Contour 면적 화면에 표시하기(putText)
                column = contours[i][0][0][0] #가로 좌표(x)
                row = contours[i][0][0][1]    #세로 좌표(y)
                # cv2.putText(outImg, str(area), tuple(contours[i][0][0]), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 0), 1)
                cv2.putText(outImg, str(area), (column-20, row-20), cv2.FONT_HERSHEY_COMPLEX, 1.0, (255, 0, 0), 1)
                cv2.circle(outImg, (cX, cY), 3, (255, 0, 0), -1)
        #결과 이미지 리턴
        return outImg
    
    def findCircle(self, img_rgb, img_gray):
        # 작성할 코드 
        # 결과를 그릴 이미지(컬러) 복사
        outImg = img_rgb.copy()
        
        circles = cv2.HoughCircles(img_gray, cv2.HOUGH_GRADIENT, 1, 200, param1 = 250, param2 = 50, minRadius = 250, maxRadius = 290) 
        for i in circles[0]:
            cv2.circle(outImg, (i[0], i[1]), i[2], (0, 255, 0), 5)
        return outImg

    # OPENCV 화면 출력 관련 함수 : 화면크기에 맞춰 이미지 출력
    def FitToWindowSize(self, image):
        image_resized = image.copy()
        #윈도우 크기 얻기
        # print('image {}'.format(image.shape))
        win_w=GetSystemMetrics(0)
        win_h=GetSystemMetrics(1)
        img_h, img_w = image.shape[:2]

        if(img_h > win_h or img_w > win_w):   
            rate_width =  (win_w / img_w)*0.95
            rate_height =  (win_h / img_h)*0.95
            scale = rate_width if (rate_width < rate_height) else rate_height
            image_resized = cv2.resize(image, dsize=(0, 0), fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)
        # cv2.imshow('image_resize',image_resized)
        return image_resized


app = QtWidgets.QApplication(sys.argv)
window = MyApp()
app.exec_()