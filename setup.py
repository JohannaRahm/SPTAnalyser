# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 11:02:56 2019

@author: Johanna Rahm

Research group Heilemann
Institute for Physical and Theoretical Chemistry, Goethe University Frankfurt a.M.
"""

import setuptools 

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(name = "pySPT",
                 version = "19.03",
                 author = "Johanna Rahm and Sebastian Malkusch",
                 author_email = "johanna.rahm@stud.uni-frankfurt.de",
                 description = "a package for analysing SPT data",
                 long_description = long_description,
                 long_description_content_type = "text/markdown",
                 #licence_file = "LICENSE", how to get license?? 
                 url="https://github.com/JohannaRahm/pySPT",
                 packages = setuptools.find_packages(),
                 install_requires=["numpy",
                                   "matplotlib",
                                   "scipy",
                                   "h5py",
                                   "tqdm",
                                   "ipywidgets",
                                   "IPython",
                                   "hide_code",
                                   "tornado==5.1",
                                   "pandas"],
                   classifiers = ["Programming Language :: Python :: 3",
                                  "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",  # "License :: OSI Approved :: GPL-3.0 License",
                                  "Operating System :: OS Independent",],)