from PyQt5 import QtCore, QtGui

class Highlighter(QtGui.QSyntaxHighlighter):
    def __init__(self, parent):
        super(Highlighter, self).__init__(parent)
        self.startFormat = QtGui.QTextCharFormat()
        self.startFormat.setForeground(QtCore.Qt.blue)
        self.stopFormat = QtGui.QTextCharFormat()
        self.stopFormat.setForeground(QtCore.Qt.red)
        self.uploadFormat = QtGui.QTextCharFormat()
        self.uploadFormat.setForeground(QtCore.Qt.darkMagenta)

    def highlightBlock(self, text):
        if text.find('start')>-1:
            self.setFormat(0, len(text), self.startFormat)
        elif text.find('stop')>-1 or text.find('pause')>-1 :
            self.setFormat(0, len(text), self.stopFormat)
        elif text.find('Model')>-1 or text.find('select')>-1:
            self.setFormat(0, len(text), self.uploadFormat)
