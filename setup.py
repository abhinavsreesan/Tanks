from distutils.core import setup
import py2exe

setup(
    console=['ESP.py'],
    options = {
        'py2exe':{
            'packages':['pygame','socket','sys','opt','Tkinter']        
        }
    }
)