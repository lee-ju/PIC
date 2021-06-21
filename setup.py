from setuptools import setup

setup(
    name='PIC',
    version='0.0.1',
    description='Patent with Indirect Citation',
    url='https://github.com/lee-ju/PIC.git',
    author='Juhyun Lee',
    author_email='leeju@korea.ac.kr',
    license='Juhyun Lee',
    packages=['PIC'],
    zip_safe=False,
    install_requires=[
        'networkx'
    ]
)
