import sys
from PySide6.QtCore import Slot, QThreadPool, QThread
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow
from Threads.piMotorThread import PiWorker
from views.mainView import Ui_calibrationUI


class mainWindow(QMainWindow, Ui_calibrationUI):
    STEP_SIZE = 1.0
    CONTROLLER_NUMBER = 'C-663'
    DEFAULT_SPEED = 3.0
    DEFAULT_ZAXIS_POSITION = 150
    STAGE_NUMBER = 'M-414.32S'

    def __init__(self, parent=None):
        super(mainWindow, self).__init__(parent)
        # self.threadPool = QThreadPool()
        self.app = QApplication.instance()
        self.connection_status = False
        self.ui = Ui_calibrationUI()
        self.ui.setupUi(self)
        self.worker = None
        self.thread = None
        self.keep_running = False
        self.setup_connections()
        self.setWindowIcon(QIcon('resources/NamisensLogo.jpg'))
        self.ui.LogBrowser.appendPlainText("Welcome to the Namisens Calibration Tool")

    def setup_connections(self):
        # Connect Signals

        self.ui.connectButton.clicked.connect(self._connect)
        self.ui.actionExit.triggered.connect(self.app.quit)


        ######################################### Movement Tab #########################################

        # self.ui.stepSizeSpin.valueChanged.connect(self.ui.zAxisSpin.setValue)
        self.ui.stepSizeSpin.valueChanged.connect(self.update_step_size)

        # Move Button Signals
        self.ui.Move.clicked.connect(self.move_clicked)

    def setup_connections_worker(self):

        self.worker.signals.log_message.connect(self.update_logger)
        ########### Worker Signals ###############################################################
        self.worker.signals.connection_status.connect(self._update_connection_progress)
        # Position Spin Box Signals
        self.ui.zAxisSpin.valueChanged.connect(self.worker.set_z_axis_position)
        self.worker.signals.z_axis_position.connect(self._update_z_axis_position)
        # self.ui.zAxisSpin.valueChanged.connect(self.worker.move_to_position)

        # Speed Spin Box Signals
        self.ui.speedSpin.valueChanged.connect(self.worker.set_speed)
        self.worker.signals.speed_value.connect(self.ui.speedSpin.setValue)
        # Step Size Spin Box Signals
        self.ui.stepSizeSpin.valueChanged.connect(self.worker.set_step_size)

        self.ui.Move.clicked.connect(self.move_clicked)
        # Up Button Signals
        # self.ui.Up.clicked.connect(self.up_clicked)
        self.ui.Up.clicked.connect(self.up_clicked)
        # Pause Button Signals
        self.ui.pausePushButton_2.clicked.connect(self.worker.pause)
        # Finished Movement Signal, called after every movement
        self.worker.signals.m_finished.connect(self.update_movement_progress)
        # Down Button Signals
        # self.ui.Down.clicked.connect(self.down_clicked)
        self.ui.Down.clicked.connect(self.down_clicked)

        ################## Calibration Tab########################################################
        self.ui.sweepPushButton.clicked.connect(self.on_sweep_clicked)

        # Set Calibration Parameters
        self.ui.nSweepSpin.valueChanged.connect(self.worker.set_n_sweep)
        self.ui.measuringTImeSpin.valueChanged.connect(self.worker.set_measurement_time)
        self.ui.calibrationTimeSpin.valueChanged.connect(self.worker.set_calibration_time)
        self.ui.maxSweepSpin.valueChanged.connect(self.worker.set_max_sweep)
        self.ui.minSweepSpin.valueChanged.connect(self.worker.set_min_sweep)
        self.ui.fMeasurementHeightSpinValue.valueChanged.connect(self.worker.set_f_measurement_height)
        self.ui.nMeasurementStopSpinValue.valueChanged.connect(self.worker.set_n_measurement_stops)
        self.ui.referenceAxisPushButton.clicked.connect(self.calibration_axis_clicked)
        # Update current calibration number
        self.worker.signals.current_calibration_number.connect(self.update_calibration_number)

    @Slot(str)
    def update_logger(self, value):
        self.ui.LogBrowser.appendPlainText(value)

    def calibration_axis_clicked(self):
        self.worker.next_action = 'calibrate'
    def up_clicked(self):
        self.worker.next_action = 'moveUp'

    def down_clicked(self):
        self.worker.next_action = 'moveDown'

    def move_clicked(self):
        self.ui.pausePushButton_2.setEnabled(True)
        self.worker.next_action = 'move'

    def on_sweep_clicked(self):
        self.ui.pausePushButton_2.setEnabled(True)
        self.worker.next_action = 'sweep'

    def update_calibration_number(self, value):
        self.ui.sweepNumberLCD.display(value)

    def update_movement_progress(self, value):
        if value == 1:
            self.ui.statusbar.showMessage("Finished Moving", 2000)
            self.ui.pausePushButton_2.setEnabled(False)
        elif value == 0:
            self.ui.statusbar.showMessage("Check motor connection", 2000)
        elif value == 2:
            self.ui.statusbar.showMessage("Moving", 2000)
        elif value == 3:
            self.ui.statusbar.showMessage("Paused", 2000)
            self.ui.pausePushButton_2.setText('Resume')
            self.ui.pausePushButton_2.setEnabled(True)

    def update_step_size(self):
        stepSize = self.ui.stepSizeSpin.value()
        self.ui.zAxisSpin.setSingleStep(stepSize)



    @Slot(float)
    def _update_z_axis_position(self, value):
        return self.ui.zAxisSpin.setValue(value)

    def _update_connection_progress(self, value):
        if value == 1:

            # Update Connection Button Text
            self.ui.statusbar.showMessage("Connected", 5000)
            self.ui.connectButton.setText('Disconnect')

            self.ui.LogBrowser.appendPlainText("\nConnected to Motor Controller")

            # Update UI Connection Status
            self._toggle_buttons(True)
            print("Thread status from update_progress {}".format(self.thread.isRunning()))

            # Get Motor Position and Speed Values from the controller
            self.ui.zAxisSpin.setValue(self.worker.getPosition())
            self.ui.speedSpin.setValue(float(self.worker.getSpeed()))

        elif value == 2:
            try:
                self.ui.statusbar.showMessage("Disconnected", 5000)
                self._toggle_buttons(False)
            finally:
                self.ui.statusbar.showMessage(f"Disconnected")
                self.ui.connectButton.setText('Connect')

        else:
            self.ui.statusbar.showMessage(f"Unable to find any controllers. "
                                          f"Please check the connection and try again.")

    @Slot()
    def _connect(self):
        self.ui.LogBrowser.appendPlainText("\nConnecting to Motor Controller")
        if self.connection_status:
            self.worker.isThreadKilled = True
            print(self.thread.isRunning())
            self._detach_worker()
        else:
            self._attach_worker()

    def _attach_worker(self):
        if self.thread is None:
            self.thread = QThread()
            self.worker = PiWorker(n_sweep_value=self.ui.nSweepSpin.value(),
                                   speed_value=self.ui.speedSpin.value(),
                                   step_size=self.ui.stepSizeSpin.value(),
                                   measurement_time_value=self.ui.measuringTImeSpin.value(),
                                   calibration_time_value=self.ui.calibrationTimeSpin.value(),
                                   max_value=self.ui.maxSweepSpin.value(),
                                   min_value=self.ui.minSweepSpin.value(),
                                   f_measurement_height_value=self.ui.fMeasurementHeightSpinValue.value(),
                                   n_measurements_value=self.ui.nMeasurementStopSpinValue.value())

            self.setup_connections_worker()
            self.worker.moveToThread(self.thread)
            self.thread.started.connect(self.worker.run)
            self.worker.signals.thread_finished.connect(self._detach_worker)
            self.thread.start()
            self.connection_status = True

    @Slot()
    def _detach_worker(self):
        if self.worker is not None:
            self.worker.kill()
            self.worker = None

        if self.thread is not None and self.thread.isRunning():
            try:
                self.thread.quit()
                self.thread.wait()
                self.thread = None
                self.connection_status = False
            finally:
                self.ui.LogBrowser.appendPlainText("Disconnected from Motor Controller")

    def _toggle_buttons(self, state):

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
