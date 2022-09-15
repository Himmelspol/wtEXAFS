# -*- coding:utf-8 -*-

"""
@author Zhihang Ye
@contact: yezhihang@live.com
@date 2022/09/07
------------------ Description -----------------------
This is a python GUI of wavelet transformation for EXAFS data.
And The python version used is 3.7.
The users could import normalized EXAFS data extracted form ATHENA in this GUI.
This GUI would return the result of wavelet transform for users' data.
And the users could view processed data as a 2D graph.
------------------ Support file of GUI -----------------------
The GUI consists of the following files:
1.  para.py ---- stores the necessary variables of WT
2.  path.py ---- stores the methods to get the path and the path names of temp files
3.  tools.py    ---- stores the methods of judging and prompting
4.  waveletMethod.py    ---- stores the methods to constructing wavelet and doing WT
5.  fileOper.py ---- execute TXT file data processing
6   showData.py ---- methods of showing the data
7.  subWindow.py ---- class of other windows
8.  mianWindow.py (THIS FILE)   ---- mainwindow and entrance of the GUI
9.  resources (folder)  ---- an folder stores logo.ico, model data, tips file and other temp files
------------------ PS -----------------------
Because the author is a beginner to Python,
there may be many irregularities and ambiguities in the code.:)
"""

__version__ = '0.2.1'
__author__ = 'Zhihang Ye'
__email__ = 'yezhihang@live.com'

'''
from .fileOper import *
from .path import *
from .tools import *
from .para import *
from .showData import *
from .mainWindow import *
from .subWindow import *
from .waveletMethod import *
'''
