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
    """

    WorkerSignals Class

    This class defines the signals emitted by a worker object.

    Attributes:
    - connection_status: Signal emitted when the connection status changes.
    - zAxisPosition: Signal emitted when the z-axis position changes.
    - speedValue: Signal emitted when the speed value changes.
    - minValue: Signal emitted when the minimum value changes.
    - maxValue: Signal emitted when the maximum value changes.
    - nSweep: Signal emitted when the number of sweeps changes.
    - haltTime: Signal emitted when the halt time changes.
    - stepSizeValue: Signal emitted when the step size value changes.
    - finished: Signal emitted when the worker has finished its task.
    - m_finished: Signal emitted when the worker has finished its sub-task.

    """

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
    """
    Python class: PiWorker

    This class is responsible for controlling the movement of a device along the z-axis using a PI controller. It provides methods for connecting the device, setting various parameters,
    * and executing movement commands.

    Attributes:
        STEP_SIZE (float): The step size for moving the device along the z-axis.
        CONTROLLER_NUMBER (str): The controller number for the PI device.
        DEFAULT_SPEED (float): The default speed for moving the device along the z-axis.
        DEFAULT_ZAXIS_POSITION (int): The default position of the z-axis.
        STAGE_NUMBER (str): The stage number of the PI device.

    Args:
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.

    Methods:

        __init__(self, function=None, *args, **kwargs)
            Initializes a new instance of the PiWorker class.

        connectDevice(self) -> None
            Connects the device to the PI controller.

        changeState(self, state: bool) -> None
            Changes the state of the thread.

        pause(self) -> None
            Toggles the paused state of the thread and stops the motion of the device.

        kill(self) -> None
            Kills the thread and closes the connection to the device.

        getPosition(self) -> float
            Retrieves the current position of the device along the z-axis.

        getSpeed(self) -> float
            Retrieves the current speed of the device.

        run(self) -> None
            Starts the execution of the thread.

        set_z_axis_position(self, position: float) -> None
            Sets the position of the z-axis.

        set_speed(self, speed: float) -> None
            Sets the speed of the device.

        set_step_size(self, step_size: float) -> None
            Sets the step size for moving the device along the z-axis.

        set_min_sweep(self, min_value: float) -> None
            Sets the minimum value for the sweep motion.

        set_max_sweep(self, max_value: float) -> None
            Sets the maximum value for the sweep motion.

        set_n_sweep(self, n_sweep: float) -> None
            Sets the number of times the sweep motion should be performed.

        set_halt_time(self, halt_time: float) -> None
            Sets the halt time for the sweep motion.

        set_calibration_time(self, calibration_time: float) -> None
            Sets the calibration time for position readings during the sweep motion.

        move(self) -> None
            Moves the device to the specified position with the specified speed.

        moveUp(self) -> None
            Moves the device in the positive direction along the z-axis.

        moveDown(self) -> None
            Moves the device in the negative direction along the z-axis.

        pause(self) -> None
            Toggles the paused state of the thread and stops the motion of the device.

        sweep(self) -> None
            Performs a sweep motion with the device, collecting position readings at each step.

    """
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
        self._zAxisPositionValue = None
        self._speedValue = None
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


    def initializeConnection(self):
        self.deviceConnected = True
        self.changeState(True)
        self.signals.connection_status.emit(1)

    @Slot()
    def connectDevice(self):
        try:
            self.piDevice = GCSDevice(self.CONTROLLER_NUMBER)
            self.serial_number = self.piDevice.EnumerateUSB(self.CONTROLLER_NUMBER)[0]
            self.piDevice.ConnectUSB(self.serial_number)
            pitools.startup(self.piDevice, stages=[self.STAGE_NUMBER], refmodes=['FNL'])
            self.piDevice = self.piDevice
            self.initializeConnection()


        except Exception as e:
            self.signals.connection_status.emit(0)
            raise e

    def changeState(self, state):
        self.isThreadRunning = state

    def pause(self):
        self.isThreadPaused = not self.isThreadPaused
        if self.piDevice:
            self.piDevice.STP('1')
        self.signals.zAxisPosition.emit(self.getPosition())

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
        if self.piDevice is None:
            self.connectDevice()

        while not self.isThreadKilled:
            QApplication.processEvents()
            if self.isThreadPaused:
                continue


            time.sleep(0.2)

################# Setters #################################################################################################################################

    @Slot(float)
    def set_z_axis_position(self, position):
        self._zAxisPositionValue = position

    @Slot(float)
    def set_speed(self, speed):
        self._speedValue = speed

    @Slot(float)
    def set_step_size(self, step_size):
        self.stepSizeValue = step_size

    @Slot(float)
    def set_min_sweep(self, min_value):
        self.minValue = min_value

    @Slot(float)
    def set_max_sweep(self, max_value):
        self.maxValue = max_value

    @Slot(int)
    def set_n_sweep(self, n_sweep):
        self.nSweepValue = n_sweep

    @Slot(float)
    def set_halt_time(self, halt_time):
        self.haltTimeValue = halt_time

    @Slot(float)
    def set_calibration_time(self, calibration_time):
        self.calibrationTimeValue = calibration_time

######### Move Functions ###############################################################################################

    @Slot(float)
    def move_to_position(self, position):

        try:

            if position is None:
                raise Exception("Position is None")

            self.piDevice.VEL('1', self._speedValue)
            self.piDevice.MOV('1', position)
            print(f"Moving at position {position} mm")

        except Exception as e:
            self.signals.m_finished.emit(False)
            return e
        finally:
            self.signals.m_finished.emit(True)


    @Slot()
    def move(self):
        """
        Method: move
        Moves the z-axis to a specified position with specified speed.
        Parameters:
            None
        Returns:
            None
        Raises:
            Exception: If an error occurs while attempting to move the z-axis.
        """

        try:
            self.move_to_position(self._zAxisPositionValue)
            while self.piDevice.IsMoving('1')['1'] == 1:
                self.signals.zAxisPosition.emit(self.getPosition())
        except Exception as e:
            self.signals.m_finished.emit(False)
            return e
        finally:
            self.signals.m_finished.emit(True)




    @Slot()
    def moveUp(self):
        """
        Method: moveUp

        Moves the z-axis in the positive direction by a specified position and speed.

        Parameters:
            None

        Returns:
            None

        Raises:
            Exception: If an error occurs while attempting to move the z-axis.

        Example usage:
            moveUp()

        """
        newPosition = self.getPosition() - self.stepSizeValue
        self.mutex.lock()
        try:
            self.move_to_position(newPosition)
            while self.piDevice.IsMoving('1')['1'] == 1:
                self.signals.zAxisPosition.emit(self.getPosition())
        finally:
            self.mutex.unlock()

    @Slot()
    def moveDown(self):
        new_position = self.getPosition() + self.stepSizeValue
        self.mutex.lock()
        try:
            self.move_to_position(new_position)
            while self.piDevice.IsMoving('1')['1'] == 1:
                self.signals.zAxisPosition.emit(self.getPosition())
        finally:
            self.mutex.unlock()

    @Slot()
    def pause(self):
        self.isThreadPaused = not self.isThreadPaused
        if self.piDevice:
            self.piDevice.STP('1')

    @Slot()
    def sweep(self):
        """

        This method performs a sweep motion using the piDevice. It moves the device from the minimum position to the maximum position multiple times, collecting position readings at each step
        *. The collected position readings are then saved to a CSV file named "posReadings50.csv".

        Parameters:

        N/A

        Returns:

        N/A

        """
        self.piDevice.VEL('1', self._speedValue)

        for i in range(int(self.nSweepValue)):
            self.posReadingDict['N'].append(i + 1)

            # Start moving to the minimum position
            self.move_to_position(self.minValue)
            pitools.waitontarget(self.piDevice, '1', postdelay=self.haltTimeValue)
            sleep(self.calibrationTimeValue)
            self.posReadingDict['MinPositionReading'].append(self.piDevice.qPOS('1')['1'])
            sleep(self.calibrationTimeValue)
            # Document minimum position readings

            # Start moving to the maximum position
            # PILogger.info("Moving to maximum position: {}".format(self.maxValue))
            self.move_to_position(self.maxValue)
            pitools.waitontarget(self.piDevice, '1', postdelay=self.haltTimeValue)
            # PILogger.info('Moved to max position: {}'.format(self.maxValue))

            # Document maximum position readings
            # PILogger.info("Getting maximum position readings")
            sleep(self.calibrationTimeValue)
            self.posReadingDict['MaxPositionReading'].append(self.piDevice.qPOS('1')['1'])
            sleep(self.calibrationTimeValue)

        self.df = pd.DataFrame.from_dict(self.posReadingDict)
        self.df.to_csv("posReadings50.csv", index=False)
