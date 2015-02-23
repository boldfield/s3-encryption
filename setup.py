from setuptools import setup, find_packages
import os


def load_file(name):
    with open(name) as fs:
        content = fs.read().strip().strip('\n')
    return content


README = load_file('README.md')
VERSION = load_file(os.path.join('s3_encryption', 'VERSION'))

with open('requirements.txt', 'r') as fs:
    install_requires = filter(lambda x: not not x, map(lambda y: y.strip('\n'), fs.readlines()))


tests_require = [
    'nose==1.2.1',
    'mock==1.0.0',
    'coverage==3.5.2',
]

entry_points = dict()

setup(name='s3-encryption',
      version=VERSION,
      description='Thin wrapper around boto3 S3 client which supports client side encryption compatable with ruby aws-sdk-core',
      long_description=README,
      keywords='S3 encryption',
      author='Brian Oldfield',
      author_email='brian@oldfield.io',
      url='https://github.com/boldfield/s3-encryption',
      download_url='https://github.com/boldfield/s3-encryption/tarball/{}'.format(VERSION),
      license='BSD',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      extras_require=dict(tests=tests_require),
      install_requires=install_requires,
      entry_points=entry_points,
      scripts=[],
      package_data={'s3_encryption': ['VERSION']},
      classifiers=['Development Status :: 4 - Beta',
                   'Intended Audience :: Developers'])
