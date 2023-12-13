import sys
from PySide6.QtCore import Slot, QThreadPool, QThread
from PySide6.QtWidgets import QApplication, QMainWindow
from Threads.piMotorThread import PiWorker
from models.mainModel import calibrationUIModel
from views.mainView import Ui_calibrationUI


class mainWindow(QMainWindow, Ui_calibrationUI):
    STEP_SIZE = 1.0
    CONTROLLER_NUMBER = 'C-663'
    DEFAULT_SPEED = 3.0
    DEFAULT_ZAXIS_POSITION = 150
    STAGE_NUMBER = 'M-414.32S'

    def __init__(self, parent=None):
        super(mainWindow, self).__init__(parent)
        self.threadPool = QThreadPool()
        self.connection_status = False
        self.ui = Ui_calibrationUI()
        self.ui.setupUi(self)
        self.worker = PiWorker()
        self.thread = QThread()
        self.is_already_connected = False

        # Connect Signals
        self.worker.signals.connection_status.connect(self.update_progress)
        self.ui.connectButton.clicked.connect(self._connect)

        ######################################### Movement Tab #########################################

        # Position Spin Box Signals
        self.ui.zAxisSpin.valueChanged.connect(self.worker.set_z_axis_position)
        self.ui.stepSizeSpin.valueChanged.connect(self.worker.set_step_size)

        # Speed Spin Box Signals
        self.ui.speedSpin.valueChanged.connect(self.worker.set_speed)
        self.worker.signals.stepSizeValue.connect(self.ui.stepSizeSpin.setValue)

        # Move Button Signals
        self.ui.Move.clicked.connect(self.move_clicked)
        self.ui.Move.clicked.connect(self.worker.move)

        # Up Button Signals
        self.ui.Up.clicked.connect(self.up_clicked)
        self.ui.Up.clicked.connect(self.worker.moveUp)

        # Down Button Signals
        self.ui.Down.clicked.connect(self.worker.moveDown)
        self.ui.Down.clicked.connect(self.down_clicked)

        # Pause Button Signals
        self.ui.pausePushButton_2.clicked.connect(self.pause_clicked)
        self.ui.pausePushButton_2.clicked.connect(self.worker.pause)
        self.worker.signals.zAxisPosition.connect(self.pause_clicked)

        # Finished Movement Signal, called after every movement
        self.worker.signals.m_finished.connect(self.update_movement)

        ################## Calibration Tab########################################################

        self.ui.sweepPushButton.clicked.connect(self.worker.sweep)

        # Set Calibration Parameters
        self.ui.nSweepSpin.valueChanged.connect(self.worker.set_n_sweep)
        self.ui.measuringTImeSpin.valueChanged.connect(self.worker.set_halt_time)
        self.ui.calibrationTimeSpin.valueChanged.connect(self.worker.set_calibration_time)
        self.ui.maxSweepSpin.valueChanged.connect(self.worker.set_max_sweep)
        self.ui.minSweepSpin.valueChanged.connect(self.worker.set_min_sweep)

    def move_clicked(self):
        self.ui.pausePushButton_2.setEnabled(True)

    def update_movement(self, value):
        self.ui.pausePushButton_2.setEnabled(False)
        self.statusBar().showMessage("Moved to ".format(self.ui.zAxisSpin.value()))

    def pause_clicked(self, value):
        self.ui.zAxisSpin.setValue(value)

    @Slot()
    def up_clicked(self):
        self.ui.zAxisSpin.setValue(self.ui.zAxisSpin.value() - self.ui.stepSizeSpin.value())
        self.statusBar().showMessage("Moving to {}".format(self.ui.zAxisSpin.value()))

    @Slot()
    def down_clicked(self):
        self.ui.zAxisSpin.setValue(self.ui.zAxisSpin.value() + self.ui.stepSizeSpin.value())
        self.statusBar().showMessage("Moving to {}".format(self.ui.zAxisSpin.value()), 2000)

    @Slot(float)
    def update_z_axis_position(self, value):
        return self.ui.zAxisSpin.setValue(value)

    def update_progress(self, value):
        if value == 1:

            # Update Connection Button Text
            self.ui.statusbar.showMessage("Connected", 5000)
            self.ui.connectButton.setText('Disconnect')
            # print(self.piWorker.isRunning())

            # Update UI Connection Status
            self.toggleButtons(True)
            print("Thread status from update_progress {}".format(self.thread.isRunning()))

            # Get Motor Position and Speed Values from the controller
            self.ui.zAxisSpin.setValue(self.worker.getPosition())
            self.ui.speedSpin.setValue(float(self.worker.getSpeed()))

        elif value == 2:
            self.ui.statusbar.showMessage("Disconnected", 5000)
            self.toggleButtons(False)
            self.ui.statusbar.showMessage(f"Disconnected")
            self.ui.connectButton.setText('Connect')

        else:
            self.ui.statusbar.showMessage(f"Unable to find any controllers. "
                                          f"Please check the connection and try again.")

    @Slot()
    def _connect(self):
        if self.connection_status:
            self.worker.kill()
            print(self.thread.isFinished(), self.thread.isRunning())

        else:
            self.attach_worker()
            print(self.thread.isFinished(), self.thread.isRunning())

    def attach_worker(self):
        if not self.is_already_connected:
            self.worker.moveToThread(self.thread)
            self.thread.started.connect(self.worker.run)
            self.worker.signals.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            self.worker.signals.finished.connect(self.thread.quit)
            self.thread.start()
            self.is_already_connected = True
        else:

            self.thread.start()

    def toggleButtons(self, state):

        # Update Connection Flag
        self.connection_status = state
        # Update UI Connection Status
        self.ui.zAxisSpin.setEnabled(state)
        self.ui.speedSpin.setEnabled(state)
        self.ui.stepSizeSpin.setEnabled(state)
        self.ui.sweepPushButton.setEnabled(state)
        self.ui.referenceAxisPushButton.setEnabled(state)
        self.ui.Up.setEnabled(state)
        self.ui.Down.setEnabled(state)
        self.ui.Move.setEnabled(state)
        self.ui.nSweepSpin.setEnabled(state)
        self.ui.measuringTImeSpin.setEnabled(state)
        self.ui.calibrationTimeSpin.setEnabled(state)
        self.ui.maxSweepSpin.setEnabled(state)
        self.ui.minSweepSpin.setEnabled(state)
        self.ui.maxSweepSpin.setEnabled(state)
        self.ui.fMeasurementHeightSpinValue.setEnabled(state)
        self.ui.nMeasurementStopSpinValue.setEnabled(state)


def main():
    app = QApplication(sys.argv)
    window = mainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
