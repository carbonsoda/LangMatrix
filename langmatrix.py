# import ctypes  # for Windows ONLY
import os
import sys
import lib.ui as ui
import lib.processing as wordsort
from functools import partial
from PySide2 import QtWidgets, QtGui
from datetime import datetime


# MAIN WINDOW
class LangMatrix(QtWidgets.QMainWindow, wordsort.Processing, ui.UiMatrix):
    def __init__(self, parent=None):
        super(LangMatrix, self).__init__(parent)
        # refuses to initialize otherwise, to come back to later
        wordsort.Processing.__init__(self)
        self.setupUi(self)

        today = str(datetime.today().date())
        self.savelbl.setText('Q:/.../Tools/LangMatrix/Results/' + today)

        self.connections()

    # Configure buttons and labels to their respective functions
    def connections(self):
        self.startbtn.clicked.connect(partial(self.startanalysis))

        # File buttons
        self.A_filebtn.clicked.connect(partial(self.updatefilepath, "A", self.A_filelbl))
        self.B_filebtn.clicked.connect(partial(self.updatefilepath, "B", self.B_filelbl))
        self.savebtn.clicked.connect(partial(self.uploadfile, self.savelbl, False))

        # column labels
        self.A_collbl.textChanged.connect(lambda: self.A_collbl.text())
        self.B_collbl.textChanged.connect(lambda: self.B_collbl.text())

    # Initiate analysis/matrix generation
    def startanalysis(self):
        if self.A_analyzepath or self.B_analyzepath:
            self.A_col = self.A_collbl.text()
            self.B_col = self.B_collbl.text()

            if self.A_col.isdigit() or self.B_col.isdigit():
                self.infomsgbox('Invalid column(s)', 'They must be letters, not numbers', iserror=True)
                return

            self.infomsgbox("Collecting files for analysis...")

            double, single = self.config()
            if double or single:
                self.infomsgbox('Searching files and starting analysis...',
                                'This may take some time')
                self._runanalysis(double, single)
            else:
                self.infomsgbox('List(s) of files are empty',
                                'Either the txt file is empty or the listed files could not be found',
                                iserror=True)

    # helper method
    def _runanalysis(self, double, single):
        foundfile = self.analysis(double, single)

        if foundfile:
            self.infomsgbox('Word Counting complete!',
                            'The co-occurance matrix can be found in\n' 
                            + str(self.outputdir).replace('\\', '/'))
        else:
            # Haven't run into anything, but placeholder for now
            self.infomsgbox('Issue!')


    # For savebtn, upload == False
    def uploadfile(self, whichlbl, upload=True):
        if upload:
            file = QtWidgets.QFileDialog.getOpenFileName(filter="Transcripts (*.txt *.csv)")[0]
            file = os.path.join(file).replace('\\', '/')
            if len(file) > 1:
                whichlbl.setText('.../' + str(os.path.split(file)[1]))
                # for some reason passing in the self.A_analyzepath or such doesn't get modified so...
                return file
            else:
                whichlbl.setText(' ')
                return ''
        else:
            savedir = QtWidgets.QFileDialog.getExistingDirectory()[0].replace('\\', '/')
            savedir = os.path.join(savedir).replace('\\', '/')
            if len(savedir) > 1:
                # choosing own save name
                self.outputdir = savedir
                try:
                    # leaves just the last two parts, ie "lib/ui.py"
                    lbltxt = '/'.join(savedir.split('/')[-2:])
                    whichlbl.setText('...' + lbltxt)
                except IndexError:
                    pass
            else:
                whichlbl.setText(' ')
                return ''

    # for some reason passing in the class variable doesn't get modified so, workaround
    def updatefilepath(self, whichpath, whichlbl):
        if whichpath == "A":
            self.A_analyzepath = self.uploadfile(self.A_filelbl)

        elif whichpath == "B":
            self.B_analyzepath = self.uploadfile(self.B_filelbl)


if __name__ == "__main__":
    # Create the Qt Application
    app = QtWidgets.QApplication(sys.argv)
    # ensures same look for all
    s = QtWidgets.QStyleFactory.create('Fusion')
    app.setStyle(s)

    # # for Windows
    # myappid = u"mycompany.myproduct.subproduct.version"  # arbitrary string
    # ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)  # from ctypes
    # app.setWindowIcon(QtGui.QIcon('resources/main.ico'))

    # Create and show main window
    window = LangMatrix()
    window.setWindowTitle('Co-Occurance Matrix Generator')
    window.setWindowIcon(QtGui.QIcon('resources/main.ico'))
    window.show()

    sys.exit(app.exec_())

