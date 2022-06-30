#encod: utf-8



"""
this is a test package. want to know how the init is work.
话说，这个只有__all__ 在用， 仅仅是限制import packageTest.* 时哪个会被默认导入。
只要我们import 了这个package, __init__.py就会自动运行。

"""

import sys, os, time, io, traceback, warnings 

from string import Template

__all__ = [ 'raiseExceptions']

import threading

__author__  = "WP test"
__status__  = "production" 
__version__ = "0.5.1.2"
__date__    = "07 February 2010"

globalP1 = 1

print('run from packageTest. __init__.py')
