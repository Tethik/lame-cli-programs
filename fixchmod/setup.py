from distutils.core import setup
setup(name='chmodfix',
      version='1.1',
      py_modules=['chmodfix'],
      entry_points={
          'console_scripts': ['chmodfix=chmodfix:main'],
      }
      )
