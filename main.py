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
        self.piDevice = None
        self.model = calibrationUIModel()
        self.ui = Ui_calibrationUI()
        self.ui.setupUi(self)
        self.worker = PiWorker()
        self.deviceConnected = False
        self.thread = QThread()

        # Signals
        self.worker.signals.connection_status.connect(self.update_progress)
        self.ui.connectButton.clicked.connect(self._connect)
        self.ui.Down.clicked.connect(self.down_clicked)
        self.ui.Up.clicked.connect(self.up_clicked)
        self.ui.zAxisSpin.valueChanged.connect(self.worker.set_z_axis_position)
        self.ui.speedSpin.valueChanged.connect(self.worker.set_speed)
        self.worker.signals.stepSizeValue.connect(self.ui.stepSizeSpin.setValue)
        self.ui.Move.clicked.connect(self.worker.move)
        self.ui.Up.clicked.connect(self.worker.moveUp)
        self.ui.Down.clicked.connect(self.worker.moveDown)
        self.ui.pausePushButton_2.clicked.connect(self.worker.pause)
        # self.worker.signals.zAxisPosition.connect(self.update_z_axis_position)

        # self.show()

    @Slot()
    def up_clicked(self):

        self.ui.zAxisSpin.setValue(self.ui.zAxisSpin.value() - self.ui.stepSizeSpin.value())

    @Slot()
    def down_clicked(self):
        self.ui.zAxisSpin.setValue(self.ui.zAxisSpin.value() + self.ui.stepSizeSpin.value())

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

            # print("Thread status from update_progress {}".format(self.workerThread.isRunning()))

            # Enable Buttons and Line editing

            self.toggleButtons(True)
            self.ui.zAxisSpin.setValue(self.worker.getPosition())
            self.ui.speedSpin.setValue(float(self.worker.getSpeed()))

        elif value == 2:
            self.ui.statusbar.showMessage("Disconnected", 5000)

        else:
            self.ui.statusbar.showMessage(f"Unable to find any controllers. "
                                          f"Please check the connection and try again.")

    @Slot()
    def _connect(self):
        if self.model.connectButtonState:

            self.ui.statusbar.showMessage(f"Disconnected")
            self.ui.connectButton.setText('Connect')
            self.toggleButtons(False)
            self.worker.kill()

        else:
            self.attach_worker()
            print(self.thread.isFinished(), self.thread.isRunning())

    def attach_worker(self):
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.thread.start()
        self.worker.signals.connection_status.connect(self.update_progress)
        self.thread.finished.connect(self.thread.deleteLater)

    def toggleButtons(self, state):
        # Update UI Connection Status
        self.model.connectButtonState = state
        self.ui.zAxisSpin.setEnabled(state)
        self.ui.speedSpin.setEnabled(state)
        self.ui.stepSizeSpin.setEnabled(state)
        self.ui.sweepPushButton.setEnabled(state)
        self.ui.referenceAxisPushButton.setEnabled(state)
        self.ui.Up.setEnabled(state)
        self.ui.Down.setEnabled(state)
        self.ui.Move.setEnabled(state)
        self.ui.pausePushButton_2.setEnabled(state)
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
