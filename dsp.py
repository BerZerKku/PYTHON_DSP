# -*- coding: utf-8 -*-
import sys
import my_func

class DSPhex():
    def __init__(self, freq=100, num=1, device='P400'):
        ''' (int, int, str) -> None

            freq - частота в кГц
            num - номер аппарата, 1..3
            source - файл исходной прошивки
        '''
        self.DEVICE = ('P400', 'RZSK', 'K400')
        
        self.setFrequence(freq)
        self.setNumber(num)
        self.setDevice(device)    
    
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
            print "Error:",
            print u"Неверный тип переменной",  freq, type(freq)
            raise TypeError
        if freq < 16 or freq > 1000:     
            print "Error:",
            print u"Полученная частота выходит за диапазон [16, 1000]кГц: ",freq
            raise ValueError
        self._freq = freq

        return freq

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
            print "Error:",
            print u"Неверный тип переменной", num, type(num)
            raise TypeError
        if num < 1 or num > 3:
            print "Error:",
            print u"Полученный номер аппарата выходит за диапазон [1, 3]:",num
            raise ValueError
        self._num = num

        return num

    def setDevice(self, device):
        ''' (self, str) -> None

            Установка типа аппарата DEVICE.
            Возвращает установленный тип аппарата.
        '''
        if not isinstance(device, str):
            print u"Error:",
            print u"Неверный тип переменной", device, type(device) 
            raise TypeError
        if not device in self.DEVICE:
            print u"Error:"
            print u"Ошибочное значение типа аппарата.", device
            raise ValueError
        self._device = device

        return device

    def saveNewHEX(self, source=None, name=None):
        ''' (self, str, str) -> str

            Сохраниение файла прошивки с новыми параметрами. В случае если
            name не задано, сохраняется в текущий каталог с именем
            %device_%freq_%num.hex. Можно задать свой текст прошивки source.

            В случае успешного сохранения, возвращает имя файла.
        '''
        device = self._device
        freq = self._freq
        num = self._num
        
        # формирование имени файла
        if name is None: 
            name = "%s_%03d_%d.hex" % (device, freq, num)
              
        if device == 'P400':
            source = self.newP400()
        elif device == 'RZSK':
            source = self.newRZSK()
        try:
            f = open(name, 'wb')
            f.write(source)
            f.close()
        except:
            print u"Error:",
            print u"Ошибка сохранения файла прошивки:", name, type(name)
            raise IOError
        print u'Файл сохранен успешно', name
        
        return name
        
    def loadSourceHEX(self, device=None, name=None):
        ''' (self, str, str) -> str

            Загрузка исходного файла прошивки в _source. В случае если name не
            задано загружается файл соответсвующий выбранному типу устройства.
            device должен быть значением из DEVICE.
            В случае успешной загрузки, возвращает имя файла.
        '''
        # загрузка файла в зависимости от типа аппарата
        if name is None:
            if device is None:
                device = self._device
        
        if device in self.DEVICE:
            if device == 'RZSK':
                # для упрощения кода в РЗСК загружается исходник 1 или 2 аппарата
                name = device + '_' + str(self._num) + '.dat'
            else:
                name = device + '.dat'
        else:
            print u"Error: ",
            print u"Неверно задан тип аппарата: ", device
        
        try:
            f = open(name, 'rb')
            self._source = f.read()
        except:
            print u"Error:",
            print u"Ошибка открытия исходного файла прошивки."
            print u'Проверьте наличие файла "P400.dat".'
            raise IOError
        
        return name

    def newP400(self, source=None, freq=None, num=None):
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
        for key in self.P400:
            adr = my_func.strHexToInt(key)
            tmp = self.P400[key][num - 1].decode('hex')
            source = source[:adr] + tmp + source[adr + len(tmp):]

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
                
    def newRZSK(self, source=None, freq=None, num=None):
        ''' (dsphex, str, int, int)
        
            Формирование нового файла прошивки для РЗСК.
            На вход можно подать прошивику, по умолчанию будет использоваться
            загруженный ранее(для 1 и 2 номера разные). 
            Возвращает содержимое нового файла прошивки.
        '''
        
        def calcCrc1(freq, num):
            ''' (int, int) -> int
            
                Возвращает контрольную сумму в зависимости от номера аппарата
                и частоты.
            '''
            
            if (num == 1):
                crc = -39
            elif (num == 2):
                crc = 38
            inc = 32
            
            crc += inc * freq 
            return crc
        
        def calcCrc2(freq, num):
            ''' (int, int) -> int
            
                Возвращает контрольную сумму в зависимости от номера аппарата
                и частоты.
            '''
            
            if (num == 1):
                crc = 9
            elif (num == 2):
                crc = -10    
            inc = 8
            
            crc += inc * freq
            return crc
        
        def calcFreq(freq):
            ''' (int) -> int
                
                Возвращает число соовтетствующее заданной частоте.
            '''
            
            val = 0
            inc = 16
            
            val += inc * freq
            return val
        
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
    
