# -*- coding: cp1251 -*-
import sys
import struct


def intToStrHex(val, num=None, arch="be"):
	''' (int) -> str

		Преобразование целого числа в строку HEX.
		
		@param val преобразуемое число
		@param num кол-во знаков, если None - то доводится до четного кол-ва
		@param arch Архитектура платформы.
		@arg "le" little-endian младшим байтов вперед
		@arg "be" big-endian старшим байтом вперед
		
		>>> intToStrHex(12)
		'0C'
		>>> intToStrHex(2048)
		'0800'
	'''
	if not isinstance(val, int):
		txt = u"Error: Ошибочный тип данных,", type(val)
		raise TypeError(txt)
	
	val = "%x" % val
	
	if num is None:
		if len(val) % 2 == 1:
			val = '0' + val
	elif isinstance(num, int):
		# если знаков не хватает, добавим ведущий ноль
		while len(val) < num:
			val = '0' + val
		# если знаков больше, уберем ведущие
		while len(val) > num:
			val = val[1:]
	else:
		txt = u"Error: Ошибочный тип данных,", type(num)
		raise TypeError(num)
	
	if arch == "be":
		pass
	elif arch == "le":
		tmp = ""
		for i in range(0, len(val), 2):
			tmp = val[i: i + 2] + tmp
		val = tmp
	else:
		txt = u"Error: Выбрана неверная архитектура."
		raise ValueError(txt)
		
	return val.upper()


def strHexToInt(val, arch="be"):
	''' (str) -> int

		Преобразование строки HEX в целое число.
		
		@param val преобразуемая строка
		@param arch Архитектура платформы.
		@arg "le" little-endian младшим байтов вперед
		@arg "be" big-endian старшим байтом вперед

		>>> strHexToInt("CC0")
		3264
		>>> strHexToInt("12")
		18
'''
	if not isinstance(val, str):
		txt = u"Error: Ошибочный тип данных,", type(val)
		raise TypeError(txt)
	
	if arch == "be":
		pass
	elif arch == "le":
		# добавление ведущего нуля, при необходимости
		if len(val) % 2 == 1:
			val = "0" + val
		# переворот строки по 2 символа
		tmp = ""
		for i in range(0, len(val), 2):
			tmp = val[i: i + 2] + tmp
		val = tmp
	else:
		txt = u"Error: Выбрана неверная архитектура."
		raise ValueError(txt)
	
	try:
		val = int(val, 16)
	except:
		txt = u"Error: Ошибка преобразования."
		raise ValueError(txt)
	
	return val


def charToStrHex(val):
	''' (str) -> str
		Преобразование символов в строку hex.

		>>> charToStrHex('1')
		'31'
		>>> charToStrHex('A')
		'41'
		>>> charToStrHex('123')
		'313233'
	'''
	if not isinstance(val, str):
		txt = u"Error: Ошибочный тип данных,", type(val)
		raise TypeError(txt)
	
	return val.encode('hex')


def strHexToChar(val):
	''' (str) -> str

		Преобразование строки HEX в символы.

		>>> strHexToChar('31')
		'1'
		>>> strHexToChar('41')
		'A'
		>>> strHexToChar("313233")
		'123'
	'''
	if not isinstance(val, str):
		txt = u"Error: Ошибочный тип данных,", type(val)
		raise TypeError(txt)
	
	try:
		val = val.decode('hex')
	except:
		txt = u"Error: Ошибка преобразования."
		raise ValueError(txt)
	
	return val


def strHexToFloat(s, arch="be"):
	''' (str) -> float
		
		Возвращает float полученный hex-cтрокой.
		@param arch выбор архитектуры
		@arg "le" little-endian младшим байтом вперед
		@arg "be" big-endian старшим байтом вперед
		
		>>> strHexToFloat("41973333")
		18.899999618530273
		>>> strHexToFloat("41973333", "le")
		4.18142498403995e-08
		>>> strHexToFloat("470FC614")
		36806.078125
	'''
	if not isinstance(s, str):
		txt = u"Error: Ошибочный тип данных,", type(s)
		raise TypeError(txt)
	
	bins = ''.join(chr(int(s[x:x + 2], 16)) for x in range(0, len(s), 2))
	
	if arch == "le":
		arch = '<f'
	elif arch == "be":
		arch = '>f'
	else:
		txt = u"Error: Выбрана неверная архитектура."
		raise ValueError(txt)
	
	try:
		val = struct.unpack(arch, bins)[0]
	except:
		txt = u"Error: Ошибка преобразования."
		raise ValueError(txt)
	
	return val


def floatToStrHex(val, arch="be"):
	''' (float) -> str

		Возвращает float преобразованный в hex-строку.
		@param arch выбор архитектуры
		@arg "le" little-endian младшим байтом вперед
		@arg "be" "big-endian" старшим байтом вперед
		
		>>> floatToStrHex(3.99)
		"407f5c29"
		>>> floatToStrHex(3.99, "le")
		"295C7F40"
		>>> floatToStrHex(12.18)
		"4142e148"
	'''
	if not isinstance(val, float):
		txt = u"Error: Ошибочный тип данных,", type(val)
		raise TypeError(txt)
	
	if arch == "le":
		arch = '<f'
	elif arch == "be":
		arch = '>f'
	else:
		txt = u"Error: Выбрана неверная архитектура."
		raise ValueError(txt)
	s = struct.pack(arch, val)
	
	return ''.join('%.2x' % ord(c) for c in s).upper()
		
if __name__ == '__main__':
	args = sys.argv
	for arg in args:
		if arg == '/?':
			print u'Справка:'


import unittest


class TestMyFunc(unittest.TestCase):
	"""${short_summary_of_testcase}
	"""
# 	def setUp(self):
# #        self.testFrame = TabCheck()
# 		self.app = QtGui.QApplication(sys.argv)
#       	self.form = TabCheck()

#   	def tearDown(self):
#   		"""${no_tearDown_required}
#       	"""
#   	    pass  # skip tearDown
	def testIntToStrHex(self):
		""" (None) -> None
			Проверка результата работы функции intToStrHex.
		"""
		self.assertEqual(intToStrHex(12), '0C')
		self.assertEqual(intToStrHex(12, num=4), '000C')
		self.assertEqual(intToStrHex(2049), '0801')
		self.assertEqual(intToStrHex(2049, num=2), '01')
		self.assertEqual(intToStrHex(2049, arch="le"), '0108')
		self.assertEqual
		
		self.assertRaises(TypeError, intToStrHex, "1")
		self.assertRaises(TypeError, intToStrHex, 12, '12')
		self.assertRaises(ValueError, intToStrHex, 12, None, "d")

	def testStrHexToInt(self):
		""" (None) -> None
			Проверка результата работы функции strHexToInt.
		"""
		self.assertEqual(strHexToInt("CC0"), 3264)
		self.assertEqual(strHexToInt("CC0", "be"), 3264)
		self.assertEqual(strHexToInt("12"), 18)
		self.assertEqual(strHexToInt("0CC0", "le"), 49164)
		
		self.assertRaises(ValueError, strHexToInt, "CC0", "d")
		self.assertRaises(TypeError, strHexToInt, 12)
		self.assertRaises(ValueError, strHexToInt, ":1")
	
	def testCharToStrHex(self):
		""" (None) -> None
			Проверка результата работы функции charToStrHex.
		"""
		self.assertEqual(charToStrHex("1"), "31")
		self.assertEqual(charToStrHex("A"), "41")
		self.assertEqual(charToStrHex("123"), "313233")
		
		self.assertRaises(TypeError, charToStrHex, 12)
	
	def testStrHexToChar(self):
		""" (None) -> None
			Проверка результата работы функции strHexToChar.
		"""
		self.assertEqual(strHexToChar("31"), "1")
		self.assertEqual(strHexToChar("41"), "A")
		self.assertEqual(strHexToChar("313233"), "123")

		self.assertRaises(TypeError, strHexToChar, 12)
		self.assertRaises(ValueError, strHexToChar, "1")
		self.assertRaises(ValueError, strHexToChar, ":1")
	
	def testHextoFloat(self):
		""" (None) -> None
			Проверка результата работы функции hexToFloat.
		"""
		self.assertEqual(strHexToFloat("41973333"), 18.899999618530273)
		self.assertEqual(strHexToFloat("41973333", "le"), 4.18142498403995e-08)
		self.assertEqual(strHexToFloat("470FC614"), 36806.078125)
		
		self.assertRaises(TypeError, strHexToFloat, 12)
		self.assertRaises(ValueError, strHexToFloat, "41973333", "d")
		self.assertRaises(ValueError, strHexToFloat, ":70FC614")
		
	def testFloatToStrHex(self):
		""" (None) -> None
			Проверка результата работы функции floatToHex.
		"""
		self.assertEqual(floatToStrHex(3.99), "407F5C29")
		self.assertEqual(floatToStrHex(3.99, "le"), "295C7F40")
		self.assertEqual(floatToStrHex(12.18), "4142E148")
		
		self.assertRaises(TypeError, floatToStrHex, 12)
		self.assertRaises(ValueError, floatToStrHex, 12.5, "d")
