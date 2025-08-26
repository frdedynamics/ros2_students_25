#!/usr/bin/env python3
# 
# # -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.rosNodeButton = QtWidgets.QPushButton(Form)
        self.rosNodeButton.setGeometry(QtCore.QRect(120, 50, 151, 51))
        self.rosNodeButton.setObjectName("rosNodeButton")
        self.setActionButton = QtWidgets.QPushButton(Form)
        self.setActionButton.setGeometry(QtCore.QRect(210, 150, 141, 71))
        self.setActionButton.setObjectName("setActionButton")
        self.actionTextEdit = QtWidgets.QTextEdit(Form)
        self.actionTextEdit.setGeometry(QtCore.QRect(40, 150, 104, 70))
        self.actionTextEdit.setObjectName("actionTextEdit")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.rosNodeButton.setText(_translate("Form", "Run ROS Node"))
        self.setActionButton.setText(_translate("Form", "Set Action"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
