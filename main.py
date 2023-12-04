import sys

from PySide6.QtGui import Qt
from PySide6.QtWidgets import QApplication, QMainWindow
from pipython import GCSDevice
from typing import Union

from pipython.pitools import pitools

from models.mainModel import calibrationUIModel
from views.mainView import Ui_calibrationUI
from PySide6.QtCore import Slot, Signal, QThreadPool, QThread

STEP_SIZE = 1.0
CONTROLLER_NUMBER = 'C-663'
DEFAULT_SPEED = 3.0
DEFAULT_ZAXIS_POSITION = 150
STAGE_NUMBER = 'M-414.32S'


class PIThread(QThread):
    connection_status = Signal(int)

    def __init__(self):
        super().__init__()
        self.piDevice: Union[None, GCSDevice] = None

    def run(self):
        try:
            self.piDevice = GCSDevice(CONTROLLER_NUMBER)
            serial_number = self.piDevice.EnumerateUSB()
            if len(serial_number) == 0:
                self.connection_status.emit(0)
            else:
                self.piDevice = self.piDevice.ConnectUSB(serial_number[0])
                # PILogger.info('Initializing device...')
                pitools.startup(self.piDevice, stages=[STAGE_NUMBER], refmodes=['FNL'])
                self.connection_status.emit(1)
        except Exception as e:
            print(e)
            self.connection_status.emit(0)

    def close(self):
        self.piDevice.CloseConnection()


class mainWindow(QMainWindow, Ui_calibrationUI):
    def __init__(self):
        super(mainWindow, self).__init__()
        self.model = calibrationUIModel()
        self.ui = Ui_calibrationUI()
        self.ui.setupUi(self)
        self.workerThreads = []
        self.workerThread = PIThread()

        # Signals
        self.ui.connectButton.clicked.connect(self._connect)
        self.workerThread.connection_status.connect(self.update_progress)

    def update_progress(self, value):
        if value == 1:
            self.ui.statusbar.showMessage(f"Connected")
            self.ui.connectButton.setText('Disconnect')
            self.model.connectButtonState = True

            # Enable Buttons and Line editing
            self.model.connectButtonState = True
            self.model.piDevice = True
            self.ui.zAxisSpin.setEnabled(True)
            self.ui.speedSpin.setEnabled(True)
            self.ui.stepSizeSpin.setEnabled(True)
            self.ui.sweepPushButton.setEnabled(True)
            self.ui.referenceAxisPushButton.setEnabled(True)
            self.ui.Up.setEnabled(True)
            self.ui.Down.setEnabled(True)
            self.ui.Move.setEnabled(True)
            self.ui.pause.setEnabled(True)
            self.ui.nSweepSpin.setEnabled(True)
            self.ui.measuringTImeSpin.setEnabled(True)
            self.ui.calibrationTimeSpin.setEnabled(True)
            self.ui.maxSweepSpin.setEnabled(True)
            self.ui.minSweepSpin.setEnabled(True)
            self.ui.maxSweepSpin.setEnabled(True)

        else:
            self.ui.statusbar.showMessage(f"Unable to find any controllers. Please check the connection and try again.")

    @Slot()
    def _connect(self):
        if self.model.connectButtonState:
            self.workerThread.close()
            self.ui.statusbar.showMessage(f"Disconnected")
            self.ui.connectButton.setText('Connect')
            self.model.connectButtonState = False
            self.model.piDevice = None
            self.ui.zAxisSpin.setEnabled(False)
            self.ui.speedSpin.setEnabled(False)
            self.ui.Up.setEnabled(False)
            self.ui.Down.setEnabled(False)
            self.ui.Move.setEnabled(False)
            self.ui.pause.setEnabled(False)
            self.ui.nSweepSpin.setEnabled(False)
            self.ui.measuringTImeSpin.setEnabled(False)
            self.ui.calibrationTimeSpin.setEnabled(False)
            self.ui.maxSweepSpin.setEnabled(False)
            self.ui.minSweepSpin.setEnabled(False)
            self.ui.maxSweepSpin.setEnabled(False)
        else:
            self.workerThread.start()
        # if self.model.connectButtonState:
        #     # Deactivate Buttons and Line editing
        #     # PILogger.info('Disconnecting...')
        #     self.model.piDevice.CloseConnection()
        #     self.model.connectButtonState = False
        #     self.ui.connectButton.setText('Connect')
        #     # PILogger.info('disconnected')
        #     self.ui.statusbar.showMessage('Disconnected!', 2000)
        #     self.model.piDevice = None
        #     self.ui.zAxisSpin.setEnabled(False)
        #     self.ui.speedSpin.setEnabled(False)
        #     self.ui.Up.setEnabled(False)
        #     self.ui.Down.setEnabled(False)
        #     self.ui.Move.setEnabled(False)
        #     self.ui.pause.setEnabled(False)
        #     self.ui.nSweepSpin.setEnabled(False)
        #     self.ui.measuringTImeSpin.setEnabled(False)
        #     self.ui.calibrationTimeSpin.setEnabled(False)
        #     self.ui.maxSweepSpin.setEnabled(False)
        #     self.ui.minSweepSpin.setEnabled(False)
        #     self.maxSweepSpin.setEnabled(False)
        #
        # else:
        #     self.model.piDevice = GCSDevice(CONTROLLER_NUMBER)
        #     # PILogger.info('Searching for controllers...')
        #     serial_number = self.model.piDevice.EnumerateUSB()
        #     if len(serial_number) == 0:
        #         self.ui.statusbar.showMessage('No controllers found!', 2000)
        #     else:
        #         self.model.piDevice.ConnectUSB(serial_number[0])
        #         # PILogger.info('Connected: {}'.format(self.piDevice.qIDN().strip()))
        #
        #         # PILogger.info(self.piDevice.qIDN())
        #
        #         # PILogger.info('Initializing device...')
        #         # pitools.startup(self.piDevice, stages=[STAGE_NUMBER], refmodes=['FNL'])
        #         # PILogger.info('done!')
        #         self.ui.connectButton.setChecked(self.model.connectButtonState)
        #         self.ui.connectButton.setText('Connected')
        #         if self.model.piDevice.IsConnected():
        #             self.ui.statusbar.showMessage('Connected!', 2000)
        #             self.model.connectButtonState = True
        #
        #         # PI Device
        #         self.model.piDevice = self.model.piDevice
        #
        #         # Set Initial Values
        #         # self.zAxisPosition = self.__getPosition()
        #         # self.speedValue = self.__getSpeed()
        #         # self.stepSizeValue = self.__getStepSize()
        #         # self.zaxis.setText(str(self.zAxisPosition))
        #         # self.speed.setText(str(self.speedValue))
        #         # self.stepSizeEdit.setText(str(self.stepSizeValue))
        #
        #         # Loggers
        #         # PILogger.info(f"Current Pos: {self.__getPosition()} mm")
        #         # PILogger.info(f"Current Velocity {self.__getSpeed()} mm/sec")
        #         # PILogger.info(f"Current Step Size {self.__getStepSize()} mm")
        #
        #         # Enable Buttons and Line editing
        #         # self.model.piDevice.CloseConnection()
        #         self.model.connectButtonState = True
        #         self.model.piDevice = True
        #         self.ui.zAxisSpin.setEnabled(True)
        #         self.ui.speedSpin.setEnabled(True)
        #         self.ui.stepSizeSpin.setEnabled(True)
        #         self.ui.sweepPushButton.setEnabled(True)
        #         self.ui.referenceAxisPushButton.setEnabled(True)
        #         self.ui.Up.setEnabled(True)
        #         self.ui.Down.setEnabled(True)
        #         self.ui.Move.setEnabled(True)
        #         self.ui.pause.setEnabled(True)
        #         self.ui.nSweepSpin.setEnabled(True)
        #         self.ui.measuringTImeSpin.setEnabled(True)
        #         self.ui.calibrationTimeSpin.setEnabled(True)
        #         self.ui.maxSweepSpin.setEnabled(True)
        #         self.ui.minSweepSpin.setEnabled(True)
        #         self.ui.maxSweepSpin.setEnabled(True)

    def keyPressedEvent(self, e):
        if e.key() == Qt.Key.Key_Escape:
            self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = mainWindow()
    window.show()
    sys.exit(app.exec())

# showSTEP_SIZE = 1.0
# CONTROLLER_NUMBER = 'C-663'
#
# DEFAULT_SPEED = 3.0
# DEFAULT_ZAXIS_POSITION = 150
# STAGE_NUMBER = 'M-414.32S'
#
# # class App(QApplication):
# #     def __init__(self, sys_argv):
# #         super().__init__(sys_argv)
# #         self.model = Model()
# #         self.main_controller = MainController(self.model)
# #         self.main_view = MainView(self.model, elf.main_controller)
# #         self.main_view.show()
# #
# #
# # if __name__ == "__main__":
# #     app = App()
# #     sys.exit(app.exec())
