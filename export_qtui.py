# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'export_translation.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from trans_export import *

class Ui_ExportWindow(object):
    def __init__(self):
        with DBWrapper() as dbconn:
            self.accounts = dbconn.select_account()
            self.account_map = {acc.name:acc.id for acc in \
                    self.accounts}
    
    def setupUi(self, ExportWindow):
        ExportWindow.setObjectName("ExportWindow")
        ExportWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(ExportWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.accountCombo = QtWidgets.QComboBox(self.centralwidget)
        self.accountCombo.addItems([acc.name for acc in self.accounts])
        self.accountCombo.setGeometry(QtCore.QRect(120, 30, 141, 27))
        self.accountCombo.setObjectName("accountCombo")
        self.accountCombo.currentIndexChanged.connect(self.account_changed)
        self.projectCombo = QtWidgets.QComboBox(self.centralwidget)
        self.projectCombo.setGeometry(QtCore.QRect(400, 30, 161, 30))
        self.projectCombo.setObjectName("projectCombo")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 30, 68, 17))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(320, 30, 68, 17))
        self.label_2.setObjectName("label_2")
        self.exportButton = QtWidgets.QPushButton(self.centralwidget)
        self.exportButton.setGeometry(QtCore.QRect(50, 490, 180, 27))
        self.exportButton.setObjectName("exportButton")
        self.exportButton.clicked.connect(self.export)
        self.exportName = QtWidgets.QLineEdit(self.centralwidget)
        self.exportName.setGeometry(QtCore.QRect(270, 490, 480, 27))
        self.exportName.setObjectName("exportName")
        self.statusLabel = QtWidgets.QLabel(self.centralwidget)
        self.statusLabel.setGeometry(QtCore.QRect(130, 530, 300, 27))
        self.statusLabel.setObjectName("statusLabel")
        self.languageInput = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.languageInput.setGeometry(QtCore.QRect(20, 140, 281, 301))
        self.languageInput.setObjectName("languageInput")
        self.textidInput = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.textidInput.setGeometry(QtCore.QRect(340, 140, 441, 301))
        self.textidInput.setObjectName("textidInput")
        ExportWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(ExportWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 25))
        self.menubar.setObjectName("menubar")
        ExportWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(ExportWindow)
        self.statusbar.setObjectName("statusbar")
        ExportWindow.setStatusBar(self.statusbar)

        self.retranslateUi(ExportWindow)
        QtCore.QMetaObject.connectSlotsByName(ExportWindow)

    def retranslateUi(self, ExportWindow):
        _translate = QtCore.QCoreApplication.translate
        ExportWindow.setWindowTitle(_translate("ExportWindow", "Export translation"))
        self.label.setText(_translate("ExportWindow", "Account:"))
        self.label_2.setText(_translate("ExportWindow", "Project:"))
        self.statusLabel.setText(_translate("ExportWindow", ""))
        self.exportButton.setText(_translate("ExportWindow", "Query and Export to "))
        self.exportName.setText(_translate("ExportWindow",
            "data/translations_export.xlsx"))

    def account_changed(self, i):
        account = self.accountCombo.currentText()
        with DBWrapper() as dbconn:
            projects = dbconn.select_project(self.account_map[account])
            self.projectCombo.clear()
            self.projectCombo.addItems(projects)

    def splitinput(self, text):
        patt = ',|\r|\n'
        values = re.split(patt, text)
        return [val.strip() for val in values if val] #remove the empty val

    def export(self):
        account = self.accountCombo.currentText()
        project = self.projectCombo.currentText()
        langs = self.splitinput(self.languageInput.toPlainText())
        textids = self.splitinput(self.textidInput.toPlainText())
        where_clause = WhereClause()
        accs = []
        accs.append(account)
        projs = []
        projs.append(project)
        where_clause.add('Account', accs)
        where_clause.add('Project', projs)
        where_clause.add('Language', langs)
        where_clause.add('Text', textids)

        print(where_clause.clauses)

        with DBWrapper() as db:
            _translate = QtCore.QCoreApplication.translate
            self.statusLabel.setText(_translate("ExportWindow",
                "Querying translation from DB..."))
            translations = db.select_translation(where_clause.clauses)
            export = TransExport()
            self.statusLabel.setText(_translate("ExportWindow",
                "Saving translation..."))
            export.save_translation(translations,
                    self.exportName.displayText())
            self.statusLabel.setText(_translate("ExportWindow",
                "Completed!"))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ExportWindow = QtWidgets.QMainWindow()
    ui = Ui_ExportWindow()
    ui.setupUi(ExportWindow)
    ExportWindow.show()
    sys.exit(app.exec_())

