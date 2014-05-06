# -*- coding: utf-8 -*-
import sys
import os
import py2exe
from distutils.core import setup
from glob import glob


# подключение библиотек Visual Studio
#sys.path.append("D:\\Program Files\\Microsoft Visual Studio 9.0\\VC\\redist\\x86\\Microsoft.VC90.CRT")
#data_files = [("Microsoft.VC90.CRT", glob(r'D:\Program Files\Microsoft Visual Studio 9.0\VC\redist\x86\Microsoft.VC90.CRT\*.*'))]
sys.path.append("D:\\work\\Python\\Distr\\!setup\\toExe\\Microsoft.VC90.CRT")
data_files = [("Microsoft.VC90.CRT", glob(r'D:\work\Python\Distr\!setup\toExe\Microsoft.VC90.CRT\*.*'))]


# подключение своих файлов
# где 'data' - каталог в который будут скопированы файлы
mydata_files = ('data', [])
# добавление всего содержимого папки 'data/'
for files in os.listdir('data/'):
    mydata_files[1].append('data/' + files)
data_files.append(mydata_files)

includes = ["sip"]
excludes = ['w9xpopen.exe']
packages = []
dll_excludes = ['libgdk-win32-2.0-0.dll', 'libgobject-2.0-0.dll', 'tcl84.dll', 'tk84.dll', 'w9xpopen.exe']

setup(
	# копирование библиотек Visual Studio
	data_files=data_files,
	#w9xpopen.exe - для совместимости с win 95/98
	#dll_excludes=['w9xpopen.exe'],
	# windows - GUI (может быть console)
	# icon_resources -> установка иконки для скомпилированного проекта
    windows=[{"script":"dsp_gui.py", "icon_resources": [(1, "icons/Apps_24x24.ico")]}],
	#
    #options={"py2exe": {"includes":["sip"]}}
	options = {"py2exe": {"compressed": 2, 
						  "optimize": 2,
						  "includes": includes,
                          "excludes": excludes,
                          "packages": packages,
                          "dll_excludes": dll_excludes,
                          "bundle_files": 3,
                          "dist_dir": "dist",
                          "xref": False,
                          "skip_archive": False,
                          "ascii": False,
                          "custom_boot_script": '',
                         }
              },
	zipfile=None
)
