from PySide2 import QtCore, QtWidgets, QtGui

# Lab Specific Labels
A_FILETXT = ".../INX/analyzelist1.txt"
B_FILETXT = ".../PB/analyzelist3.txt"
SAVEPATHTXT = "Q:/.../Tools/LangMatrix/Results/[dd]-[mm]-[yyyy]"


class UiMatrix:
    def setupUi(self, MainWindow):
        MainWindow.setWindowTitle('Co-Occurance Matrix Generator')
        self.window = QtWidgets.QWidget(MainWindow)
        self.window.setFont(QtGui.QFont('Arial', 10))
        self.window.setMinimumWidth(500)

        self.startbtn = QtWidgets.QPushButton("Start Analysis")
        self.startbtn.setFixedHeight(40)

        windowlyt = QtWidgets.QVBoxLayout(self.window)
        windowlyt.setContentsMargins(10, 5, 10, 5)
        windowlyt.addWidget(self.fileframesetup())
        windowlyt.addWidget(self.saveframesetup())
        windowlyt.addWidget(self.startbtn)

        MainWindow.setCentralWidget(self.window)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def fileframesetup(self):
        fileframe = QtWidgets.QFrame()

        uploadfilesfrm = self.foldergrouboxsetup()
        # defaultoptionsfrm = self.pbinx_framesetup()

        # Layout configuration
        fileframelyt = QtWidgets.QVBoxLayout(fileframe)
        fileframelyt.setSpacing(5)
        fileframelyt.setAlignment(QtCore.Qt.AlignLeft)
        # add widgets
        fileframelyt.addWidget(uploadfilesfrm)
        # fileframelyt.addWidget(defaultoptionsfrm)

        return fileframe

    def saveframesetup(self):
        savebox = QtWidgets.QGroupBox("Save results in...")

        self.savelbl = self.path_lblsetup(SAVEPATHTXT)
        self.savebtn = self.file_btnsetup('Pick folder')

        savelyt = QtWidgets.QHBoxLayout(savebox)
        savelyt.setAlignment(QtCore.Qt.AlignLeft)
        savelyt.setSpacing(10)
        savelyt.addWidget(self.savelbl)
        savelyt.addWidget(self.savebtn)

        return savebox

    def foldergrouboxsetup(self):
        box = QtWidgets.QGroupBox("Transcripts to Analyze")

        instructlbl = QtWidgets.QLabel("Upload list of files (*.txt)")
        columnlbl = QtWidgets.QLabel("Analysis\ncolumn")

        # Each file has a lbl, btn, and lineedit field
        self.A_filelbl = self.path_lblsetup(A_FILETXT)
        self.A_filebtn = self.file_btnsetup("Upload")
        self.A_collbl = self.file_colEntrysetup("C")
        # self.A_clearbtn = self.file_btnsetup("Clear")

        self.B_filelbl = self.path_lblsetup(B_FILETXT)
        self.B_filebtn = self.file_btnsetup("Upload")
        self.B_collbl = self.file_colEntrysetup("A")
        # self.B_clearbtn = self.file_btnsetup("Clear")

        # Layout configuration
        boxlyt = QtWidgets.QGridLayout(box)
        boxlyt.setSpacing(5)
        # boxlyt.setAlignment(QtCore.Qt.AlignCenter)

        boxlyt.addWidget(instructlbl, 0, 0, 1, 2)
        boxlyt.addWidget(columnlbl, 0, 2, 1, 1)
        # Add file i/o widgets
        boxlyt.addWidget(self.A_filelbl, 1, 0, 1, 1)
        boxlyt.addWidget(self.A_filebtn, 1, 1, 1, 1)
        boxlyt.addWidget(self.A_collbl, 1, 2, 1, 1)
        # boxlyt.addWidget(self.A_clearbtn, 1, 3, 1, 1)

        boxlyt.addWidget(self.B_filelbl, 2, 0, 1, 1)
        boxlyt.addWidget(self.B_filebtn, 2, 1, 1, 1)
        boxlyt.addWidget(self.B_collbl, 2, 2, 1, 1)
        # boxlyt.addWidget(self.B_clearbtn, 1, 3, 1, 1)

        return box

    # configuration for each filepath label
    def path_lblsetup(self, placeholdertxt):
        lbl = QtWidgets.QLabel(" ")
        if placeholdertxt:
            lbl.setText(placeholdertxt)

        lbl.setFixedHeight(25)
        lbl.setMinimumWidth(200)
        lbl.setFont(QtGui.QFont('Courier New', 9))
        lbl.setFrameShape(QtWidgets.QFrame.Box)
        lbl.setFrameShadow(QtWidgets.QFrame.Sunken)
        lbl.setStyleSheet("background-color: rgba(255, 255, 255, 0.5)")

        return lbl

    # configuration for each upload-file button
    def file_btnsetup(self, text, shortcut=None):
        btn = QtWidgets.QPushButton(text)
        btn.setFixedSize(QtCore.QSize(100, 25))

        if shortcut:
            btn.setShortcut(QtGui.QKeySequence(shortcut))
        return btn

    # Sets up column-entry field, as lineedit widget
    def file_colEntrysetup(self, placeholdertxt):
        columnentry = QtWidgets.QLineEdit()
        columnentry.setFixedWidth(30)

        if placeholdertxt:
            columnentry.setPlaceholderText(placeholdertxt)

        return columnentry

    # Option for pre-set defaults
    def pbinx_framesetup(self):
        box = QtWidgets.QGroupBox("Default Options")

        pblbl = QtWidgets.QLabel("Choose all Picture Books?")
        inxlbl = QtWidgets.QLabel("Choose all INX subjects?")

        self.pbchbx = QtWidgets.QCheckBox("Yes")
        self.inxchbx = QtWidgets.QCheckBox("Yes")

        lyt = QtWidgets.QFormLayout(box)
        right = QtWidgets.QFormLayout.FieldRole
        left = QtWidgets.QFormLayout.LabelRole

        lyt.setWidget(0, left, pblbl)
        lyt.setWidget(0, right, self.pbchbx)
        lyt.setWidget(1, left, inxlbl)
        lyt.setWidget(1, right, self.inxchbx)

        return box

    def infomsgbox(self, infomsg, detailedmsg="", iserror=False):
        msg = QtWidgets.QMessageBox()
        msg.setFixedSize(QtCore.QSize(450, 350))
        msg.setWindowTitle("Matrix Generation")
        if iserror:
            msg.setIcon(QtWidgets.QMessageBox.Warning)
        else:
            msg.setIcon(QtWidgets.QMessageBox.Information)

        msg.setText(infomsg)
        msg.setInformativeText(detailedmsg)

        msg.exec_()

