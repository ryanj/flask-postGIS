from setuptools import setup

setup(name='PGParks',
      version='1.0',
      description='National Parks Finder',
      author='Ryan Jarvinen',
      author_email='ryanj@redhat.com',
      url='http://www.python.org/sigs/distutils-sig/',
     install_requires=['Flask>=0.10.1', 'MarkupSafe' , 'Flask-SQLAlchemy>=1.0'],
     )
