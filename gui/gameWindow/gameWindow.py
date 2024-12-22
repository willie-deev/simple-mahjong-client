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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
    QLayout, QMainWindow, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1321, 816)
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
        self.selfCards = QWidget(self.centralwidget)
        self.selfCards.setObjectName(u"selfCards")
        self.selfCards.setMinimumSize(QSize(0, 0))
        self.selfCards.setMaximumSize(QSize(16777215, 16777215))
        self.horizontalLayout_3 = QHBoxLayout(self.selfCards)
        self.horizontalLayout_3.setSpacing(1)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_3 = QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)

        self.handCards = QHBoxLayout()
        self.handCards.setObjectName(u"handCards")

        self.horizontalLayout_3.addLayout(self.handCards)

        self.horizontalSpacer_4 = QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_4)

        self.newCards = QHBoxLayout()
        self.newCards.setObjectName(u"newCards")

        self.horizontalLayout_3.addLayout(self.newCards)

        self.horizontalSpacer_5 = QSpacerItem(0, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_5)

        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.selfActionedCardsLayout = QHBoxLayout()
        self.selfActionedCardsLayout.setObjectName(u"selfActionedCardsLayout")

        self.verticalLayout_8.addLayout(self.selfActionedCardsLayout)

        self.verticalSpacer_9 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_8.addItem(self.verticalSpacer_9)

        self.verticalLayout_8.setStretch(0, 1)

        self.horizontalLayout_3.addLayout(self.verticalLayout_8)

        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(4, 1)

        self.gridLayout.addWidget(self.selfCards, 1, 0, 1, 1)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_2)

        self.leftCardsLayout = QVBoxLayout()
        self.leftCardsLayout.setSpacing(1)
        self.leftCardsLayout.setObjectName(u"leftCardsLayout")

        self.verticalLayout_3.addLayout(self.leftCardsLayout)

        self.verticalSpacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.leftNewCardsLayout = QVBoxLayout()
        self.leftNewCardsLayout.setObjectName(u"leftNewCardsLayout")

        self.verticalLayout_3.addLayout(self.leftNewCardsLayout)

        self.verticalSpacer_10 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_10)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalSpacer_10 = QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_10)

        self.leftActionedCardsLayout = QVBoxLayout()
        self.leftActionedCardsLayout.setObjectName(u"leftActionedCardsLayout")

        self.horizontalLayout_5.addLayout(self.leftActionedCardsLayout)

        self.horizontalLayout_5.setStretch(1, 1)

        self.verticalLayout_3.addLayout(self.horizontalLayout_5)

        self.verticalLayout_3.setStretch(0, 1)
        self.verticalLayout_3.setStretch(4, 1)

        self.gridLayout_2.addLayout(self.verticalLayout_3, 0, 0, 2, 1)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.rightActionedCardsLayout = QVBoxLayout()
        self.rightActionedCardsLayout.setObjectName(u"rightActionedCardsLayout")

        self.horizontalLayout_10.addLayout(self.rightActionedCardsLayout)

        self.horizontalSpacer_12 = QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_12)

        self.horizontalLayout_10.setStretch(0, 1)

        self.verticalLayout_4.addLayout(self.horizontalLayout_10)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_4)

        self.rightNewCardsLayout = QVBoxLayout()
        self.rightNewCardsLayout.setObjectName(u"rightNewCardsLayout")

        self.verticalLayout_4.addLayout(self.rightNewCardsLayout)

        self.verticalSpacer_12 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_12)

        self.rightCardsLayout = QVBoxLayout()
        self.rightCardsLayout.setSpacing(1)
        self.rightCardsLayout.setObjectName(u"rightCardsLayout")

        self.verticalLayout_4.addLayout(self.rightCardsLayout)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_3)

        self.verticalLayout_4.setStretch(1, 1)
        self.verticalLayout_4.setStretch(5, 1)

        self.gridLayout_2.addLayout(self.verticalLayout_4, 0, 2, 2, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalSpacer_11 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_9.addItem(self.verticalSpacer_11)

        self.oppositeActionedCardsLayout = QHBoxLayout()
        self.oppositeActionedCardsLayout.setObjectName(u"oppositeActionedCardsLayout")

        self.verticalLayout_9.addLayout(self.oppositeActionedCardsLayout)

        self.verticalLayout_9.setStretch(1, 1)

        self.horizontalLayout_4.addLayout(self.verticalLayout_9)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)

        self.oppositeNewCardsLayout = QHBoxLayout()
        self.oppositeNewCardsLayout.setObjectName(u"oppositeNewCardsLayout")

        self.horizontalLayout_4.addLayout(self.oppositeNewCardsLayout)

        self.horizontalSpacer_11 = QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_11)

        self.oppositeCardsLayout = QHBoxLayout()
        self.oppositeCardsLayout.setSpacing(1)
        self.oppositeCardsLayout.setObjectName(u"oppositeCardsLayout")

        self.horizontalLayout_4.addLayout(self.oppositeCardsLayout)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.horizontalLayout_4.setStretch(1, 1)
        self.horizontalLayout_4.setStretch(5, 1)

        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.verticalLayout.setStretch(0, 3)

        self.gridLayout_2.addLayout(self.verticalLayout, 0, 1, 1, 1)

        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.leftDiscardedLayout = QGridLayout()
        self.leftDiscardedLayout.setObjectName(u"leftDiscardedLayout")

        self.gridLayout_5.addLayout(self.leftDiscardedLayout, 1, 0, 2, 1)

        self.oppositeDiscardedLayout = QGridLayout()
        self.oppositeDiscardedLayout.setObjectName(u"oppositeDiscardedLayout")

        self.gridLayout_5.addLayout(self.oppositeDiscardedLayout, 0, 0, 1, 2)

        self.rightDiscardedLayout = QGridLayout()
        self.rightDiscardedLayout.setObjectName(u"rightDiscardedLayout")

        self.gridLayout_5.addLayout(self.rightDiscardedLayout, 0, 2, 2, 1)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalSpacer_7 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer_7)

        self.leftWind = QLabel(self.centralwidget)
        self.leftWind.setObjectName(u"leftWind")
        self.leftWind.setAlignment(Qt.AlignCenter)

        self.verticalLayout_6.addWidget(self.leftWind)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer_5)


        self.horizontalLayout.addLayout(self.verticalLayout_6)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_9)

        self.oppositeWind = QLabel(self.centralwidget)
        self.oppositeWind.setObjectName(u"oppositeWind")
        self.oppositeWind.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_7.addWidget(self.oppositeWind)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_8)


        self.verticalLayout_5.addLayout(self.horizontalLayout_7)

        self.label_8 = QLabel(self.centralwidget)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setAlignment(Qt.AlignCenter)

        self.verticalLayout_5.addWidget(self.label_8)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_7)

        self.selfWind = QLabel(self.centralwidget)
        self.selfWind.setObjectName(u"selfWind")
        self.selfWind.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.selfWind)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_6)


        self.verticalLayout_5.addLayout(self.horizontalLayout_2)


        self.horizontalLayout.addLayout(self.verticalLayout_5)

        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer_6)

        self.rightWind = QLabel(self.centralwidget)
        self.rightWind.setObjectName(u"rightWind")
        self.rightWind.setAlignment(Qt.AlignCenter)

        self.verticalLayout_7.addWidget(self.rightWind)

        self.verticalSpacer_8 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer_8)


        self.horizontalLayout.addLayout(self.verticalLayout_7)

        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 4)
        self.horizontalLayout.setStretch(2, 1)

        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.verticalLayout_2.setStretch(0, 1)

        self.gridLayout_5.addLayout(self.verticalLayout_2, 1, 1, 1, 1)

        self.selfDiscardedWidget = QWidget(self.centralwidget)
        self.selfDiscardedWidget.setObjectName(u"selfDiscardedWidget")
        sizePolicy.setHeightForWidth(self.selfDiscardedWidget.sizePolicy().hasHeightForWidth())
        self.selfDiscardedWidget.setSizePolicy(sizePolicy)
        self.selfDiscardedLayout = QGridLayout(self.selfDiscardedWidget)
        self.selfDiscardedLayout.setObjectName(u"selfDiscardedLayout")

        self.gridLayout_5.addWidget(self.selfDiscardedWidget, 2, 1, 1, 2)

        self.gridLayout_5.setRowStretch(0, 2)
        self.gridLayout_5.setRowStretch(1, 3)
        self.gridLayout_5.setRowStretch(2, 2)
        self.gridLayout_5.setColumnStretch(0, 2)
        self.gridLayout_5.setColumnStretch(1, 3)
        self.gridLayout_5.setColumnStretch(2, 2)

        self.gridLayout_2.addLayout(self.gridLayout_5, 1, 1, 1, 1)

        self.gridLayout_2.setRowStretch(0, 1)
        self.gridLayout_2.setRowStretch(1, 5)
        self.gridLayout_2.setColumnStretch(0, 1)
        self.gridLayout_2.setColumnStretch(1, 10)
        self.gridLayout_2.setColumnStretch(2, 1)

        self.gridLayout.addLayout(self.gridLayout_2, 0, 0, 1, 1)

        self.gridLayout.setRowStretch(0, 7)
        self.gridLayout.setRowStretch(1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.leftWind.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.oppositeWind.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.selfWind.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.rightWind.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
    # retranslateUi

