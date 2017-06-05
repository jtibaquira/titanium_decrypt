from setuptools import setup

setup(
    name='titanium_decrypt',
    version='1.0.0',
    description='Extraction tool for encrypted Appcelerator Titanium android apps',
    author='wiez',
    license='MIT',
    install_requires=['pycrypto', 'jsbeautifier'],
    py_modules=['titanium_decrypt'],
    entry_points={
        'console_scripts': [
            'titanium_decrypt = titanium_decrypt:main',
        ],
    },
)