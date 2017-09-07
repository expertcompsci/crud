# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 13:06:03 2017

@author: ben.lester
"""

from setuptools import setup

setup(
    name='aip_app',
    packages=['aip_app'],
    include_package_data=True,
    install_requires=[
        'flask'
    ],
)