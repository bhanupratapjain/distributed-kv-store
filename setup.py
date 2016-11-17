from setuptools import setup

setup(name='Distributed Key Value Store',
      version='0.1',
      description='Distributed Key Value Store',
      url='https://github.ccs.neu.edu/bhanupratapjain/distributed-kv-store',
      author='bhanupratapjain, sourabhb, vignushu',
      license='MIT',
      py_modules=['store', 'client'],
      install_requires=[
          'Click',
      ],
      entry_points={
          "console_scripts": [
              "store = store:cli",
              "client= client:cli"
          ]
      },
      zip_safe=False)
