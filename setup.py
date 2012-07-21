# coding: utf-8

import sys
from setuptools import setup
from setup_commands import Test3k


# hack to avoid TypeError on
# interpreter shutdown
try:
    import multiprocessing
except ImportError:
    pass


if sys.version < '3':
    author_name = unicode('Álvaro Justen'.decode('utf-8'))
    cmdclass = {}
else:
    author_name = 'Álvaro Justen'
    cmdclass = {'test': Test3k}

setup(name='mongodict',
      version='0.1.1',
      author=author_name,
      author_email='alvarojusten@gmail.com',
      url='https://github.com/turicas/mongodict/',
      description='MongoDB-backed Python dict-like interface',
      zip_safe=True,
      py_modules=['mongodict'],
      install_requires=['pymongo'],
      test_suite='nose.collector',
      license='GPL3',
      keywords=['key-value', 'database', 'mongodb', 'dictionary'],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2.7',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      use_2to3=True,
      use_2to3_fixers=['fixes'],
      cmdclass=cmdclass,
)
