# -*- coding: cp1251 -*-
import sys

def intToStrHex(val):
	''' (int) -> str
	
		�������������� ������ ����� � ������ HEX.
		
		>>> intToStrHex(12)
		'0C'
		>>> intToStrHex(2048)
		'0800'
	'''
	val = "%x" % val
	if len(val) % 2 == 1:
		val = '0' + val
	return val
	
def strHexToInt(val):
	''' (str) -> int
	
		�������������� ������ HEX � ����� �����.
		
		>>> strHexToInt("CC0")
		3264
		>>> strHexToInt("12")
		18
	'''
	return int(val, 16) 
	
def charToStrHex(val):
	''' (str) -> str
	
		�������������� ��������� � ������ HEX.
		
		>>> charToStrHex('1')
		'31'
		>>> 'A'.encode('hex')
		'41'
		>>> "123".encode('hex')
		'313233'
	'''
	return val.encode('hex')
	
def strHexToChar(val):
	''' (str) -> str
		
		�������������� ������ HEX � �������.
		
		>>> '31'.decode('hex')
		'1'
		>>> '41'.decode('hex')
		'A'
		>>> "313233".decode('hex')
		'123'
	'''
	return val.decode('hex')
	
if __name__ == '__main__':
	args = sys.argv
	for arg in args:
		if arg == '/?':
			print u'�������:'