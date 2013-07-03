try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='zencoder',
      version='0.6.5',
      description='Integration library for Zencoder',
      author='Alex Schworer',
      author_email='alex.schworer@gmail.com',
      url='http://github.com/schworer/zencoder-py',
      license="MIT License",
      install_requires=['requests>=1.0'],
      tests_require=['mock', 'nose'],
      packages=['zencoder'],
      platforms='any',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Topic :: Software Development :: Libraries :: Python Modules'
      ]
     )

