from distutils.core import setup
import py2exe
import os
 
includes = ['tinys3','yaml','boto']
excludes = ['_gtkagg', 'bsddb', 'curses', 'pywin.debugger',
            'pywin.debugger.dbgcon', 'pywin.dialogs']
packages = []
dll_excludes = []
consolebuild = ['tsback.py']
options = {"py2exe": {"compressed": 2, 
                          "optimize": 2,
                          "unbuffered": True,
                          "includes": includes,
                          "excludes": excludes,
                          "packages": packages,
                          "dll_excludes": dll_excludes,
                          "bundle_files": 2,
                          "dist_dir": "dist",
                          "xref": False,
                          "skip_archive": False,
                          "ascii": False,
                          "dist_dir": "..\\dist",
                          "custom_boot_script": ''
                         }
              }
 
setup(name="Tableau Utils", description="bunch of useful utilities for Tableau", author="Shankar Narayanan SGS", platforms="windows", options = options, zipfile = "library.zip",console=consolebuild)
