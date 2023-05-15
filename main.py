from PySide6.QtWidgets import * 
from PySide6.QtMultimedia import * 
from PySide6.QtMultimediaWidgets import * 
from PySide6.QtCore import * 
from PySide6.QtGui import * 
import numpy as np 
import cv2
import sys


class MainWindow(QWidget):
   def __init__(self):
      super().__init__()

      self.setWindowTitle("Medical Moonshot: Testing")

      self.label = QLabel()
      self.label.setAlignment(Qt.AlignCenter)
      self.label.setAlignment(Qt.AlignBottom)

      self.buttongroup = QButtonGroup()
   
      self.BPCButton = QPushButton("Blood Pressure Cuff")
      self.BPCButton.setCheckable(True)
      self.BPCButton.clicked.connect(self.BPCAction)

      self.POButton = QPushButton("Pulse Oximeter")
      self.POButton.setCheckable(True)
      self.POButton.clicked.connect(self.POAction)

      self.THButton = QPushButton("Thermometer")
      self.THButton.setCheckable(True)
      self.THButton.clicked.connect(self.THAction)

      self.buttongroup.addButton(self.POButton)
      self.buttongroup.addButton(self.BPCButton)
      self.buttongroup.addButton(self.THButton)

      self.layout = QGridLayout(self)
      self.layout.addWidget(self.BPCButton, 0, 0)
      self.layout.addWidget(self.POButton, 0, 1)
      self.layout.addWidget(self.THButton, 0, 2)
      self.layout.addWidget(self.label, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)

      self.camera = CameraThread()
      self.camera.image.connect(self.update_image)
      self.camera.start()

   def update_image(self, frame):
      frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
      image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
      self.label.setPixmap(QPixmap.fromImage(image))
   
   def BPCAction(self):
      print("Performing BPCuff")
   
   def POAction(self):
      print("Performing PO Action")
   
   def THAction(self):
      print("Performing Thermometer")

class CameraThread(QThread):
   image = Signal(np.ndarray)

   def __init__(self):
      super().__init__()

   def start_capture(self):
      self.capture = cv2.VideoCapture(0)

   def run(self):
      self.start_capture()
      while True:
         ret, frame = self.capture.read()
         if ret:
            self.image.emit(frame)

if __name__ == "__main__":
    
    app = QApplication()
    main = MainWindow()

    main.show()

    sys.exit(app.exec_())

