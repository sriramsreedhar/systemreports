import setuptools
with open("README.rst", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='sysreports',  
     version='1.0',
     scripts=['sysreports'] ,
     author="Sriram Sreedhar",
     author_email="sriramsreedhar003@gmail.com",
     description="Generates Detailed System Report",
     long_description=long_description,
     long_description_content_type="text/markdown",
     install_requires=[
        "os",
        'shutil',
        'datetime',
        'sysconfig',
        'platform',
        'psutil',
    ],
     url="https://github.com/sriramsreedhar/systemreports.git",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 2.7",
         "License :: OSI Approved :: BSD License",
         "Operating System :: OS Independent",
     ],
 )
