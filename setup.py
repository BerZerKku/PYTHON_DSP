# -*- coding: utf-8 -*-
import sys
from distutils.core import setup
from glob import glob
import py2exe

sys.path.append("D:\\Program Files\\Microsoft Visual Studio 9.0\\VC\\redist\\x86\\Microsoft.VC90.CRT")
data_files = [("Microsoft.VC90.CRT", glob(r'D:\Program Files\Microsoft Visual Studio 9.0\VC\redist\x86\Microsoft.VC90.CRT\*.*'))]
mydata_files = ('', ["Apps.png"])
data_files.append(mydata_files)
setup(
	# копирование библиотек Visual Studio
	data_files=data_files,
	#w9xpopen.exe - для совместимости с win 95/98
	dll_excludes=['w9xpopen.exe'],
	# windows - GUI (может быть console)
	# icon_resources -> установка иконки для скомпилированного проекта
    windows=[{"script":"dsp_gui.py", "icon_resources": [(1, "Apps_24x24.ico")]}],
	#
    options={"py2exe": {"includes":["sip"]}}
)
