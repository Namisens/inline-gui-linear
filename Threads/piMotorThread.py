import time
from time import sleep

import pandas as pd
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QThread, QMutex, QMutexLocker
from PySide6.QtCore import QObject, Slot, Signal, QRunnable
from pipython import GCSDevice
from typing import Union
from pipython.pitools import pitools
from models.mainModel import calibrationUIModel


class WorkerSignals(QObject):
    connection_status = Signal(int)
    zAxisPosition = Signal(float)
    speedValue = Signal(float)
    minValue = Signal(float)
    maxValue = Signal(float)
    nSweep = Signal(int)
    haltTime = Signal(float)
    stepSizeValue = Signal(float)
    finished = Signal(bool)
    m_finished = Signal(bool)


class PiWorker(QObject):
    STEP_SIZE = 1.0
    CONTROLLER_NUMBER = 'C-663'
    DEFAULT_SPEED = 3.0
    DEFAULT_ZAXIS_POSITION = 150
    STAGE_NUMBER = 'M-414.32S'


    def __init__(self, function=None, *args, **kwargs):
        super(PiWorker, self).__init__()

        self.serial_number = None
        self.piDevice: Union[GCSDevice, None] = None
        self.stepSizeValue = None
        self.zAxisPositionValue = None
        self.speedValue = None
        self.args = args
        self.kwargs = kwargs
        self.function = function
        self.nSweepValue = None
        self.haltTimeValue = None
        self.minValue = None
        self.maxValue = None
        self.cancelTimeValue = None
        self.deviceConnected = False
        self.models = calibrationUIModel()
        self.mutex = QMutex()
        self.posReadingDict = {'N': [], 'MinPositionReading': [], 'MaxPositionReading': []}

        # Class Specific Flags
        self.isThreadRunning = False
        self.signals = WorkerSignals()

        self.isThreadPaused: bool = False
        self.isThreadKilled: bool = False

    @Slot()
    def connectDevice(self):
        try:
            self.piDevice = GCSDevice(self.CONTROLLER_NUMBER)
            self.serial_number = self.piDevice.EnumerateUSB(self.CONTROLLER_NUMBER)[0]
            self.piDevice.ConnectUSB(self.serial_number)
            pitools.startup(self.piDevice, stages=[self.STAGE_NUMBER], refmodes=['FNL'])
            self.piDevice = self.piDevice
            self.deviceConnected = True
            self.changeState(True)
            self.signals.connection_status.emit(1)


        except Exception as e:
            self.signals.connection_status.emit(0)
            raise e

    def changeState(self, state):
        self.isThreadRunning = state

    def pause(self):
        self.isThreadPaused = not self.isThreadPaused

    def kill(self):
        self.isThreadKilled = True
        self.piDevice.CloseConnection()
        self.piDevice = None
        self.signals.connection_status.emit(2)
        self.isThreadRunning = False
        self.signals.finished.emit(True)

    def getPosition(self):
        return self.piDevice.qPOS('1')['1']

    def getSpeed(self):
        return self.piDevice.qVEL('1')['1']

    @Slot()
    def run(self):
        # self.mutex.lock()
        if self.piDevice is None:
            self.connectDevice()

        while True:
            QApplication.processEvents()
            time.sleep(0.2)
            # print("Thread is running")
        # self.mutex.unlock()

################# Setters #################################################################################################################################

    @Slot(float)
    def set_z_axis_position(self, position):
        self.zAxisPositionValue = position

    @Slot(float)
    def set_speed(self, speed):
        self.speedValue = speed

    @Slot(float)
    def set_step_size(self, step_size):
        self.stepSizeValue = step_size

    def set_min_sweep(self, min_value):
        self.minValue = min_value

    def set_max_sweep(self, max_value):
        self.maxValue = max_value

    def set_n_sweep(self, n_sweep):
        self.nSweepValue = n_sweep

    def set_halt_time(self, halt_time):
        self.haltTimeValue = halt_time

    def set_calibration_time(self, calibration_time):
        self.calibrationTimeValue = calibration_time

#########Move Functions###############################################################################################

    @Slot()
    def move(self):
        try:

            self.piDevice.VEL('1', self.speedValue)
            self.piDevice.MOV('1', self.zAxisPositionValue)
            print("Moving at position {} mm, at speed {} mm/sec".format(self.zAxisPositionValue, self.speedValue))
            if pitools.ontarget(self.piDevice, '1'):
                self.signals.zAxisPosition.emit(self.getPosition())
                print("Reached target position: {}".format(self.zAxisPositionValue))
        except Exception as e:
            self.signals.m_finished.emit(False)
            return e

        finally:
            self.signals.m_finished.emit(True)

    @Slot()
    def moveUp(self):
        try:

            self.piDevice.VEL('1', self.speedValue)
            self.piDevice.MOV('1', self.zAxisPositionValue)
            print("Moving at position {} mm, at speed {} mm/sec".format(self.zAxisPositionValue, self.speedValue))
            if pitools.ontarget(self.piDevice, '1')and self.zAxisPositionValue == self.getPosition():
                self.signals.zAxisPosition.emit(self.getPosition())
                print("Reached target position: {} mm".format(self.zAxisPositionValue))

        except Exception as e:
            raise e

    @Slot()
    def moveDown(self):
        self.piDevice.VEL('1', self.speedValue)
        self.piDevice.MOV('1', self.zAxisPositionValue)
        print("Moving at position {} mm, at speed {} mm/sec".format(self.zAxisPositionValue, self.speedValue))

    @Slot()
    def pause(self):
        try:
            self.isThreadPaused = not self.isThreadPaused
            self.piDevice.STP('1')
            self.signals.zAxisPosition.emit(self.getPosition())
        except Exception as e:
            raise e

    @Slot()
    def sweep(self):
        self.piDevice.VEL('1', self.speedValue)

        for i in range(int(self.nSweepValue)):
            self.posReadingDict['N'].append(i + 1)
            # Start moving to the minimum position
            self.piDevice.MOV('1', self.minValue)
            pitools.waitontarget(self.piDevice, '1', postdelay=self.haltTimeValue)
            sleep(self.calibrationTimeValue)
            self.posReadingDict['MinPositionReading'].append(self.piDevice.qPOS('1')['1'])
            sleep(self.calibrationTimeValue)
            # Document minimum position readings

            # Start moving to the maximum position
            # PILogger.info("Moving to maximum position: {}".format(self.maxValue))
            self.piDevice.MOV('1', self.maxValue)
            pitools.waitontarget(self.piDevice, '1', postdelay=self.haltTimeValue)
            # PILogger.info('Moved to max position: {}'.format(self.maxValue))

            # Document maximum position readings
            # PILogger.info("Getting maximum position readings")
            sleep(self.calibrationTimeValue)
            self.posReadingDict['MaxPositionReading'].append(self.piDevice.qPOS('1')['1'])
            sleep(self.calibrationTimeValue)

        self.df = pd.DataFrame.from_dict(self.posReadingDict)
        self.df.to_csv("posReadings50.csv", index=False)
