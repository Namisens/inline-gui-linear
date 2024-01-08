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
    z_axis_position = Signal(float)
    speed_value = Signal(float)
    minValue = Signal(float)
    maxValue = Signal(float)
    nSweep = Signal(int)
    haltTime = Signal(float)
    stepSizeValue = Signal(float)
    thread_finished = Signal(bool)
    m_finished = Signal(int)
    current_calibration_number = Signal(int)


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


    def __init__(self, n_sweep_value, n_measurements_value,step_size,
                 measurement_time_value,min_value, max_value, f_measurement_height_value,
                 calibration_time_value, speed_value,*args, **kwargs):
        super(PiWorker, self, ).__init__()

        self.serial_number = None
        self.piDevice: Union[GCSDevice, None] = None
        self.stepSizeValue = step_size
        self._zAxisPositionValue = None
        self._speedValue = speed_value
        self.args = args
        self.kwargs = kwargs
        self.nSweepValue = n_sweep_value
        self.measurementTimeValue = measurement_time_value
        self.minValue = min_value
        self.maxValue = max_value
        self.nMeasurementsValue = n_measurements_value
        self.fMeasurementHeightValue = f_measurement_height_value
        self.calibrationTimeValue = calibration_time_value
        self.next_action = None

        self.models = calibrationUIModel()
        self.mutex = QMutex()
        self.posReadingDict = {'N': [], 'MinPositionReading': [], 'MaxPositionReading': []}

        # Class Specific Flags
        self.isThreadRunning = False
        self.signals = WorkerSignals()
        self.isThreadPaused: bool = False
        self.isThreadKilled: bool = False


    def initializeConnection(self):
        self.isThreadRunning = True
        self.signals.connection_status.emit(1)
        self.signals.z_axis_position.emit(self.getPosition())
        self.signals.speed_value.emit(self.getSpeed())

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
        self.signals.z_axis_position.emit(self.getPosition())

    def kill(self):
        self.isThreadKilled = True
        if self.piDevice:
            self.piDevice.CloseConnection()
            self.piDevice = None
        self.signals.connection_status.emit(2)
        self.isThreadRunning = False
        self.signals.thread_finished.emit(True)

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
            if not self.isThreadPaused:
                if self.next_action=='move':
                    self.move()
                elif self.next_action=='moveUp':
                    self.moveUp()
                elif self.next_action=='moveDown':
                    self.moveDown()
                elif self.next_action=='sweep':
                    self.sweep()
                elif self.next_action=='calibrate':
                    self.calibrate_axis()
                else:
                    continue
            else:
                if self.piDevice.IsMoving('1')['1'] == 1:
                    self.piDevice.STP('1')
                self.signals.z_axis_position.emit(self.getPosition())

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

    def set_f_measurement_height(self, f_measurement_height):
        self.fMeasurementHeightValue = f_measurement_height

    @Slot(float)
    def set_n_measurement_stops(self, n_measurements):
        self.nMeasurementsValue = n_measurements

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
    def set_measurement_time(self, measurement_time):
        self.measurementTimeValue = measurement_time

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
            raise e


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
            self.signals.m_finished.emit(2)
            while self.piDevice.IsMoving('1')['1'] == 1:
                self.signals.z_axis_position.emit(self.getPosition())
            self.signals.m_finished.emit(1)
            self.next_action = None
        except Exception as e:
            self.signals.m_finished.emit(0)
            return e

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
        self.signals.m_finished.emit(2)
        try:
            self.move_to_position(newPosition)
            while self.piDevice.IsMoving('1')['1'] == 1:
                self.signals.z_axis_position.emit(self.getPosition())
            self.signals.m_finished.emit(1)
        except Exception as e:
            self.signals.m_finished.emit(0)
            raise e
        finally:
            self.mutex.unlock()
            self.next_action = None

    @Slot()
    def moveDown(self):
        """
        Moves the object down by the specified step size.

        Parameters:
            None

        Returns:
            None

        """
        new_position = self.getPosition() + self.stepSizeValue
        self.mutex.lock()
        self.signals.m_finished.emit(2)
        try:
            self.move_to_position(new_position)
            while self.piDevice.IsMoving('1')['1'] == 1:
                self.signals.z_axis_position.emit(self.getPosition())
            self.signals.m_finished.emit(1)
        except Exception as e:
            self.signals.m_finished.emit(0)
            raise e
        finally:
            self.mutex.unlock()
            self.next_action = None



    def pause(self):
        self.isThreadPaused = not self.isThreadPaused
        # print(self.isThreadPaused)
        # if self.piDevice.IsMoving('1')['1'] == 1:
        #     self.piDevice.STP('1')
        # self.signals.z_axis_position.emit(self.getPosition())
        self.next_action = None

    def calibrate_axis(self):
        self.piDevice.FRF('1')
        self.next_action = None


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
        try:
            self.signals.m_finished.emit(2)

            for i in range(int(self.nSweepValue)):
                QApplication.processEvents()
                self.signals.current_calibration_number.emit(i + 1)
                self.posReadingDict['N'].append(i + 1)

                if not self.isThreadPaused:
                    try:
                    # Start moving to the minimum position
                        if self.nMeasurementsValue and self.fMeasurementHeightValue != 0.0 or None:

                            self.move_to_position(self.fMeasurementHeightValue)
                            pitools.waitontarget(self.piDevice, '1', postdelay=self.measurementTimeValue)
                            self.signals.z_axis_position.emit(self.getPosition())

                            remainingHeight = abs(self.fMeasurementHeightValue - self.minValue)

                            while(self.getPosition() !=self.minValue):

                                for j in range(1,int(self.nMeasurementsValue+1)):
                                    moveLocation:float = self.fMeasurementHeightValue - j*(remainingHeight/self.nMeasurementsValue)
                                    self.move_to_position(moveLocation)
                                    pitools.waitontarget(self.piDevice, '1', postdelay=self.measurementTimeValue)
                                    self.signals.z_axis_position.emit(self.getPosition())

                            self.move_to_position(self.maxValue)

                            pitools.waitontarget(self.piDevice, '1', postdelay=self.calibrationTimeValue)

                        else:
                            self.justSweep()


                    except Exception as e:
                        raise e

                    finally:
                        self.signals.m_finished.emit(1)
                        self.signals.z_axis_position.emit(self.getPosition())
                        self.signals.m_finished.emit(1)

                else:
                    self.signals.m_finished.emit(3)
                    break

        finally:
            self.next_action = None




    def justSweep(self):
        self.move_to_position(self.minValue)
        pitools.waitontarget(self.piDevice, '1', postdelay=self.measurementTimeValue)

        self.move_to_position(self.maxValue)
        pitools.waitontarget(self.piDevice, '1', postdelay=self.measurementTimeValue)
