import os
from setuptools import setup, find_packages


def read(f_name):
    return open(os.path.join(os.path.dirname(__file__), f_name)).read()


setup(
    name='nwg-wrapper',
    version='0.0.2',
    description='Wrapper to display script output or text file content on desktop in wlroots-based compositors',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "": ["config/*"]
    },
    url='https://github.com/nwg-piotr/nwg-wrapper',
    license='MIT',
    author='Piotr Miller',
    author_email='nwg.piotr@gmail.com',
    python_requires='>=3.4.0',
    install_requires=['pygobject'],
    entry_points={
        'gui_scripts': [
            'nwg-wrapper = nwg_wrapper.main:main'
        ]
    }
)
