# -*- coding: utf-8 -*-
import sys
import os
import my_func


#####
class DSPhex():
    VERSION = u"1v03"
    FIRMWARE = {
                    u'Р400' : { '1v36' : 'P400_1v36',
                                '1v34' : 'P400_1v34',
                                '1v30' : 'P400_1v30'
                             },
                    u'РЗСК' : {
                                '1v30' : 'RZSK_1v30'
                             },
#                    u'К400' : (
#                              ('1.xx', 'K400_old')
#                              )
                }
    DIR_DATA = "data/"
    EXT_DATA = ".dat"
    DIR_HEX = "hex/"
    
    _device = None;
    _freq = None;
    _num = None;
    _version = None;
    
#####
    def __init__(self, freq=100, num=1, device=u'Р400'):
        ''' (self, int, int, str) -> None

            freq - частота в кГц
            num - номер аппарата, 1..3
            source - файл исходной прошивки
        '''
        self.setFrequence(freq)
        self.setNumber(num)
        self.setDevice(device)  
        
#####     
    def __str__(self):
        ''' (self) -> str
        
            Возвращает версию программы.
        '''
        return self.VERSION    
        
#####
    def getVersions(self, device=None):
        ''' (self, str) -> list of str
            
            Возвращает список возможных версий прошивок для заданного типа
            аппарата, упорядоченный по убыванию.
            В случае ошибочного типа возвращается пустой список.
        '''
        versions = []
        
        if device is None:
            device = self._device
            
        device = unicode(device)
        if self.FIRMWARE.has_key(device):
            versions = sorted(self.FIRMWARE[device], reverse = True)
        return versions
    
#####
    def setVersion(self, vers):
        ''' (self, str) -> str
            
            Установка версии прошивки.
            Возвращает установленную версию.
        '''    
        
        if not self.FIRMWARE[self._device].has_key(vers):
            raise ValueError(u"Ошибочное значение переменной 'vers'.")
        
        self._version = vers
        return vers 
               
#####            
    def setFrequence(self, freq):
        ''' (self, str/number) -> int

            Установка частоты [16, 1000] кГц. Может быть задано строкой
            или числом.
            Возвращает установленную частоту.
        '''
        # проверка полученного номера аппарата
        try:
            freq = int(freq)
        except:
            raise TypeError(u"Неверный тип переменной 'freq'.")
        
        if freq < 16 or freq > 1000:     
            raise ValueError(u"Ошибочное значение переменной 'freq'.")
        
        self._freq = freq
        return freq

#####
    def setNumber(self, num):
        ''' (self, str/number) -> int

            Установка номера аппарата [1, 3]. Может быть задано строкой
            или числом.
            Возвращает установленный номер аппарата.
        '''
        # проверка полученной частоты аппарата
        try:
            num = int(num)
        except:
            raise TypeError(u"Неверный тип переменной 'num'.")
        
        if num < 1 or num > 3:
            raise ValueError(u"Ошибочное значение переменной 'num'.")
        
        self._num = num
        return num
    
#####
    def getDevices(self):
        ''' (self) -> list of str
        
            Возвращает список аппаратов, для которых можно сформировать
            прошивку, упорядоченный по возрастанию.
        '''
        return sorted(self.FIRMWARE)  
    
#####
    def setDevice(self, device):
        ''' (self, str) -> None

            Установка типа аппарата DEVICE.
            Возвращает установленный тип аппарата.
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

#####
    def saveNewHEX(self, name=None):
        ''' (self, str) -> str

            Сохраниение файла прошивки с новыми параметрами. В случае если
            name не задано, сохраняется в текущий каталог с именем
            созданным на основе информации о версии прошивки, частоте и 
            номере аппарата.

            В случае успешного сохранения, возвращает имя файла.
        '''
        device = self._device
        freq = self._freq
        num = self._num
        vers = self._version
        
        self.loadSourceHEX()
              
        if device == u'Р400':
            if vers == '1v36':
                source = self.newP400_1v36()
            elif vers == '1v34':
                source = self.newP400_1v34()
            elif vers == '1v30':
                source = self.newP400_1v30()
        elif device == u'РЗСК':
            source = self.newRZSK_1v30()
        
        # формирование имени файла
        if name is None: 
            name = unicode(self.DIR_HEX)
            name += "%s_%03d_%d.hex" % (self.FIRMWARE[device] [vers], freq, num)
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
        
#####  
    def loadSourceHEX(self):
        ''' (self) -> str

            Загрузка исходного файла прошивки в _source. 
            В случае успешной загрузки, возвращает имя файла.
        '''
        
        # выбор исходного файла прошивки на основании уставок
        name = self.DIR_DATA
        name += self.FIRMWARE[self._device][self._version]
        name += '_' + str(self._num)
        name += self.EXT_DATA
            
        try:
            name = unicode(name)
            f = open(name, 'rb')
            self._source = f.read()
        except:
            print name
            raise IOError(u"Ошибка открытия исходного файла прошивки.")
        
        return name

#####
    def newP400_1v30(self, source=None, freq=None, num=None):
        ''' (str) -> sr

            Формирование нового файла прошивки для Р400.
            На вход можно подать прошивику, по умолчанию
            будет использоваться загруженный ранее.
            Возвращает содержимое нового файла прошивки.
        '''
        # массив изменяемых строк в заисисмости от номера аппарата
        # значение словаря  зависит от номера аппарата [1, 2] 
        self.P400 = {'1320': ['1310091210095048', '1210091310095048'],
                     '1378': ['0009131009121009', '0009121009131009'],
                     '1C88': ['8048980A01109080', '9048980A01109080'],
                     '1CA8': ['7598904898AF8006', '7598804898AF8006'],
                     '57B0': ['00010019700000FB', '00020019700000FB']}
        # строка '57D0' вычисляется относительно частоты и номера аппарата
        # xx (crc1) (crc2) xx xx xx (crc1, crc2 - двухбайтные)
        # строка '1BD0' зависит от частоты
        # (fr) xx xx xx xx xx xx
        
        #####       
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
        
        #####
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
        
        #####
        def calcFreq(val):
            val = val = "%02x0" % val
            if len(val) < 4:
                val = '0' + val
            val = val[2:] + val[:2]
            return val.upper()
        
        if freq is None:
            freq = self._freq

        if num is None:
            num = self._num

        if source is None:
            source = self._source

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
             
    #           
    def newRZSK_1v30(self, source=None, freq=None, num=None):
        ''' (dsphex, str, int, int)
        
            Формирование нового файла прошивки для РЗСК.
            На вход можно подать прошивику, по умолчанию будет использоваться
            загруженный ранее(для 1 и 2 номера разные). 
            Возвращает содержимое нового файла прошивки.
        '''
        
        #####
        def calcCrc1(freq, num):
            ''' (int, int) -> int
                Возвращает контрольную сумму в зависимости от номера аппарата
                и частоты.
            '''   
            if (num == 1):
                crc = -39
            elif (num == 2):
                crc = 38
            return crc + 32*freq
        
        #####
        def calcCrc2(freq, num):
            ''' (int, int) -> int
                Возвращает контрольную сумму в зависимости от номера аппарата
                и частоты.
            '''
            if (num == 1):
                crc = 9
            elif (num == 2):
                crc = -10    
            return crc + 8*freq
        
        #####
        def calcFreq(freq):
            ''' (int) -> int
                Возвращает число соовтетствующее заданной частоте.
            '''
            return 16 * freq
        
        
        if freq is None:
            freq = self._freq

        if num is None:
            num = self._num

        if source is None:
            source = self._source
        
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
        
#       
if __name__ == '__main__':
    ''' Создание файла прошивки с заданной частотой и номером. По умолчанию
        будет создана прошивка 100кГц-1
        Ключи:
        -f[number] - частота [10, 1000]кГц, например -f100
        -n[number] - номер аппарата [1, 3], например -n2
        -d[name] - тип аппарата [P400, PZSK, K400], например -dP400
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
    
    try:
        dspHEX.loadSourceHEX()
    except:
        print u'Не удалось загрузить файл прошивки'

    try:
        dspHEX.saveNewHEX()
    except:
        print u'Не удалось сохранить файл прошивки'
    
