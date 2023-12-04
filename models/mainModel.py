from PySide6.QtCore import QObject, Signal, Slot, QAbstractItemModel
from typing import Union
from pipython import GCSDevice


class calibrationUIModel(QAbstractItemModel):
    def __init__(self):
        super().__init__()
        self._connectButtonState: bool = False
        # self._piDevice: Union[GCSDevice, None] = None
        self._zAxisPosition: Union[float, None] = None
        self._speedValue: Union[float, None] = None
        self._stepSizeValue: Union[float, None] = None
        self._minValue: Union[float, None] = None
        self._maxValue: Union[float, None] = None
        self._nSweepValue: Union[int, None] = None
        self._haltTimeValue: Union[float, None] = None

    @property
    def zAxisPosition(self) -> float:
        return self._zAxisPosition

    @zAxisPosition.setter
    def zAxisPosition(self, value):
        self.zAxisPosition = value
        self.zAxisPosition.emit()

    @property
    def speedValue(self):
        return self.speedValue

    @speedValue.setter
    def speedValue(self, value):
        self._speedValue = value
        self.speedValue.emit()

    @property
    def stepSizeValue(self):
        return self.stepSizeValue

    @stepSizeValue.setter
    def stepSizeValue(self, value):
        self._stepSizeValue = value
        self.stepSizeValue.emit()

    @property
    def minValue(self):
        return self.minValue

    @minValue.setter
    def minValue(self, value):
        self._minValue = value
        self.minValue.emit()

    @property
    def maxValue(self):
        return self.maxValue

    @maxValue.setter
    def maxValue(self, value):
        self._maxValue = value
        self.maxValue.emit()

    @property
    def nSweepValue(self):
        return self.nSweepValue

    @nSweepValue.setter
    def nSweepValue(self, value):
        self._nSweepValue = value
        self.nSweepValue.emit()

    @property
    def haltTimeValue(self):
        return self.haltTimeValue

    @haltTimeValue.setter
    def haltTimeValue(self, value):
        self._haltTimeValue = value
        self.haltTimeValue.emit()

    @property
    def connectButtonState(self):
        return self._connectButtonState

    @connectButtonState.setter
    def connectButtonState(self, value):
        self._connectButtonState = value

    @property
    def piDevice(self):
        return self._piDevice

    @piDevice.setter
    def piDevice(self, value):
        self._piDevice = value
        # self.piDevice.emit()

    zAxisChanged = Signal()
    speedValueChanged = Signal()
    stepSizeValueChanged = Signal()
    minValueChanged = Signal()
    maxValueChanged = Signal()
    nSweepValueChanged = Signal()
    haltTimeValueChanged = Signal()
    connectButtonStateChanged = Signal()
    piDeviceChanged = Signal()



