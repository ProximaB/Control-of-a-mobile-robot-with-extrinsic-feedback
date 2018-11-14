import cv2
def start_webcam(self):
        if not self.cameraRuns:
            self.capture = cv2.VideoCapture(cv2.CAP_DSHOW)
            self.cameraRuns = not self.cameraRuns
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.update_frame)
            self.timer.start(2)

from PyQt5.QtCore import QTime, QTimer
from PyQt5.QtWidgets import QApplication, QLCDNumber


class DigitalClock(QLCDNumber):
    def __init__(self, parent=None):
        super(DigitalClock, self).__init__(parent)

        self.setSegmentStyle(QLCDNumber.Filled)

        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)

        self.showTime()

        self.setWindowTitle("Digital Clock")
        self.resize(150, 60)

    def showTime(self):
        time = QTime.currentTime()
        text = time.toString('hh:mm')
        if (time.second() % 2) == 0:
            text = text[:2] + ' ' + text[3:]

        self.display(text)


import sys

app = QApplication(sys.argv)
clock = DigitalClock()
clock.show()
sys.exit(app.exec_())