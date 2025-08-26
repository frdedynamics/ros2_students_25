from main import Ui_Form as Main_Widget

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import sys, os
import subprocess, signal
import time

class GUI_Window(QWidget, Main_Widget):
    def __init__(self, parent=None):
        super(GUI_Window, self).__init__(parent)
        self.setupUi(self)
        # self.resize(854, 480)
        self.setWindowTitle("My GUI app")
        self.rosNodeButton.clicked.connect(self.start_ros_node)
        self.my_publisher_proc = None

        ## Set Action button
        self.msg_data = None
        self.setActionButton.clicked.connect(self.set_action)
        self.my_action_proc = None

        self.show()

    def start_ros_node(self):
        if self.my_publisher_proc == None: # because you don't want to start several processes in each click
            self.my_publisher_proc = subprocess.Popen(["ros2", "run", "my_gui_pkg", "service"], text=True, preexec_fn=os.setsid)
        else:
            print("The node is already exist")
    
    def set_action(self):
        self.msg_data = self.actionTextEdit.toPlainText() # we read the data
        print(self.msg_data)
        subprocess.Popen(["ros2", "run", "my_gui_pkg", "client", str(self.msg_data), "1"], text=True, preexec_fn=os.setsid)

    def kill_processes(self):
        # This is to kill rosnodes as you close the windiw
        try:
            os.killpg(os.getpgid(self.my_publisher_proc.pid), signal.SIGINT)
            print("Sent SIGINT to ROS node")
        except Exception as e:
            print(e)

    def closeEvent(self, event):
        print("Window closing...")
        self.kill_processes()
        time.sleep(0.5)
        event.accept() # let the window close

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = GUI_Window()
    sys.exit(app.exec_())
