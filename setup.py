from setuptools import setup, find_packages

classifiers = [
        'Intended Audience :: Education',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows :: Windows 10 IoT Core'
        'Operating System :: POSIX :: Linux :: Raspbian'
        'Operating System :: POSIX :: Linux :: Kali',
    ]

setup(
    name='adeept_picarpro',
    version='0.1',
    packages=find_packages(),
    license='MIT',
    description='A Python package to control the Adeept Picar-Pro robot',
    long_description=open('README.md').read(),
    author=['Alyson Melissa Sánchez Serratos', 
            'Rodrigo Antonio Benítez De La Portilla', 
            'Liliana Camacho Suárez',
            'Ángel Rogelio Cruz Ibarra'],
    install_requires=[
        'time', 
        'RPi.GPIO', 
        'sys', 
        'rpi_ws281x', 
        'threading', 
        'luma.core',
        'luma.oled',
        'adafruit-pca9685',
        'mpu6050-raspberrypi',
        'future',
        'openCV',
        'flask',
        'flask_cors',
        'datetime',
        'imutils',
        'numpy',
        'os',
        'importlib'], 
    url='https://github.com/Rodrig0at/Car-Robot.git',
    classifiers= classifiers,
)