# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainView.ui'
##
## Created by: Qt User Interface Compiler version 6.6.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QCheckBox, QDoubleSpinBox,
    QFrame, QGraphicsView, QGridLayout, QHBoxLayout,
    QLCDNumber, QLabel, QMainWindow, QMenu,
    QMenuBar, QPushButton, QScrollArea, QSizePolicy,
    QSpacerItem, QSpinBox, QStatusBar, QTabWidget,
    QVBoxLayout, QWidget)

class Ui_calibrationUI(object):
    def setupUi(self, calibrationUI):
        if not calibrationUI.objectName():
            calibrationUI.setObjectName(u"calibrationUI")
        calibrationUI.resize(473, 677)
        calibrationUI.setWindowOpacity(1.000000000000000)
        calibrationUI.setTabShape(QTabWidget.Rounded)
        self.actionReference_Axis = QAction(calibrationUI)
        self.actionReference_Axis.setObjectName(u"actionReference_Axis")
        self.actionReboot_System = QAction(calibrationUI)
        self.actionReboot_System.setObjectName(u"actionReboot_System")
        self.centralWidget = QWidget(calibrationUI)
        self.centralWidget.setObjectName(u"centralWidget")
        self.verticalLayout_4 = QVBoxLayout(self.centralWidget)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.connectButton = QPushButton(self.centralWidget)
        self.connectButton.setObjectName(u"connectButton")

        self.horizontalLayout_3.addWidget(self.connectButton)


        self.verticalLayout_4.addLayout(self.horizontalLayout_3)

        self.Tabs = QTabWidget(self.centralWidget)
        self.Tabs.setObjectName(u"Tabs")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Tabs.sizePolicy().hasHeightForWidth())
        self.Tabs.setSizePolicy(sizePolicy)
        self.Settings = QWidget()
        self.Settings.setObjectName(u"Settings")
        self.verticalLayout_2 = QVBoxLayout(self.Settings)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.settingsTabTopVpacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.settingsTabTopVpacer)

        self.settingsInputsGridLayout = QGridLayout()
        self.settingsInputsGridLayout.setObjectName(u"settingsInputsGridLayout")
        self.speedLabel = QLabel(self.Settings)
        self.speedLabel.setObjectName(u"speedLabel")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.speedLabel.sizePolicy().hasHeightForWidth())
        self.speedLabel.setSizePolicy(sizePolicy1)

        self.settingsInputsGridLayout.addWidget(self.speedLabel, 0, 0, 1, 1)

        self.zAxisLabel = QLabel(self.Settings)
        self.zAxisLabel.setObjectName(u"zAxisLabel")
        sizePolicy1.setHeightForWidth(self.zAxisLabel.sizePolicy().hasHeightForWidth())
        self.zAxisLabel.setSizePolicy(sizePolicy1)

        self.settingsInputsGridLayout.addWidget(self.zAxisLabel, 1, 0, 1, 1)

        self.zAxisUnitLabel = QLabel(self.Settings)
        self.zAxisUnitLabel.setObjectName(u"zAxisUnitLabel")
        sizePolicy1.setHeightForWidth(self.zAxisUnitLabel.sizePolicy().hasHeightForWidth())
        self.zAxisUnitLabel.setSizePolicy(sizePolicy1)

        self.settingsInputsGridLayout.addWidget(self.zAxisUnitLabel, 1, 3, 1, 1)

        self.stepSizeLabel = QLabel(self.Settings)
        self.stepSizeLabel.setObjectName(u"stepSizeLabel")
        sizePolicy1.setHeightForWidth(self.stepSizeLabel.sizePolicy().hasHeightForWidth())
        self.stepSizeLabel.setSizePolicy(sizePolicy1)

        self.settingsInputsGridLayout.addWidget(self.stepSizeLabel, 2, 0, 1, 1)

        self.stepSizeUnitLabel = QLabel(self.Settings)
        self.stepSizeUnitLabel.setObjectName(u"stepSizeUnitLabel")
        sizePolicy1.setHeightForWidth(self.stepSizeUnitLabel.sizePolicy().hasHeightForWidth())
        self.stepSizeUnitLabel.setSizePolicy(sizePolicy1)

        self.settingsInputsGridLayout.addWidget(self.stepSizeUnitLabel, 2, 3, 1, 1)

        self.speedUnitLabel = QLabel(self.Settings)
        self.speedUnitLabel.setObjectName(u"speedUnitLabel")
        sizePolicy1.setHeightForWidth(self.speedUnitLabel.sizePolicy().hasHeightForWidth())
        self.speedUnitLabel.setSizePolicy(sizePolicy1)
        self.speedUnitLabel.setMaximumSize(QSize(16777215, 16777215))
        self.speedUnitLabel.setMouseTracking(True)
        self.speedUnitLabel.setTextFormat(Qt.AutoText)

        self.settingsInputsGridLayout.addWidget(self.speedUnitLabel, 0, 3, 1, 1)

        self.speedSpin = QDoubleSpinBox(self.Settings)
        self.speedSpin.setObjectName(u"speedSpin")
        self.speedSpin.setEnabled(False)
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.speedSpin.sizePolicy().hasHeightForWidth())
        self.speedSpin.setSizePolicy(sizePolicy2)
        self.speedSpin.setDecimals(2)
        self.speedSpin.setMaximum(6.000000000000000)
        self.speedSpin.setSingleStep(0.100000000000000)

        self.settingsInputsGridLayout.addWidget(self.speedSpin, 0, 1, 1, 2)

        self.zAxisSpin = QDoubleSpinBox(self.Settings)
        self.zAxisSpin.setObjectName(u"zAxisSpin")
        self.zAxisSpin.setEnabled(False)
        self.zAxisSpin.setMaximum(300.000000000000000)

        self.settingsInputsGridLayout.addWidget(self.zAxisSpin, 1, 1, 1, 2)

        self.stepSizeSpin = QDoubleSpinBox(self.Settings)
        self.stepSizeSpin.setObjectName(u"stepSizeSpin")
        self.stepSizeSpin.setEnabled(False)
        self.stepSizeSpin.setSingleStep(1.000000000000000)
        self.stepSizeSpin.setStepType(QAbstractSpinBox.DefaultStepType)
        self.stepSizeSpin.setValue(0.000000000000000)

        self.settingsInputsGridLayout.addWidget(self.stepSizeSpin, 2, 1, 1, 2)


        self.verticalLayout_2.addLayout(self.settingsInputsGridLayout)

        self.settingsTabMiddleVSpacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.MinimumExpanding)

        self.verticalLayout_2.addItem(self.settingsTabMiddleVSpacer)

        self.settingsTabButtonHLayout = QHBoxLayout()
        self.settingsTabButtonHLayout.setObjectName(u"settingsTabButtonHLayout")
        self.Up = QPushButton(self.Settings)
        self.Up.setObjectName(u"Up")
        self.Up.setEnabled(False)
        sizePolicy3 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.Up.sizePolicy().hasHeightForWidth())
        self.Up.setSizePolicy(sizePolicy3)

        self.settingsTabButtonHLayout.addWidget(self.Up)

        self.Move = QPushButton(self.Settings)
        self.Move.setObjectName(u"Move")
        self.Move.setEnabled(False)
        sizePolicy3.setHeightForWidth(self.Move.sizePolicy().hasHeightForWidth())
        self.Move.setSizePolicy(sizePolicy3)

        self.settingsTabButtonHLayout.addWidget(self.Move)

        self.Down = QPushButton(self.Settings)
        self.Down.setObjectName(u"Down")
        self.Down.setEnabled(False)
        sizePolicy3.setHeightForWidth(self.Down.sizePolicy().hasHeightForWidth())
        self.Down.setSizePolicy(sizePolicy3)

        self.settingsTabButtonHLayout.addWidget(self.Down)


        self.verticalLayout_2.addLayout(self.settingsTabButtonHLayout)

        self.settingsTabBottomVSpacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.MinimumExpanding)

        self.verticalLayout_2.addItem(self.settingsTabBottomVSpacer)

        self.Tabs.addTab(self.Settings, "")
        self.Calibration = QWidget()
        self.Calibration.setObjectName(u"Calibration")
        self.verticalLayout_3 = QVBoxLayout(self.Calibration)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.calibrationTabTopSpacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.calibrationTabTopSpacer)

        self.calibartionButtonsHLayout = QHBoxLayout()
        self.calibartionButtonsHLayout.setObjectName(u"calibartionButtonsHLayout")
        self.sweepPushButton = QPushButton(self.Calibration)
        self.sweepPushButton.setObjectName(u"sweepPushButton")
        self.sweepPushButton.setEnabled(False)
        sizePolicy4 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.sweepPushButton.sizePolicy().hasHeightForWidth())
        self.sweepPushButton.setSizePolicy(sizePolicy4)

        self.calibartionButtonsHLayout.addWidget(self.sweepPushButton)

        self.referenceAxisPushButton = QPushButton(self.Calibration)
        self.referenceAxisPushButton.setObjectName(u"referenceAxisPushButton")
        self.referenceAxisPushButton.setEnabled(False)
        sizePolicy4.setHeightForWidth(self.referenceAxisPushButton.sizePolicy().hasHeightForWidth())
        self.referenceAxisPushButton.setSizePolicy(sizePolicy4)

        self.calibartionButtonsHLayout.addWidget(self.referenceAxisPushButton)


        self.verticalLayout_3.addLayout(self.calibartionButtonsHLayout)

        self.calibrationTabLine1 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.calibrationTabLine1)

        self.calibrationTabVLayout = QVBoxLayout()
        self.calibrationTabVLayout.setObjectName(u"calibrationTabVLayout")
        self.calibrationSwTiHLayout = QHBoxLayout()
        self.calibrationSwTiHLayout.setObjectName(u"calibrationSwTiHLayout")
        self.calibrationTabLabelVLazout = QVBoxLayout()
        self.calibrationTabLabelVLazout.setObjectName(u"calibrationTabLabelVLazout")
        self.nSweepsLabel = QLabel(self.Calibration)
        self.nSweepsLabel.setObjectName(u"nSweepsLabel")
        sizePolicy5 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.nSweepsLabel.sizePolicy().hasHeightForWidth())
        self.nSweepsLabel.setSizePolicy(sizePolicy5)

        self.calibrationTabLabelVLazout.addWidget(self.nSweepsLabel)

        self.measuringTImeLabel = QLabel(self.Calibration)
        self.measuringTImeLabel.setObjectName(u"measuringTImeLabel")
        sizePolicy6 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.MinimumExpanding)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.measuringTImeLabel.sizePolicy().hasHeightForWidth())
        self.measuringTImeLabel.setSizePolicy(sizePolicy6)

        self.calibrationTabLabelVLazout.addWidget(self.measuringTImeLabel)

        self.calibrationTimeLabel_2 = QLabel(self.Calibration)
        self.calibrationTimeLabel_2.setObjectName(u"calibrationTimeLabel_2")
        sizePolicy6.setHeightForWidth(self.calibrationTimeLabel_2.sizePolicy().hasHeightForWidth())
        self.calibrationTimeLabel_2.setSizePolicy(sizePolicy6)

        self.calibrationTabLabelVLazout.addWidget(self.calibrationTimeLabel_2)


        self.calibrationSwTiHLayout.addLayout(self.calibrationTabLabelVLazout)

        self.SpinBoxVLayout = QVBoxLayout()
        self.SpinBoxVLayout.setObjectName(u"SpinBoxVLayout")
        self.nSweepSpin = QSpinBox(self.Calibration)
        self.nSweepSpin.setObjectName(u"nSweepSpin")
        self.nSweepSpin.setEnabled(False)
        sizePolicy2.setHeightForWidth(self.nSweepSpin.sizePolicy().hasHeightForWidth())
        self.nSweepSpin.setSizePolicy(sizePolicy2)

        self.SpinBoxVLayout.addWidget(self.nSweepSpin)

        self.measuringTImeSpin = QDoubleSpinBox(self.Calibration)
        self.measuringTImeSpin.setObjectName(u"measuringTImeSpin")
        self.measuringTImeSpin.setEnabled(False)
        sizePolicy2.setHeightForWidth(self.measuringTImeSpin.sizePolicy().hasHeightForWidth())
        self.measuringTImeSpin.setSizePolicy(sizePolicy2)

        self.SpinBoxVLayout.addWidget(self.measuringTImeSpin)

        self.calibrationTimeSpin = QDoubleSpinBox(self.Calibration)
        self.calibrationTimeSpin.setObjectName(u"calibrationTimeSpin")
        self.calibrationTimeSpin.setEnabled(False)
        sizePolicy7 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.calibrationTimeSpin.sizePolicy().hasHeightForWidth())
        self.calibrationTimeSpin.setSizePolicy(sizePolicy7)

        self.SpinBoxVLayout.addWidget(self.calibrationTimeSpin)


        self.calibrationSwTiHLayout.addLayout(self.SpinBoxVLayout)

        self.unitsLabelVLayout = QVBoxLayout()
        self.unitsLabelVLayout.setObjectName(u"unitsLabelVLayout")
        self.nsweepUnitLabel = QLabel(self.Calibration)
        self.nsweepUnitLabel.setObjectName(u"nsweepUnitLabel")
        sizePolicy8 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.nsweepUnitLabel.sizePolicy().hasHeightForWidth())
        self.nsweepUnitLabel.setSizePolicy(sizePolicy8)

        self.unitsLabelVLayout.addWidget(self.nsweepUnitLabel)

        self.measuringTimeUnitLabel = QLabel(self.Calibration)
        self.measuringTimeUnitLabel.setObjectName(u"measuringTimeUnitLabel")
        sizePolicy8.setHeightForWidth(self.measuringTimeUnitLabel.sizePolicy().hasHeightForWidth())
        self.measuringTimeUnitLabel.setSizePolicy(sizePolicy8)

        self.unitsLabelVLayout.addWidget(self.measuringTimeUnitLabel)

        self.calibrationTimeUnitLabel = QLabel(self.Calibration)
        self.calibrationTimeUnitLabel.setObjectName(u"calibrationTimeUnitLabel")
        sizePolicy8.setHeightForWidth(self.calibrationTimeUnitLabel.sizePolicy().hasHeightForWidth())
        self.calibrationTimeUnitLabel.setSizePolicy(sizePolicy8)

        self.unitsLabelVLayout.addWidget(self.calibrationTimeUnitLabel)


        self.calibrationSwTiHLayout.addLayout(self.unitsLabelVLayout)


        self.calibrationTabVLayout.addLayout(self.calibrationSwTiHLayout)

        self.calibrationRngMstopsGridLayout = QGridLayout()
        self.calibrationRngMstopsGridLayout.setObjectName(u"calibrationRngMstopsGridLayout")
        self.nMeasurementsHLayout = QHBoxLayout()
        self.nMeasurementsHLayout.setObjectName(u"nMeasurementsHLayout")
        self.noOfMeasurementStops = QLabel(self.Calibration)
        self.noOfMeasurementStops.setObjectName(u"noOfMeasurementStops")
        sizePolicy6.setHeightForWidth(self.noOfMeasurementStops.sizePolicy().hasHeightForWidth())
        self.noOfMeasurementStops.setSizePolicy(sizePolicy6)

        self.nMeasurementsHLayout.addWidget(self.noOfMeasurementStops)

        self.nMeasurementStopSpinValue = QDoubleSpinBox(self.Calibration)
        self.nMeasurementStopSpinValue.setObjectName(u"nMeasurementStopSpinValue")
        self.nMeasurementStopSpinValue.setEnabled(False)
        sizePolicy2.setHeightForWidth(self.nMeasurementStopSpinValue.sizePolicy().hasHeightForWidth())
        self.nMeasurementStopSpinValue.setSizePolicy(sizePolicy2)

        self.nMeasurementsHLayout.addWidget(self.nMeasurementStopSpinValue)

        self.nMeasurementUnitLabel = QLabel(self.Calibration)
        self.nMeasurementUnitLabel.setObjectName(u"nMeasurementUnitLabel")
        sizePolicy8.setHeightForWidth(self.nMeasurementUnitLabel.sizePolicy().hasHeightForWidth())
        self.nMeasurementUnitLabel.setSizePolicy(sizePolicy8)

        self.nMeasurementsHLayout.addWidget(self.nMeasurementUnitLabel)


        self.calibrationRngMstopsGridLayout.addLayout(self.nMeasurementsHLayout, 1, 2, 1, 1)

        self.mSweepHLayout = QHBoxLayout()
        self.mSweepHLayout.setObjectName(u"mSweepHLayout")
        self.maxSweepLabel = QLabel(self.Calibration)
        self.maxSweepLabel.setObjectName(u"maxSweepLabel")
        sizePolicy6.setHeightForWidth(self.maxSweepLabel.sizePolicy().hasHeightForWidth())
        self.maxSweepLabel.setSizePolicy(sizePolicy6)
        self.maxSweepLabel.setScaledContents(False)

        self.mSweepHLayout.addWidget(self.maxSweepLabel)

        self.maxSweepSpin = QDoubleSpinBox(self.Calibration)
        self.maxSweepSpin.setObjectName(u"maxSweepSpin")
        self.maxSweepSpin.setEnabled(False)
        sizePolicy2.setHeightForWidth(self.maxSweepSpin.sizePolicy().hasHeightForWidth())
        self.maxSweepSpin.setSizePolicy(sizePolicy2)
        self.maxSweepSpin.setMinimum(20.000000000000000)
        self.maxSweepSpin.setMaximum(300.000000000000000)

        self.mSweepHLayout.addWidget(self.maxSweepSpin)

        self.maxSweepDistanceUnitLabel = QLabel(self.Calibration)
        self.maxSweepDistanceUnitLabel.setObjectName(u"maxSweepDistanceUnitLabel")
        sizePolicy8.setHeightForWidth(self.maxSweepDistanceUnitLabel.sizePolicy().hasHeightForWidth())
        self.maxSweepDistanceUnitLabel.setSizePolicy(sizePolicy8)

        self.mSweepHLayout.addWidget(self.maxSweepDistanceUnitLabel)


        self.calibrationRngMstopsGridLayout.addLayout(self.mSweepHLayout, 0, 0, 1, 1)

        self.fMeasurementHLayout = QHBoxLayout()
        self.fMeasurementHLayout.setObjectName(u"fMeasurementHLayout")
        self.fMeasurementHeightLabel = QLabel(self.Calibration)
        self.fMeasurementHeightLabel.setObjectName(u"fMeasurementHeightLabel")
        sizePolicy6.setHeightForWidth(self.fMeasurementHeightLabel.sizePolicy().hasHeightForWidth())
        self.fMeasurementHeightLabel.setSizePolicy(sizePolicy6)

        self.fMeasurementHLayout.addWidget(self.fMeasurementHeightLabel)

        self.fMeasurementHeightSpinValue = QDoubleSpinBox(self.Calibration)
        self.fMeasurementHeightSpinValue.setObjectName(u"fMeasurementHeightSpinValue")
        self.fMeasurementHeightSpinValue.setEnabled(False)
        sizePolicy2.setHeightForWidth(self.fMeasurementHeightSpinValue.sizePolicy().hasHeightForWidth())
        self.fMeasurementHeightSpinValue.setSizePolicy(sizePolicy2)

        self.fMeasurementHLayout.addWidget(self.fMeasurementHeightSpinValue)

        self.fMeasurementHeightUnitLabel = QLabel(self.Calibration)
        self.fMeasurementHeightUnitLabel.setObjectName(u"fMeasurementHeightUnitLabel")
        sizePolicy8.setHeightForWidth(self.fMeasurementHeightUnitLabel.sizePolicy().hasHeightForWidth())
        self.fMeasurementHeightUnitLabel.setSizePolicy(sizePolicy8)

        self.fMeasurementHLayout.addWidget(self.fMeasurementHeightUnitLabel)


        self.calibrationRngMstopsGridLayout.addLayout(self.fMeasurementHLayout, 0, 2, 1, 1)

        self.minSweepHlayout = QHBoxLayout()
        self.minSweepHlayout.setObjectName(u"minSweepHlayout")
        self.minSweepLabel = QLabel(self.Calibration)
        self.minSweepLabel.setObjectName(u"minSweepLabel")
        sizePolicy6.setHeightForWidth(self.minSweepLabel.sizePolicy().hasHeightForWidth())
        self.minSweepLabel.setSizePolicy(sizePolicy6)

        self.minSweepHlayout.addWidget(self.minSweepLabel)

        self.minSweepSpin = QDoubleSpinBox(self.Calibration)
        self.minSweepSpin.setObjectName(u"minSweepSpin")
        self.minSweepSpin.setEnabled(False)
        sizePolicy2.setHeightForWidth(self.minSweepSpin.sizePolicy().hasHeightForWidth())
        self.minSweepSpin.setSizePolicy(sizePolicy2)
        self.minSweepSpin.setMinimum(15.000000000000000)

        self.minSweepHlayout.addWidget(self.minSweepSpin)

        self.minSweepDistanceUnitLabel = QLabel(self.Calibration)
        self.minSweepDistanceUnitLabel.setObjectName(u"minSweepDistanceUnitLabel")
        sizePolicy8.setHeightForWidth(self.minSweepDistanceUnitLabel.sizePolicy().hasHeightForWidth())
        self.minSweepDistanceUnitLabel.setSizePolicy(sizePolicy8)

        self.minSweepHlayout.addWidget(self.minSweepDistanceUnitLabel)


        self.calibrationRngMstopsGridLayout.addLayout(self.minSweepHlayout, 1, 0, 1, 1)

        self.line_3 = QFrame(self.Calibration)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.VLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.calibrationRngMstopsGridLayout.addWidget(self.line_3, 0, 1, 1, 1)

        self.line_4 = QFrame(self.Calibration)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.VLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.calibrationRngMstopsGridLayout.addWidget(self.line_4, 1, 1, 1, 1)


        self.calibrationTabVLayout.addLayout(self.calibrationRngMstopsGridLayout)

        self.verticalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.calibrationTabVLayout.addItem(self.verticalSpacer_2)


        self.verticalLayout_3.addLayout(self.calibrationTabVLayout)

        self.Tabs.addTab(self.Calibration, "")

        self.verticalLayout_4.addWidget(self.Tabs)

        self.pausePushButton_2 = QPushButton(self.centralWidget)
        self.pausePushButton_2.setObjectName(u"pausePushButton_2")
        self.pausePushButton_2.setEnabled(False)
        sizePolicy9 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy9.setHorizontalStretch(0)
        sizePolicy9.setVerticalStretch(0)
        sizePolicy9.setHeightForWidth(self.pausePushButton_2.sizePolicy().hasHeightForWidth())
        self.pausePushButton_2.setSizePolicy(sizePolicy9)

        self.verticalLayout_4.addWidget(self.pausePushButton_2)

        self.line = QFrame(self.centralWidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_4.addWidget(self.line)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.imageView = QGraphicsView(self.centralWidget)
        self.imageView.setObjectName(u"imageView")

        self.horizontalLayout.addWidget(self.imageView)

        self.graphicsView = QGraphicsView(self.centralWidget)
        self.graphicsView.setObjectName(u"graphicsView")
        sizePolicy.setHeightForWidth(self.graphicsView.sizePolicy().hasHeightForWidth())
        self.graphicsView.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.graphicsView)


        self.verticalLayout_4.addLayout(self.horizontalLayout)

        self.line_2 = QFrame(self.centralWidget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_4.addWidget(self.line_2)

        self.bottomSweepHLayout = QHBoxLayout()
        self.bottomSweepHLayout.setObjectName(u"bottomSweepHLayout")
        self.currentSweepNumberLabel = QLabel(self.centralWidget)
        self.currentSweepNumberLabel.setObjectName(u"currentSweepNumberLabel")

        self.bottomSweepHLayout.addWidget(self.currentSweepNumberLabel)

        self.sweepNumberLCD = QLCDNumber(self.centralWidget)
        self.sweepNumberLCD.setObjectName(u"sweepNumberLCD")
        self.sweepNumberLCD.setDigitCount(1)

        self.bottomSweepHLayout.addWidget(self.sweepNumberLCD)


        self.verticalLayout_4.addLayout(self.bottomSweepHLayout)

        self.line_5 = QFrame(self.centralWidget)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShape(QFrame.HLine)
        self.line_5.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_4.addWidget(self.line_5)

        self.viewLogCheckBox = QCheckBox(self.centralWidget)
        self.viewLogCheckBox.setObjectName(u"viewLogCheckBox")

        self.verticalLayout_4.addWidget(self.viewLogCheckBox)

        self.line_6 = QFrame(self.centralWidget)
        self.line_6.setObjectName(u"line_6")
        self.line_6.setFrameShape(QFrame.HLine)
        self.line_6.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_4.addWidget(self.line_6)

        self.scrollArea = QScrollArea(self.centralWidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.LoggerContents = QWidget()
        self.LoggerContents.setObjectName(u"LoggerContents")
        self.LoggerContents.setGeometry(QRect(0, 0, 453, 69))
        self.scrollArea.setWidget(self.LoggerContents)

        self.verticalLayout_4.addWidget(self.scrollArea)

        calibrationUI.setCentralWidget(self.centralWidget)
        self.menubar = QMenuBar(calibrationUI)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 473, 22))
        self.menuMenu = QMenu(self.menubar)
        self.menuMenu.setObjectName(u"menuMenu")
        calibrationUI.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(calibrationUI)
        self.statusbar.setObjectName(u"statusbar")
        calibrationUI.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuMenu.menuAction())
        self.menuMenu.addAction(self.actionReference_Axis)
        self.menuMenu.addAction(self.actionReboot_System)

        self.retranslateUi(calibrationUI)

        self.Tabs.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(calibrationUI)
    # setupUi

    def retranslateUi(self, calibrationUI):
        calibrationUI.setWindowTitle(QCoreApplication.translate("calibrationUI", u"Calibration UI", None))
        self.actionReference_Axis.setText(QCoreApplication.translate("calibrationUI", u"Reference Axis", None))
        self.actionReboot_System.setText(QCoreApplication.translate("calibrationUI", u"Reboot System", None))
        self.connectButton.setText(QCoreApplication.translate("calibrationUI", u"Connect", None))
        self.speedLabel.setText(QCoreApplication.translate("calibrationUI", u"Speed", None))
        self.zAxisLabel.setText(QCoreApplication.translate("calibrationUI", u"Z-Axis", None))
        self.zAxisUnitLabel.setText(QCoreApplication.translate("calibrationUI", u"mm", None))
        self.stepSizeLabel.setText(QCoreApplication.translate("calibrationUI", u"Step-Size", None))
        self.stepSizeUnitLabel.setText(QCoreApplication.translate("calibrationUI", u"mm", None))
        self.speedUnitLabel.setText(QCoreApplication.translate("calibrationUI", u"mm/s", None))
        self.Up.setText(QCoreApplication.translate("calibrationUI", u"Up", None))
        self.Move.setText(QCoreApplication.translate("calibrationUI", u"Move", None))
        self.Down.setText(QCoreApplication.translate("calibrationUI", u"Down", None))
        self.Tabs.setTabText(self.Tabs.indexOf(self.Settings), QCoreApplication.translate("calibrationUI", u"Movement Settings", None))
        self.sweepPushButton.setText(QCoreApplication.translate("calibrationUI", u"Start Calibration", None))
        self.referenceAxisPushButton.setText(QCoreApplication.translate("calibrationUI", u"Calibrate Axis", None))
        self.nSweepsLabel.setText(QCoreApplication.translate("calibrationUI", u"N Sweeps", None))
        self.measuringTImeLabel.setText(QCoreApplication.translate("calibrationUI", u"Measuring Time", None))
        self.calibrationTimeLabel_2.setText(QCoreApplication.translate("calibrationUI", u"Calibration Time", None))
        self.nsweepUnitLabel.setText(QCoreApplication.translate("calibrationUI", u"int", None))
        self.measuringTimeUnitLabel.setText(QCoreApplication.translate("calibrationUI", u"sec", None))
        self.calibrationTimeUnitLabel.setText(QCoreApplication.translate("calibrationUI", u"sec", None))
        self.noOfMeasurementStops.setText(QCoreApplication.translate("calibrationUI", u"No. of Measurement Stop", None))
        self.nMeasurementUnitLabel.setText(QCoreApplication.translate("calibrationUI", u"int", None))
        self.maxSweepLabel.setText(QCoreApplication.translate("calibrationUI", u"Max Sweep Value", None))
        self.maxSweepDistanceUnitLabel.setText(QCoreApplication.translate("calibrationUI", u"mm", None))
        self.fMeasurementHeightLabel.setText(QCoreApplication.translate("calibrationUI", u"First Measurement Height", None))
        self.fMeasurementHeightUnitLabel.setText(QCoreApplication.translate("calibrationUI", u"mm", None))
        self.minSweepLabel.setText(QCoreApplication.translate("calibrationUI", u"Min Sweep Value", None))
        self.minSweepDistanceUnitLabel.setText(QCoreApplication.translate("calibrationUI", u"mm", None))
        self.Tabs.setTabText(self.Tabs.indexOf(self.Calibration), QCoreApplication.translate("calibrationUI", u"Calibration", None))
        self.pausePushButton_2.setText(QCoreApplication.translate("calibrationUI", u"Pause", None))
        self.currentSweepNumberLabel.setText(QCoreApplication.translate("calibrationUI", u"Current Calibration Run", None))
        self.viewLogCheckBox.setText(QCoreApplication.translate("calibrationUI", u"View Log", None))
        self.menuMenu.setTitle(QCoreApplication.translate("calibrationUI", u"Menu", None))
    # retranslateUi

