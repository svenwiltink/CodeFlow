from setuptools import setup, find_packages

setup(name='CodeFlow',
      author='Sven Wiltink',
      author_email='sven.wiltink@hotmail.com',
      description="A small workflow module",
      url='https://github.com/SvenWiltink/PyFlow',
      version='0.0.3',
      packages=find_packages(),
      package_dir={'': 'src'},
      test_suite='nose.collector'
      )
