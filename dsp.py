# -*- coding: utf-8 -*-

##
#  @file      dsp.py
#  @brief     Создание файлов прошивки DSP для АВАНТ Р400, Р400м, РЗСК, К400.
#  @details   Создание файла прошивки для для заданного типа аппарата, версии
#             прошивки, частоты и номера.
#             На данный момент потдерживаются:
#                 - Р400
#                     -# 1v36
#                     -# 1v34
#                     -# 1v30
#                 - РЗСК
#                     -# 1v30
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
import os
import my_func

#------------------------------------------------------------------------------
def newP400_1v36(source, freq, num):
    ''' (str) -> sr

        Корректирует файл прошивки версии 1v36 для Р400 для указанной частоты
        и номера аппарата.
    '''
    return source

#-----------------------------------------------------------------------------
def newP400_1v34(source, freq, num):
    ''' (str, int, int) -> str

        Корректирует файл прошивки версии 1v30 для Р400 для указанной частоты
        и номера аппарата.
    '''
    return source

def newP400_1v30(source, freq, num):
    ''' (str, int, int) -> str

        Корректирует файл прошивки версии 1v30 для Р400 для указанной частоты
        и номера аппарата.
    '''

    # массив изменяемых строк в заисисмости от номера аппарата
    # значение словаря  зависит от номера аппарата [1, 2]
#        self.P400 = {'1320': ['1310091210095048', '1210091310095048'],
#                     '1378': ['0009131009121009', '0009121009131009'],
#                     '1C88': ['8048980A01109080', '9048980A01109080'],
#                     '1CA8': ['7598904898AF8006', '7598804898AF8006'],
#                     '57B0': ['00010019700000FB', '00020019700000FB']}
    # строка '57D0' вычисляется относительно частоты и номера аппарата
    # xx (crc1) (crc2) xx xx xx (crc1, crc2 - двухбайтные)
    # строка '1BD0' зависит от частоты
    # (fr) xx xx xx xx xx xx

    #
    def calcCrc1(freq, num):
        val = freq * 32
        if num == 1:
            val += 64
        elif num == 2:
            val -= 64
        else:
            print u"calcCrc1"
            print u"Значения кроме 1 и 2 не принимаются:", num, type(num)
            raise ValueError
        val = my_func.intToStrHex(val)
        while len(val) < 4:
            val = '0' + val
        val = val[2:] + val[:2]
        return val

    #
    def calcCrc2(freq, num):
        val = freq * 8
        if num == 1:
            val -= 16
        elif num == 2:
            val += 16
        else:
            print u"calcCrc2"
            print u"Значения кроме 1 и 2 не принимаются:", num, type(num)
            raise ValueError
        val = my_func.intToStrHex(val)
        while len(val) < 4:
            val = '0' + val
        val = val[2:] + val[:2]
        return val

    #
    def calcFreq(val):
        val = "%02x0" % val
        if len(val) < 4:
            val = '0' + val
        val = val[2:] + val[:2]
        return val.upper()

    if not isinstance(source, str):
        raise TypeError(u"Ошибочный тип данных 'str'", unicode(type(source)))

    if not isinstance(freq, int):
        raise TypeError(u"Ошибочный тип данных 'freq'", unicode(type(freq)))

    if not isinstance(num, int):
        raise TypeError(u"Ошибочный тип данных 'num'", unicode(type(num)))

    # зависимости только от номера аппарата
    # на данный момент не используется, а берутся два разных
    # исходника прошивок
#        for key in self.P400:
#            adr = my_func.strHexToInt(key)
#            tmp = self.P400[key][num - 1].decode('hex')
#            source = source[:adr] + tmp + source[adr + len(tmp):]

    # строка '1BD0' зависит от частоты
    fr = calcFreq(freq).decode('hex')
    adr = my_func.strHexToInt('1BD0')
    source = source[:adr] + fr + source[adr + len(fr):]

    # строка '57D0' вычисляется относительно частоты и номера аппарата
    # xx (crc1) (crc2) xx xx xx (crc1, crc2 - двухбайтные)
    crc1 = calcCrc1(freq, num).decode('hex')
    crc2 = calcCrc2(freq, num).decode('hex')
    adr = my_func.strHexToInt('57D0') + 1
    source = source[:adr] + crc1 + crc2 + source[adr + len(crc1) + len(crc2):]

    return source

#------------------------------------------------------------------------------
def newRZSK_1v30(source, freq, num):
    ''' (str, int, int) -> str
        
        Корректирует файл прошивки версии 1v30 для РЗСК для указанной частоты
        и номера аппарата.
    '''


    def calcCrc1(freq, num):
        ''' (int, int) -> int
            
        Вычисление КС для заданной частоты и номера аппарата. 
        '''
        if (num == 1):
            crc = -39
        elif (num == 2):
            crc = 38
        return crc + 32 * freq


    def calcCrc2(freq, num):
        ''' (int, int) -> int
        
            Вычисление КС для заданной частоты и номера аппарата.
        '''
        if (num == 1):
            crc = 9
        elif (num == 2):
            crc = -10
        return crc + 8 * freq


    def calcFreq(freq):
        ''' (int) -> int
        
            Вычисление значения для частоты.
        '''
        return 16 * freq


    if not isinstance(source, str):
        raise TypeError(u"Ошибочный тип данных 'str'", unicode(type(source)))

    if not isinstance(freq, int):
        raise TypeError(u"Ошибочный тип данных 'freq'", unicode(type(freq)))

    if not isinstance(num, int):
        raise TypeError(u"Ошибочный тип данных 'num'", unicode(type(num)))

     # строка '1BD0' зависит от частоты
    fr = my_func.intToStrHex(calcFreq(freq))
    fr = fr[2:] + fr[:2]
    fr = fr.decode('hex')
    adr = my_func.strHexToInt('4DE6')
    source = source[:adr] + fr + source[adr + len(fr):]

    crc1 = my_func.intToStrHex(calcCrc1(freq, num))
    crc1 = crc1[2:] + crc1[:2]
    crc1 = crc1.decode('hex')
    adr = my_func.strHexToInt('7C1E')
    source = source[:adr] + crc1 + source[adr + len(crc1):]

    crc2 = my_func.intToStrHex(calcCrc2(freq, num))
    crc2 = crc2[2:] + crc2[:2]
    crc2 = crc2.decode('hex')
    adr = my_func.strHexToInt('7C22')
    source = source[:adr] + crc2 + source[adr + len(crc2):]

    return source


#-----------------------------------------------------------------------------
## Класс создания прошивки DSP АВАНТ.
class DSPhex():
    ## Данные для создания прошивок.
    #  Название аппарата задается на русском языке, для упорядочивания списка.
    FIRMWARE = {
                    u'Р400' : { '1v36' : ('P400_1v36', newP400_1v36),
                                '1v34' : ('P400_1v34', newP400_1v34),
                                '1v30' : ('P400_1v30', newP400_1v30)
                             },
                    u'РЗСК' : {
                                '1v30' : ('RZSK_1v30', newRZSK_1v30)
                             },
#                    u'К400' : (
#                              ('1.xx', 'K400_old')
#                              )
                }

    ## Путь для файлов исходных прошивок.
    DIR_DATA = "data/"
    ## Расширение файлов исходных прошивок.
    EXT_DATA = ".dat"
    ## Путь для сохранения файлов прошивок.
    DIR_HEX = "hex/"

    ## Тип аппарата.
    _device = None;
    ## Частота.
    _freq = None;
    ## Номер аппарата.
    _num = None;
    ## Версия прошивки.
    _version = None;
    ## Исходная прошивка
    _source = None

    ## Максимальная частота.
    MAX_FREQ = 1000
    ## Минимальная частота.
    MIN_FREQ = 16

    #
    def __init__(self, freq=100, num=1, device=u'Р400'):
        ''' (self, int, int, str) -> None
            
            Конструктор.
            @param freq Частота.
            @param num Номер аппарата.
            @param device Тип аппарата.
        '''
        self.setFrequence(freq)
        self.setNumber(num)
        self.setDevice(device)

    #
    def __str__(self):
        ''' (self) -> str
            
            Встроенная функция.
            @return Версия программы.
        '''
        return "Версия файла dsp.py %s" % VERSION

    #
    def getVersions(self, device=None):
        ''' (self, str) -> list of str
            
            Формирование списка версий прошивок доступных для заданного типа
            аппарата. Список упорядочен по убыванию.
            
            @param device Тип аппарата.
            @return Список версий прошивок.
        '''
        versions = []

        if device is None:
            device = self._device

        device = unicode(device)
        if self.FIRMWARE.has_key(device):
            versions = sorted(self.FIRMWARE[device], reverse=True)
        return versions

    #
    def setVersion(self, vers):
        ''' (self, str) -> str
            
            Установка версии прошивки.
            
            @param vers Версия прошивки.
            @return Установленная версию прошивки.
        '''

        if not self.FIRMWARE[self._device].has_key(vers):
            raise ValueError(u"Ошибочное значение переменной 'vers'.")

        self._version = vers
        return vers

    #
    def setFrequence(self, freq):
        ''' (self, str or number) -> int

            Установка частоты .
            
            @param freq Частота в диапазоне [MIN_FREQ, MAX_FREQ]кГц.
            @see MIN_FREQ
            @see MAX_FREQ
            @return Установленная частота.
        '''
        # проверка полученного номера аппарата
        try:
            freq = int(freq)
        except:
            raise TypeError(u"Неверный тип переменной 'freq'.")

        if freq < self.MIN_FREQ or freq > self.MAX_FREQ:
            raise ValueError(u"Ошибочное значение переменной 'freq'.")

        self._freq = freq
        return freq

    #
    def setNumber(self, num):
        ''' (self, str/number) -> int

            Установка номера аппарата. 
            
            @param num Номер аппарата в диапазоне [1, 2].
            @return Установленный номер аппарата.
        '''
        # проверка полученной частоты аппарата
        try:
            num = int(num)
        except:
            raise TypeError(u"Неверный тип переменной 'num'.")

        if num < 1 or num > 2:
            raise ValueError(u"Ошибочное значение переменной 'num'.")

        self._num = num
        return num

    #
    def getDevices(self):
        ''' (self) -> list of str
        
        
            Формирование списка версий аппаратов, для которых можно сформировать
            прошивку, упорядоченный по возрастанию.
            
            @return Список версий аппатов.
        '''
        return sorted(self.FIRMWARE)

    #
    def setDevice(self, device):
        ''' (self, str) -> None
            
            Установка типа аппарата.
  
            @param device Версия аппарата.
            @return Установленная версию аппарата.
        '''
        if not isinstance(device, (str, unicode)):
            raise TypeError(u"Неверный тип переменной 'device'.")

        if not device in self.FIRMWARE.keys():
            raise ValueError(u"Ошибочное значение переменной 'device'.")

        # в случае смены аппарата, установим последнюю версию прошивки для него

        if self._device != device:
            self._device = device
            self.setVersion(self.getVersions(device) [0])

        return device

    #
    def saveNewHEX(self, name=None):
        ''' (self, str) -> str

            Сохраниение файла прошивки с заданными параметрами. В случае если
            \a name не задано, сохраняется в текущий каталог с именем
            созданным на основе информации о версии прошивки, частоте и 
            номере аппарата.
            
            @param name Путь и(или) имя файла прошивки.
            @return Имя файла созданной прошивки.
        '''

        device = self._device
        freq = self._freq
        num = self._num
        vers = self._version

        self.loadSourceHEX()

        # вызов функции создания файла прошивки
        func = self.FIRMWARE[device] [vers] [1]
        try:
            source = func (self._source, freq, num)
        except Exception as inst:
            text = u"Ошибка вызова функции создания новой прошивки: "
            text += unicode(func)
            raise NameError(text)

        # формирование имени файла
        if name is None:
            name = unicode(self.DIR_HEX)
            name += "%s_%03d_%d.hex" % \
                (self.FIRMWARE[device] [vers] [0], freq, num)
        else:
            name = unicode(name)

        try:
            # создание папки для прошивок, в случае ее отсутствия
            if not os.path.exists(self.DIR_HEX):
                os.makedirs(self.DIR_HEX)

            # сохранение файла прошивки
            f = open(name, 'wb')
            f.write(source)
            f.close()
        except Exception as inst:
            raise IOError(inst)

        print u'Файл сохранен успешно', name
        return name

    #
    def loadSourceHEX(self):
        ''' (self) -> str

            Загрузка исходного файла прошивки.
            
            @return Имя исходного файла прошивки. 
        '''

        # выбор необходимого исходного файла прошивки
        name = self.DIR_DATA
        name += self.FIRMWARE[self._device][self._version][0]
        name += '_' + str(self._num)
        name += self.EXT_DATA

        try:
            name = unicode(name)
            f = open(name, 'rb')
            self._source = f.read()
        except:
            raise IOError(u"Ошибка открытия исходного файла прошивки.")

        return name



#-----------------------------------------------------------------------------
if __name__ == '__main__':
    ''' Создание файла прошивки с заданной частотой и номером. 
        По умолчанию будет создана прошивка Р400_1v36 100кГц-1.
        Ключи:
        -f[number] - частота [MIN_FREQ, MAX_FREQ]кГц, например -f100
        -n[number] - номер аппарата [1, 2], например -n2
        -d[name] - тип аппарата [Р400, РЗСК, К400], например -dP400
        -v[vers] - версия прошивки, например -v1v30
    '''

    dspHEX = DSPhex()

    # установка папаремтров заданных ключами
    for i in range(1, len(sys.argv)):
        arg = sys.argv[i]
        if arg[:2] == '-f':
            dspHEX.setFrequence(arg[2:])
        elif arg[:2] == '-n':
            dspHEX.setNumber(arg[2:])
        elif arg[:2] == '-d':
            dspHEX.setDevice(arg[2:])
        elif arg[:2] == '-v':
            dspHEX.setFrequence(arg[2:])

    try:
        dspHEX.loadSourceHEX()
    except:
        print u'Не удалось загрузить файл прошивки'

    try:
        dspHEX.saveNewHEX()
    except:
        print u'Не удалось сохранить файл прошивки'
