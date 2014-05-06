# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import Qt

import dsp
import my_func
import resources_rc

#
class DSPGui(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        
        # внешний вид
        # Windows, WindowsXP, Motif, CDE, Plastique, Cleanlooks
        QtGui.QApplication.setStyle('Cleanlooks')
        
        self.setMinimumWidth(300)
        # запрет изменения размеров формы
        flag = QtCore.Qt.Window
        flag |= QtCore.Qt.MSWindowsFixedSizeDialogHint
        self.setWindowFlags(flag)
        
        # установим фиктивный виджет
        self.mainWidget = QtGui.QWidget(self)
        self.setCentralWidget(self.mainWidget)
        
        # установка иконки и титула
        self.setWindowIcon(QtGui.QIcon(':icons/Apps.png'))
        title = u'Прошивка DSP ' + str(dsp.DSPhex())
        self.setWindowTitle(title)
        
        # 
        self.pSave = QtGui.QPushButton(u'Сохранить')
        self.pSave.clicked.connect(self.fileSave)
        self.pSaveAs = QtGui.QPushButton(u'Сохранить как...')
        self.pSaveAs.clicked.connect(self.fileSaveAs)
        
        # 
        label1 = QtGui.QLabel(u'Частота, кГц')
        label2 = QtGui.QLabel(u'Номер аппарата')
        label3 = QtGui.QLabel(u'Аппарат')
        label4 = QtGui.QLabel(u'Версия прошивки')
        
        # 
        self.eFreq = QtGui.QSpinBox()
        self.eFreq.setRange(16, 1000)
        self.eNum = QtGui.QSpinBox()
        self.eNum.setRange(1, 2)
        
        #
        self.eDevice = QtGui.QComboBox()
        self.eDevice.addItems(dsp.DSPhex().getDevices())
        self.eDevice.setDisabled(False)
        
        #
        self.eVersion = QtGui.QComboBox()
        self.eVersion.addItems(dsp.DSPhex().getVersions())
        self.eVersion.setDisabled(False)
        
        # 
        grid = QtGui.QGridLayout(self.mainWidget) 
        grid.addWidget(label3, 0, 0)
        grid.addWidget(self.eDevice, 0, 1)    
        grid.addWidget(label4, 1, 0)   
        grid.addWidget(self.eVersion, 1, 1)
        grid.addWidget(label1, 2, 0)
        grid.addWidget(self.eFreq, 2, 1)
        grid.addWidget(label2, 3, 0)
        grid.addWidget(self.eNum, 3, 1)
        grid.addWidget(self.pSave, 4, 0)
        grid.addWidget(self.pSaveAs, 4, 1)
        
        a = self.sizeHint()
        print a.height(), a.width()
        b = self.size()
        print b.height(), b.width()
        
        self.center()
        self.show()
        
    #
    def center(self):
        ''' (self) -> None
        
            Установка окна посередине экрана.
        '''
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)
    
    #    
    def fileSave(self, checked=False, name=None):
        ''' (dspgui, bool, str) -> None
        
            Сохранение файла прошивки. Если имя name не задано, оно будет
            сгенерировано.
        '''
        tdsp = dsp.DSPhex()
        tdsp.setFrequence(self.eFreq.value())
        tdsp.setNumber(self.eNum.value())
        tdsp.setDevice(unicode(self.eDevice.currentText()))
        tdsp.setVersion(unicode(self.eVersion.currentText()))
        try:
            tdsp.saveNewHEX(name=name)
        except Exception as inst:
            Qt.QMessageBox.critical(self, u"Ошибка сохранения файла прошивки",
                                     str(inst))
    
    #    
    def fileSaveAs(self, checked=False, name=None):
        ''' (dspgui, bool, str) -> None
        
            Выбор пути и имени файла прошивки, если на входе name не задано.
        '''
        if name is None:
            name = QtGui.QFileDialog.getSaveFileName(self, u"Сохранить как...",
                                        filter="HEX Files (*.hex)")
            # выход, в случае отсутствия имени
            if not name:
                return
        
        self.fileSave(name=name)
        
#        
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    
    dspGui = DSPGui()
    dspGui.show()
    
    app.exec_()
