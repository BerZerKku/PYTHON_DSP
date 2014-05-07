# -*- coding: utf-8 -*-

##
#  @file      dsp_gui.py
#  @brief     Оболочка для создания файлов прошивки DSP аппаратов АВАНТ.
#  @details   Создание файла прошивки для для заданного типа аппарата, версии
#             прошивки, частоты и номера.
#
#  @version   1.03
#  @date      май 2014
#  @author    Щеблыкин М.В.

# дополнительные возможности
#  @pre       First initialize the system.
#  @bug       Не найдено
#  @warning   Improper use can crash your application
#  @copyright GNU Public License.

## Версия программы.
VERSION = u"1v03"

import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import Qt

import dsp
import my_func
import resources_rc

#------------------------------------------------------------------------------
## GUI для cоздания прошивки DSP АВАНТ.
#  Помогает создать файл прошивки для аппарата.
#  Имеется возможность выбрать тип аппарата, версию прошивки, частоту и номер.
class DSPGui(QtGui.QMainWindow):
    def __init__(self, parent=None):
        ''' (self, xz) -> None
            
            Конструктор.
            @param parent См. pyQT4.
        '''

        # инициализация предка
        QtGui.QMainWindow.__init__(self, parent)

        # внешний вид
        # Windows, WindowsXP, Motif, CDE, Plastique, Cleanlooks
        QtGui.QApplication.setStyle('Cleanlooks')

        # установка минимальной ширины окна
        self.setMinimumWidth(300)

        # запрет изменения размеров формы
        flag = QtCore.Qt.Window
        flag |= QtCore.Qt.MSWindowsFixedSizeDialogHint
        self.setWindowFlags(flag)

        ## фиктивный виджет
        self.mainWidget = QtGui.QWidget(self)
        self.setCentralWidget(self.mainWidget)

        # установка иконки и титула
        self.setWindowIcon(QtGui.QIcon(':icons/Apps.png'))
#        # вывод версии файла dsp.py
#        title = u'Прошивка DSP ' + str(dsp.DSPhex())
        print dsp.DSPhex()
        # вывод версии GUI
        title = u"Прошивка DSP %s" % VERSION
        self.setWindowTitle(title)

        ## Кнопка сохранить
        self.pSave = QtGui.QPushButton(u'Сохранить')
        self.pSave.clicked.connect(self.fileSave)
        ## Кнопка сохранить как
        self.pSaveAs = QtGui.QPushButton(u'Сохранить как...')
        self.pSaveAs.clicked.connect(self.fileSaveAs)

        # создание напдписей
        label1 = QtGui.QLabel(u'Частота, кГц')
        label2 = QtGui.QLabel(u'Номер аппарата')
        label3 = QtGui.QLabel(u'Аппарат')
        label4 = QtGui.QLabel(u'Версия прошивки')

        ## поле ввода частоты
        self.eFreq = QtGui.QSpinBox()
        self.eFreq.setRange(16, 1000)

        ## поле ввода номера аппарата
        self.eNum = QtGui.QSpinBox()
        self.eNum.setRange(1, 2)

        # доступные версии прошивок будут добавлены при выборе типа аппарата
        ## поле выбора версии прошивки
        self.eVersion = QtGui.QComboBox()


        # при изменении значения в данном поле, будет вызвана функция
        # перезаполнения элементов поля версии прошивок
        ## поле выбора типа аппарата
        self.eDevice = QtGui.QComboBox()
        self.eDevice.currentIndexChanged.connect(self.refreshVersion)
        self.eDevice.addItems(dsp.DSPhex().getDevices())

        # заполнение формы
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

        # установка онка по центру экрана
        self.center()

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
        
            Сохранение файла прошивки. Если имя \a name не задано, оно будет
            сгенерировано автоматически.
            
            @param checked См. pyQT4.
            @param name Имя прошивки.
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
                                            unicode(inst))

    #
    def fileSaveAs(self, checked=False):
        ''' (dspgui, bool, str) -> None
        
            Выбор пути и имени файла прошивки, если на входе name не задано.
            
            @param checked См. pyQT4.
        '''

        name = QtGui.QFileDialog.getSaveFileName(self, u"Сохранить как...",
                                        filter="HEX Files (*.hex)")
        # выход, в случае отсутствия имени
        if name:
            self.fileSave(name=name)

    #
    def refreshVersion(self):
        ''' (self) -> None
        
            Заполнение элемента выбора версии прошивки для выбранного
            типа аппарата.
        '''
        self.eVersion.clear()
        device = self.eDevice.currentText()
        self.eVersion.addItems(dsp.DSPhex().getVersions(device))
        # если имеется больше одной версии прошивок, будет разрешен их выбор
        self.eVersion.setEnabled(self.eVersion.count() > 1)


#
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    dspGui = DSPGui()
    dspGui.show()

    app.exec_()
