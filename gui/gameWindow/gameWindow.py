# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gameWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLayout,
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,
    QSpacerItem, QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1360, 730)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setAutoFillBackground(False)
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.widget_2 = QWidget(self.centralwidget)
        self.widget_2.setObjectName(u"widget_2")
        self.verticalLayout = QVBoxLayout(self.widget_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.widget_3 = QWidget(self.widget_2)
        self.widget_3.setObjectName(u"widget_3")

        self.verticalLayout.addWidget(self.widget_3)

        self.widget = QWidget(self.widget_2)
        self.widget.setObjectName(u"widget")
        self.widget.setMinimumSize(QSize(0, 85))
        self.widget.setMaximumSize(QSize(16777215, 16777215))
        self.horizontalLayout_2 = QHBoxLayout(self.widget)
        self.horizontalLayout_2.setSpacing(1)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer = QSpacerItem(0, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.pushButton_15 = QPushButton(self.widget)
        self.pushButton_15.setObjectName(u"pushButton_15")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButton_15.sizePolicy().hasHeightForWidth())
        self.pushButton_15.setSizePolicy(sizePolicy1)
        self.pushButton_15.setMinimumSize(QSize(1, 0))
        self.pushButton_15.setMaximumSize(QSize(70, 16777215))
        self.pushButton_15.setBaseSize(QSize(0, 0))
        font = QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.pushButton_15.setFont(font)

        self.horizontalLayout_2.addWidget(self.pushButton_15)

        self.pushButton_7 = QPushButton(self.widget)
        self.pushButton_7.setObjectName(u"pushButton_7")
        sizePolicy1.setHeightForWidth(self.pushButton_7.sizePolicy().hasHeightForWidth())
        self.pushButton_7.setSizePolicy(sizePolicy1)
        self.pushButton_7.setMinimumSize(QSize(1, 0))
        self.pushButton_7.setMaximumSize(QSize(70, 16777215))
        self.pushButton_7.setBaseSize(QSize(0, 0))
        self.pushButton_7.setFont(font)

        self.horizontalLayout_2.addWidget(self.pushButton_7)

        self.pushButton_16 = QPushButton(self.widget)
        self.pushButton_16.setObjectName(u"pushButton_16")
        sizePolicy1.setHeightForWidth(self.pushButton_16.sizePolicy().hasHeightForWidth())
        self.pushButton_16.setSizePolicy(sizePolicy1)
        self.pushButton_16.setMinimumSize(QSize(1, 0))
        self.pushButton_16.setMaximumSize(QSize(70, 16777215))
        self.pushButton_16.setBaseSize(QSize(0, 0))
        self.pushButton_16.setFont(font)

        self.horizontalLayout_2.addWidget(self.pushButton_16)

        self.pushButton_10 = QPushButton(self.widget)
        self.pushButton_10.setObjectName(u"pushButton_10")
        sizePolicy1.setHeightForWidth(self.pushButton_10.sizePolicy().hasHeightForWidth())
        self.pushButton_10.setSizePolicy(sizePolicy1)
        self.pushButton_10.setMinimumSize(QSize(1, 0))
        self.pushButton_10.setMaximumSize(QSize(70, 16777215))
        self.pushButton_10.setBaseSize(QSize(0, 0))
        self.pushButton_10.setFont(font)

        self.horizontalLayout_2.addWidget(self.pushButton_10)

        self.pushButton_14 = QPushButton(self.widget)
        self.pushButton_14.setObjectName(u"pushButton_14")
        sizePolicy1.setHeightForWidth(self.pushButton_14.sizePolicy().hasHeightForWidth())
        self.pushButton_14.setSizePolicy(sizePolicy1)
        self.pushButton_14.setMinimumSize(QSize(1, 0))
        self.pushButton_14.setMaximumSize(QSize(70, 16777215))
        self.pushButton_14.setBaseSize(QSize(0, 0))
        self.pushButton_14.setFont(font)

        self.horizontalLayout_2.addWidget(self.pushButton_14)

        self.pushButton_3 = QPushButton(self.widget)
        self.pushButton_3.setObjectName(u"pushButton_3")
        sizePolicy1.setHeightForWidth(self.pushButton_3.sizePolicy().hasHeightForWidth())
        self.pushButton_3.setSizePolicy(sizePolicy1)
        self.pushButton_3.setMinimumSize(QSize(1, 0))
        self.pushButton_3.setMaximumSize(QSize(70, 16777215))
        self.pushButton_3.setBaseSize(QSize(0, 0))
        self.pushButton_3.setFont(font)

        self.horizontalLayout_2.addWidget(self.pushButton_3)

        self.pushButton_17 = QPushButton(self.widget)
        self.pushButton_17.setObjectName(u"pushButton_17")
        sizePolicy1.setHeightForWidth(self.pushButton_17.sizePolicy().hasHeightForWidth())
        self.pushButton_17.setSizePolicy(sizePolicy1)
        self.pushButton_17.setMinimumSize(QSize(1, 0))
        self.pushButton_17.setMaximumSize(QSize(70, 16777215))
        self.pushButton_17.setBaseSize(QSize(0, 0))
        self.pushButton_17.setFont(font)

        self.horizontalLayout_2.addWidget(self.pushButton_17)

        self.pushButton_9 = QPushButton(self.widget)
        self.pushButton_9.setObjectName(u"pushButton_9")
        sizePolicy1.setHeightForWidth(self.pushButton_9.sizePolicy().hasHeightForWidth())
        self.pushButton_9.setSizePolicy(sizePolicy1)
        self.pushButton_9.setMinimumSize(QSize(1, 0))
        self.pushButton_9.setMaximumSize(QSize(70, 16777215))
        self.pushButton_9.setBaseSize(QSize(0, 0))
        self.pushButton_9.setFont(font)

        self.horizontalLayout_2.addWidget(self.pushButton_9)

        self.pushButton_4 = QPushButton(self.widget)
        self.pushButton_4.setObjectName(u"pushButton_4")
        sizePolicy1.setHeightForWidth(self.pushButton_4.sizePolicy().hasHeightForWidth())
        self.pushButton_4.setSizePolicy(sizePolicy1)
        self.pushButton_4.setMinimumSize(QSize(1, 0))
        self.pushButton_4.setMaximumSize(QSize(70, 16777215))
        self.pushButton_4.setBaseSize(QSize(0, 0))
        self.pushButton_4.setFont(font)

        self.horizontalLayout_2.addWidget(self.pushButton_4)

        self.pushButton_6 = QPushButton(self.widget)
        self.pushButton_6.setObjectName(u"pushButton_6")
        sizePolicy1.setHeightForWidth(self.pushButton_6.sizePolicy().hasHeightForWidth())
        self.pushButton_6.setSizePolicy(sizePolicy1)
        self.pushButton_6.setMinimumSize(QSize(1, 0))
        self.pushButton_6.setMaximumSize(QSize(70, 16777215))
        self.pushButton_6.setBaseSize(QSize(0, 0))
        self.pushButton_6.setFont(font)

        self.horizontalLayout_2.addWidget(self.pushButton_6)

        self.pushButton_2 = QPushButton(self.widget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        sizePolicy1.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy1)
        self.pushButton_2.setMinimumSize(QSize(1, 0))
        self.pushButton_2.setMaximumSize(QSize(70, 16777215))
        self.pushButton_2.setBaseSize(QSize(0, 0))
        self.pushButton_2.setFont(font)

        self.horizontalLayout_2.addWidget(self.pushButton_2)

        self.pushButton = QPushButton(self.widget)
        self.pushButton.setObjectName(u"pushButton")
        sizePolicy1.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy1)
        self.pushButton.setMinimumSize(QSize(1, 0))
        self.pushButton.setMaximumSize(QSize(70, 16777215))
        self.pushButton.setBaseSize(QSize(0, 0))
        self.pushButton.setFont(font)

        self.horizontalLayout_2.addWidget(self.pushButton)

        self.pushButton_12 = QPushButton(self.widget)
        self.pushButton_12.setObjectName(u"pushButton_12")
        sizePolicy1.setHeightForWidth(self.pushButton_12.sizePolicy().hasHeightForWidth())
        self.pushButton_12.setSizePolicy(sizePolicy1)
        self.pushButton_12.setMinimumSize(QSize(1, 0))
        self.pushButton_12.setMaximumSize(QSize(70, 16777215))
        self.pushButton_12.setBaseSize(QSize(0, 0))
        self.pushButton_12.setFont(font)

        self.horizontalLayout_2.addWidget(self.pushButton_12)

        self.pushButton_5 = QPushButton(self.widget)
        self.pushButton_5.setObjectName(u"pushButton_5")
        sizePolicy1.setHeightForWidth(self.pushButton_5.sizePolicy().hasHeightForWidth())
        self.pushButton_5.setSizePolicy(sizePolicy1)
        self.pushButton_5.setMinimumSize(QSize(1, 0))
        self.pushButton_5.setMaximumSize(QSize(70, 16777215))
        self.pushButton_5.setBaseSize(QSize(0, 0))
        self.pushButton_5.setFont(font)

        self.horizontalLayout_2.addWidget(self.pushButton_5)

        self.pushButton_11 = QPushButton(self.widget)
        self.pushButton_11.setObjectName(u"pushButton_11")
        sizePolicy1.setHeightForWidth(self.pushButton_11.sizePolicy().hasHeightForWidth())
        self.pushButton_11.setSizePolicy(sizePolicy1)
        self.pushButton_11.setMinimumSize(QSize(1, 0))
        self.pushButton_11.setMaximumSize(QSize(70, 16777215))
        self.pushButton_11.setBaseSize(QSize(0, 0))
        self.pushButton_11.setFont(font)

        self.horizontalLayout_2.addWidget(self.pushButton_11)

        self.pushButton_13 = QPushButton(self.widget)
        self.pushButton_13.setObjectName(u"pushButton_13")
        sizePolicy1.setHeightForWidth(self.pushButton_13.sizePolicy().hasHeightForWidth())
        self.pushButton_13.setSizePolicy(sizePolicy1)
        self.pushButton_13.setMinimumSize(QSize(1, 0))
        self.pushButton_13.setMaximumSize(QSize(70, 16777215))
        self.pushButton_13.setBaseSize(QSize(0, 0))
        self.pushButton_13.setFont(font)

        self.horizontalLayout_2.addWidget(self.pushButton_13)

        self.pushButton_8 = QPushButton(self.widget)
        self.pushButton_8.setObjectName(u"pushButton_8")
        sizePolicy1.setHeightForWidth(self.pushButton_8.sizePolicy().hasHeightForWidth())
        self.pushButton_8.setSizePolicy(sizePolicy1)
        self.pushButton_8.setMinimumSize(QSize(1, 0))
        self.pushButton_8.setMaximumSize(QSize(70, 16777215))
        self.pushButton_8.setBaseSize(QSize(0, 0))
        self.pushButton_8.setFont(font)

        self.horizontalLayout_2.addWidget(self.pushButton_8)

        self.horizontalSpacer_2 = QSpacerItem(0, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addWidget(self.widget)

        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 1)

        self.gridLayout.addWidget(self.widget_2, 0, 0, 1, 1)

        self.gridLayout.setRowStretch(0, 4)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1360, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.pushButton_15.setText(QCoreApplication.translate("MainWindow", u"1\n"
"                                                        00000\n"
"                                                    ", None))
        self.pushButton_7.setText(QCoreApplication.translate("MainWindow", u"1\n"
"                                                        00000\n"
"                                                    ", None))
        self.pushButton_16.setText(QCoreApplication.translate("MainWindow", u"1\n"
"                                                        00000\n"
"                                                    ", None))
        self.pushButton_10.setText(QCoreApplication.translate("MainWindow", u"1\n"
"                                                        00000\n"
"                                                    ", None))
        self.pushButton_14.setText(QCoreApplication.translate("MainWindow", u"1\n"
"                                                        00000\n"
"                                                    ", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"1\n"
"                                                        00000\n"
"                                                    ", None))
        self.pushButton_17.setText(QCoreApplication.translate("MainWindow", u"1\n"
"                                                        00000\n"
"                                                    ", None))
        self.pushButton_9.setText(QCoreApplication.translate("MainWindow", u"1\n"
"                                                        00000\n"
"                                                    ", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"1\n"
"                                                        00000\n"
"                                                    ", None))
        self.pushButton_6.setText(QCoreApplication.translate("MainWindow", u"1\n"
"                                                        00000\n"
"                                                    ", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"1\n"
"                                                        00000\n"
"                                                    ", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"1\n"
"                                                        00000\n"
"                                                    ", None))
        self.pushButton_12.setText(QCoreApplication.translate("MainWindow", u"1\n"
"                                                        00000\n"
"                                                    ", None))
        self.pushButton_5.setText(QCoreApplication.translate("MainWindow", u"1\n"
"                                                        00000\n"
"                                                    ", None))
        self.pushButton_11.setText(QCoreApplication.translate("MainWindow", u"1\n"
"                                                        00000\n"
"                                                    ", None))
        self.pushButton_13.setText(QCoreApplication.translate("MainWindow", u"1\n"
"                                                        00000\n"
"                                                    ", None))
        self.pushButton_8.setText(QCoreApplication.translate("MainWindow", u"1\n"
"                                                        00000\n"
"                                                    ", None))
    # retranslateUi

