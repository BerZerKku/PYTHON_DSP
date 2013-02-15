# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import Qt

import dsp
import my_func


class DSPGui(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        
        # внешний вид
        # Windows, WindowsXP, Motif, CDE, Plastique, Cleanlooks
        QtGui.QApplication.setStyle('Cleanlooks')
        
        self.center()
        
        # запрет изменения размеров формы
        flag = QtCore.Qt.Window
        flag |= QtCore.Qt.MSWindowsFixedSizeDialogHint
        self.setWindowFlags(flag)
        
        # установим фиктивный виджет
        self.mainWidget = QtGui.QWidget(self)
        self.setCentralWidget(self.mainWidget)
        
        # установка иконки и титула
        self.setWindowIcon(QtGui.QIcon('apps.png'))
        self.setWindowTitle(u'Прошивка DSP')
        
        # 
        self.pSave = QtGui.QPushButton(u'Сохранить')
        self.pSave.clicked.connect(self.fileSave)
        self.pSaveAs = QtGui.QPushButton(u'Сохранить как...')
        self.pSaveAs.clicked.connect(self.fileSaveAs)
        
        # 
        label1 = QtGui.QLabel(u'Частота, кГц')
        label2 = QtGui.QLabel(u'Номер аппарата')
        label3 = QtGui.QLabel(u'Аппарат')
        
        # 
        self.eFreq = QtGui.QSpinBox()
        self.eFreq.setRange(10, 1000)
        self.eNum = QtGui.QSpinBox()
        self.eNum.setRange(1, 2)
        
        #
        self.eDevice = QtGui.QComboBox()
        tHex = dsp.DSPhex()
        self.eDevice.addItems(['P400'])
        self.eDevice.setDisabled(True)
        
        # 
        grid = QtGui.QGridLayout(self.mainWidget) 
        grid.addWidget(label3, 0, 0)
        grid.addWidget(self.eDevice, 0, 1)       
        grid.addWidget(label1, 1, 0)
        grid.addWidget(self.eFreq, 1, 1)
        grid.addWidget(label2, 2, 0)
        grid.addWidget(self.eNum, 2, 1)
        grid.addWidget(self.pSave, 3, 0)
        grid.addWidget(self.pSaveAs, 3, 1)
    
    def center(self):
        ''' (self) -> None
        
            Установка окна посередине экрана.
        '''
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)
        
    def fileSave(self, checked=False, name=None):
        tdsp = dsp.DSPhex()
        tdsp.loadSourceHEX()
        tdsp.setFrequence(self.eFreq.value())
        tdsp.setNumber(self.eNum.value())
        tdsp.setDevice(str(self.eDevice.currentText()))
        tdsp.saveNewHEX(name=name)
        
    def fileSaveAs(self, checked=False, name=None):
        print name, type(name)
        if name is None:
            name = QtGui.QFileDialog.getSaveFileName(self, u"Сохранить как...",
                                        filter="HEX Files (*.hex)")
            # выход, в случае отсутствия имени
            if not name:
                return
        
        self.fileSave(name=name)
        
        
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    
    dspGui = DSPGui()
    dspGui.show()
    
    app.exec_()