import time
from time import sleep

import pandas as pd
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QThread
from PySide6.QtCore import QObject, Slot, Signal, QRunnable
from pipython import GCSDevice
from typing import Union
from pipython.pitools import pitools


class WorkerSignals(QObject):
    connection_status = Signal(int)
    isThreadRunningSignal = Signal(bool)
    zAxisPosition = Signal(float)
    speedValue = Signal(float)
    minValue = Signal(float)
    maxValue = Signal(float)
    nSweep = Signal(int)
    haltTime = Signal(float)
    stepSizeValue = Signal(float)


class PiWorker(QThread):
    STEP_SIZE = 1.0
    CONTROLLER_NUMBER = 'C-663'
    DEFAULT_SPEED = 3.0
    DEFAULT_ZAXIS_POSITION = 150
    STAGE_NUMBER = 'M-414.32S'

    def __init__(self, function=None, *args, **kwargs):
        super(PiWorker, self).__init__()

        self.serial_number = None
        self.piDevice: Union[GCSDevice, None] = None
        self.args = args
        self.kwargs = kwargs
        self.function = function
        self.deviceConnected = False

        # Class Specific Flags
        self.isThreadRunning = False
        self.signals = WorkerSignals()

        self.isThreadPaused: bool = False
        self.isThreadKilled: bool = False

    @Slot(int)
    def connectButtonStatus(self, state):
        pass

    @Slot()
    def connectDevice(self):
        try:
            self.piDevice = GCSDevice(self.CONTROLLER_NUMBER)
            self.serial_number = self.piDevice.EnumerateUSB(self.CONTROLLER_NUMBER)[0]
            self.piDevice.ConnectUSB(self.serial_number)
            pitools.startup(self.piDevice, stages=[self.STAGE_NUMBER], refmodes=['FNL'])
            self.piDevice = self.piDevice
            self.deviceConnected = True
            self.signals.connection_status.emit(1)

        except Exception as e:
            self.signals.connection_status.emit(0)
            raise e

    def changeState(self, state):
        self.isThreadRunning = state
        self.signals.isThreadRunningSignal.emit(self.isThreadRunning)

    def pause(self):
        self.isThreadPaused = not self.isThreadPaused

    def kill(self):
        self.isThreadKilled = True
        self.piDevice.CloseConnection()
        self.piDevice = None
        self.signals.connection_status.emit(2)
        self.isThreadRunning = False

    def getPosition(self):
        return self.piDevice.qPOS('1')['1']

    def getSpeed(self):
        return self.piDevice.qVEL('1')['1']
    def run(self):
        QApplication.processEvents()
        self.connectDevice()

    @Slot(float)
    def set_z_axis_position(self, position):
        self.signals.zAxisPosition = position

    @Slot(float)
    def set_speed(self, speed):
        self.signals.speedValue = speed

    @Slot(float)
    def set_step_size(self, step_size):
        self.signals.stepSizeValue = step_size

    @Slot()
    def move(self):
        try:

            self.piDevice.VEL('1', self.signals.speedValue)
            self.piDevice.MOV('1', self.signals.zAxisPosition)
            print("Moving at position {}, at speed {}".format(self.signals.zAxisPosition, self.signals.speedValue))
            if pitools.ontarget(self.piDevice, '1'):
                self.signals.zAxisPosition.emit(self.getPosition())
                print("Reached target position: {}".format(self.signals.zAxisPosition))
        except Exception as e:
            return e

    @Slot()
    def moveUp(self):
        try:

            self.piDevice.VEL('1', self.signals.speedValue)
            self.piDevice.MVR('1', self.signals.stepSizeValue)
            print("Moving at position {}, at speed {}".format(self.signals.zAxisPosition, self.signals.speedValue))
            print(f"{self.getPosition()} {self.signals.zAxisPosition}")
            # self.signals.zAxisPosition.emit(self.getPosition())

        except Exception as e:
            raise e

    @Slot()
    def moveDown(self):

        self.piDevice.VEL('1', self.signals.speedValue)
        self.piDevice.MOV('1', self.signals.zAxisPosition)
        print("Moving at position {}, at speed {}".format(self.signals.zAxisPosition, self.signals.speedValue))

    @Slot()
    def pause(self):
        # self.piDevice.VEL('1', 0)
        try:
            self.isThreadPaused = not self.isThreadPaused
            self.piDevice.HLT('1')
            self.piDevice.signals.zAixisPosition.emit(self.getPosition())
        except Exception as GCSError:
            raise GCSError


class Worker(QThread):
    resultReady = Signal()

    def __init__(self, function, *args, **kwargs):
        super(Worker, self).__init__()
        self.function = function
        self.args = args
        self.kwargs = kwargs

    @Slot()
    def run(self):
        self.function(*self.args, **self.kwargs)
