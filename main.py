################################################################################
##
## BY: WANDERSON M.PIMENTA
## PROJECT MADE WITH: Qt Designer and PySide2
## V: 1.0.0
##
## This project can be used freely for all uses, as long as they maintain the
## respective credits only in the Python scripts, any information in the visual
## interface (GUI) can be modified without any implication.
##
## There are limitations on Qt licenses if you want to use your products
## commercially, I recommend reading them on the official website:
## https://doc.qt.io/qtforpython/licenses.html
##
################################################################################

import sys, os
import platform
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import (Signal, QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PySide2.QtWidgets import *

# GUI FILE
from app_modules import *

file_list = []
file_sender = []
DIR = ''

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        ## PRINT ==> SYSTEM
        print('System: ' + platform.system())
        print('Version: ' + platform.release())

        ########################################################################
        ## START - WINDOW ATTRIBUTES
        ########################################################################

        ## REMOVE ==> STANDARD TITLE BAR
        UIFunctions.removeTitleBar(True)
        ## ==> END ##

        ## SET ==> WINDOW TITLE
        self.setWindowTitle('Bushin AI')
        UIFunctions.labelTitle(self, 'Bushin AI')
        UIFunctions.labelDescription(self, 'Get the raw data.')
        ## ==> END ##

        ## WINDOW SIZE ==> DEFAULT SIZE
        startSize = QSize(1000, 720)
        self.resize(startSize)
        self.setMinimumSize(startSize)
        # UIFunctions.enableMaximumSize(self, 500, 720)
        ## ==> END ##

        ## ==> CREATE MENUS
        ########################################################################

        ## ==> TOGGLE MENU SIZE
        self.ui.btn_toggle_menu.clicked.connect(lambda: UIFunctions.toggleMenu(self, 175, True))
        ## ==> END ##

        ## ==> ADD CUSTOM MENUS
        self.ui.stackedWidget.setMinimumWidth(20)
        UIFunctions.addNewMenu(self, "이미지 수집", "btn_raw_data", "url(:/16x16/icons/16x16/cil-library-add.png)", True)
        UIFunctions.addNewMenu(self, "이미지 분석", "btn_learning", "url(:/16x16/icons/16x16/cil-laptop.png)", True)
        UIFunctions.addNewMenu(self, "데이터 관리", "btn_result", "url(:/16x16/icons/16x16/cil-find-in-page.png)", True)
        UIFunctions.addNewMenu(self, "Setting", "btn_setting", "url(:/16x16/icons/16x16/cil-settings.png)", False)
        # UIFunctions.addNewMenu(self, "Custom Widgets", "btn_widgets", "url(:/16x16/icons/16x16/cil-equalizer.png)", False)
        ## ==> END ##

        # START MENU => SELECTION
        UIFunctions.selectStandardMenu(self, "btn_raw_data")
        ## ==> END ##

        ## ==> START PAGE
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_collection)
        ## ==> END ##

        ## USER ICON ==> SHOW HIDE
        UIFunctions.userIcon(self, "EZ", "", True)
        ## ==> END ##


        ## ==> MOVE WINDOW / MAXIMIZE / RESTORE
        ########################################################################
        def moveWindow(event):
            # IF MAXIMIZED CHANGE TO NORMAL
            if UIFunctions.returStatus() == 1:
                UIFunctions.maximize_restore(self)

            # MOVE WINDOW
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()

        # WIDGET TO MOVE
        self.ui.frame_label_top_btns.mouseMoveEvent = moveWindow
        ## ==> END ##

        ## ==> LOAD DEFINITIONS
        ########################################################################
        UIFunctions.uiDefinitions(self)
        ## ==> END ##

        ########################################################################
        ## END - WINDOW ATTRIBUTES
        ############################## ---/--/--- ##############################




        ########################################################################
        #                                                                      #
        ## START -------------- WIDGETS FUNCTIONS/PARAMETERS ---------------- ##
        #                                                                      #
        ## ==> USER CODES BELLOW                                              ##
        ########################################################################



        ## ==> QTableWidget RARAMETERS
        ########################################################################
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        ## ==> END ##



        ########################################################################
        #                                                                      #
        ## END --------------- WIDGETS FUNCTIONS/PARAMETERS ----------------- ##
        #                                                                      #
        ############################## ---/--/--- ##############################


        ## SHOW ==> MAIN WINDOW
        ########################################################################
        self.show()
        ## ==> END ##


        # 이미지 수집
        self.ui.btn_cam1.setCheckable(True)
        self.ui.btn_cam1.clicked.connect(self.toggle_btn_cam1)
        self.ui.btn_cam2.setCheckable(True)
        self.ui.btn_cam2.clicked.connect(self.toggle_btn_cam2)
        self.ui.btn_cam3.setCheckable(True)
        self.ui.btn_cam3.clicked.connect(self.toggle_btn_cam3)

        self.ui.btn_test.clicked.connect(self.btn_test)
        self.ui.btn_scan.clicked.connect(self.btn_scan)

        # 이미지 분석
        self.label_ = []
        self.ui.comboBox_2.currentIndexChanged.connect(self.onComboBox_2)
        self.onComboBox_2(0)      # 초기 기본 셋팅: 3열

        # 데이터 관리
        self.pixmap = QPixmap("On.png")
        self.ui.textile_image.setPixmap(self.pixmap)
        self.ui.textile_image.setScaledContents(True)

        self.pixmap = QPixmap("Off.png")
        self.ui.mask_image.setPixmap(self.pixmap)
        self.ui.mask_image.setScaledContents(True)


    # 이미지 수집
    def toggle_btn_cam1(self, state):
        if state == True:
            print("btn_cam1: On")
        else:
            print("btn_cam1: Off")

    def toggle_btn_cam2(self, state):
        if state == True:
            print("btn_cam2: On")
        else:
            print("btn_cam2: Off")

    def toggle_btn_cam3(self, state):
        if state == True:
            print("btn_cam3: On")
        else:
            print("btn_cam3: Off")

    def btn_test(self):
        print("btn_test: pressed")
        self.pixmap = QPixmap("On.png")
        self.ui.label_scan_image.setPixmap(self.pixmap)
        self.ui.label_scan_image.setScaledContents(True)

    def btn_scan(self):
        print("btn_scan: pressed")
        self.pixmap = QPixmap("Off.png")
        self.ui.label_scan_image.setPixmap(self.pixmap)
        self.ui.label_scan_image.setScaledContents(True)

    # 이미지 분석
    def onComboBox_2(self, index):
        # 폴더에 있는 파일 리스트를 불러옴
        global DIR
        global file_list
        global file_sender
        file_sender.clear()

        DIR = './icons/24x24'   # 파일 있는 경로
        file_list = [name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))]
        # file_list = os.listdir(folder_name)

        # div = 행의 개수
        if len(file_list) // (index+3) == 0:        # int(파일 개수 / 열)
            div = 1
        elif len(file_list) % (index+3) == 0:       # 파일 개수를 열로 나눈 나머지
            div = len(file_list) // (index+3)
        else:
            div = len(file_list) // (index+3) + 1   # int(파일 개수 / 열) + 1

        # print(range(0, div))
        # print(range(len(self.label_)))
        print(f"총 파일 개수: {len(file_list)}개")

        if len(self.label_) > 0:
            for i in range(len(self.label_)):
                if i < len(file_list):
                    # print(i)
                    self.label_[i].deleteLater()
            self.label_.clear()

        for file_name in file_list:
            self.label_.append(file_name)

        def clickable(widget):
            class Filter(QObject):
                clicked = Signal()

                def eventFilter(self, obj, event):
                    if obj == widget:
                        if event.type() == QEvent.MouseButtonRelease:
                            if obj.rect().contains(event.pos()):
                                self.clicked.emit()
                                # The developer can opt for .emit(obj) to get the object within the slot.
                                return True
                    return False

            filter = Filter(widget)
            widget.installEventFilter(filter)
            file_sender.append(filter)
            return filter.clicked

        for i in range(0, div):
            for j in range(index+3):
                # print(i, j)
                num = i * (index+3) + j
                if num < len(file_list):
                    # print(num)
                    self.label_[num] = QLabel(self.ui.scrollAreaWidgetContents_4)
                    self.label_[num].setText("")
                    self.label_[num].setObjectName(f"label_{num}")
                    self.ui.gridLayout_6.addWidget(self.label_[num], int(i), int(j), 1, 1)

                    self.pixmap = QPixmap(f"{DIR}/{file_list[num]}")
                    self.label_[num].setPixmap(self.pixmap)
                    self.label_[num].setAlignment(Qt.AlignCenter)
                    # self.label_[num].setScaledContents(True)        # 맞춤 사이즈
                    self.label_[num].setScaledContents(False)       # 원본 사이즈

                    clickable(self.label_[num]).connect(self.pictureListClicked)

        # 불량 (0부터 시작)
        self.label_[2].setStyleSheet("border: 7px solid red;")
        self.label_[4].setStyleSheet("border: 7px solid red;")

    def pictureListClicked(self):
        global DIR
        global file_list
        global file_sender

        image_name = ''
        for i, object_name in enumerate(file_sender):
            if object_name == self.sender():
                image_name = file_list[i]

        if image_name != '':
            self.pop_up = QLabel("")
            self.pixmap = QPixmap(f"{DIR}/{image_name}")
            self.pop_up.setPixmap(self.pixmap)
            self.pop_up.setWindowTitle(image_name)
            self.pop_up.show()

        # self.ui.gridLayout_5.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        # self.label_[7].clear()
        # self.label_[7].setHidden(True)

        # # creating scroll label
        # label = ScrollLabel(self)
        # # setting tool tip
        # label.setToolTip("It is tool tip")


    ########################################################################
    ## MENUS ==> DYNAMIC MENUS FUNCTIONS
    ########################################################################
    def Button(self):
        # GET BT CLICKED
        btnWidget = self.sender()

        # Raw Data
        if btnWidget.objectName() == "btn_raw_data":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_collection)
            UIFunctions.resetStyle(self, "btn_raw_data")
            UIFunctions.labelPage(self, "이미지 수집")
            btnWidget.setStyleSheet(UIFunctions.selectMenu(btnWidget.styleSheet()))

        # Learning
        if btnWidget.objectName() == "btn_learning":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_analysis)
            UIFunctions.resetStyle(self, "btn_learning")
            UIFunctions.labelPage(self, "이미지 분석")
            btnWidget.setStyleSheet(UIFunctions.selectMenu(btnWidget.styleSheet()))

        # Results
        if btnWidget.objectName() == "btn_result":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_management)
            UIFunctions.resetStyle(self, "btn_result")
            UIFunctions.labelPage(self, "데이터 관리")
            btnWidget.setStyleSheet(UIFunctions.selectMenu(btnWidget.styleSheet()))

        # Settings
        if btnWidget.objectName() == "btn_setting":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_widgets)
            UIFunctions.resetStyle(self, "btn_setting")
            UIFunctions.labelPage(self, "Setting")
            btnWidget.setStyleSheet(UIFunctions.selectMenu(btnWidget.styleSheet()))

    ## ==> END ##

    ########################################################################
    ## START ==> APP EVENTS
    ########################################################################

    ## EVENT ==> MOUSE DOUBLE CLICK
    ########################################################################
    def eventFilter(self, watched, event):
        if watched == self.le and event.type() == QtCore.QEvent.MouseButtonDblClick:
            print("pos: ", event.pos())
    ## ==> END ##

    ## EVENT ==> MOUSE CLICK
    ########################################################################
    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()
        if event.buttons() == Qt.LeftButton:
            print('Mouse click: LEFT CLICK')
        if event.buttons() == Qt.RightButton:
            print('Mouse click: RIGHT CLICK')
        if event.buttons() == Qt.MidButton:
            print('Mouse click: MIDDLE BUTTON')
    ## ==> END ##

    ## EVENT ==> KEY PRESSED
    ########################################################################
    def keyPressEvent(self, event):
        print('Key: ' + str(event.key()) + ' | Text Press: ' + str(event.text()))
    ## ==> END ##

    ## EVENT ==> RESIZE EVENT
    ########################################################################
    def resizeEvent(self, event):
        self.resizeFunction()
        return super(MainWindow, self).resizeEvent(event)

    def resizeFunction(self):
        print('Height: ' + str(self.height()) + ' | Width: ' + str(self.width()))
    ## ==> END ##

    ########################################################################
    ## END ==> APP EVENTS
    ############################## ---/--/--- ##############################

if __name__ == "__main__":
    app = QApplication(sys.argv)
    QtGui.QFontDatabase.addApplicationFont('fonts/segoeui.ttf')
    QtGui.QFontDatabase.addApplicationFont('fonts/segoeuib.ttf')
    window = MainWindow()
    sys.exit(app.exec_())
