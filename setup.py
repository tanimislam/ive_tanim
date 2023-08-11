import os, sys
from setuptools import setup, find_packages
#
## requirements are in "requirements.txt"
reqs = sorted(set(map(lambda line: line.strip(),
                      filter(lambda line: len( line.strip( ) ) != 0,
                             open( 'requirements.txt', 'r').readlines()))))

setup(
    name = 'ive_tanim',
    version = '1.5',
    #
    ## following advice on find_packages excluding tests from https://setuptools.readthedocs.io/en/latest/setuptools.html#using-find-packages
    packages = find_packages( exclude = ["*.tests", "*.tests.*", "tests" ] ),
    url = 'https://github.com/tanimislam/ive_tanim',
    license = 'BSD-2-Clause',
    author = 'Tanim Islam',
    author_email = 'tanim.islam@gmail.com',
    description = 'Image-video-email low level functionality from Tanim, initially for Tanim.',
    #
    ## classification: where in package space does "ive_tanim live"?
    ## follow (poorly) advice I infer from https://blog.ionelmc.ro/2014/05/25/python-packaging/#the-setup-script
    classifiers=[
    # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
      'Development Status :: 5 - Production/Stable',
      'Intended Audience :: End Users/Desktop',
      'License :: OSI Approved :: BSD License',
      'Operating System :: POSIX',
      'Environment :: Console',
      'Programming Language :: Python :: 3',
    # uncomment if you test on these interpreters:
    # 'Programming Language :: Python :: Implementation :: IronPython',
    # 'Programming Language :: Python :: Implementation :: Jython',
    # 'Programming Language :: Python :: Implementation :: Stackless',
        'Topic :: Utilities',
    ],
    #
    ## requirements
    install_requires = reqs,
    python_requires = '>=3.7',
    #
    ## the executables I am creating
    entry_points = {
        'console_scripts' : [
            #
            ## CLI stuff
            "github_md_2_html = ive_tanim.cli.github_md_2_html:_main",
            "autoCropImage = ive_tanim.cli.autoCropImage:_main",
            "convertImage = ive_tanim.cli.convertImage:_main",
            "gitZipArchive = ive_tanim.cli.gitZipArchive:main",
            "imageFromURL = ive_tanim.cli.imageFromURL:_main",
            "inline_images = ive_tanim.cli.inline_images:_main",
            "myrst2html = ive_tanim.cli.myrst2html:_main",
            "simple_email = ive_tanim.cli.simple_email:_main",
            "simple_email_config = ive_tanim.cli.simple_email_config:main",
        ]
    },
    #
    ## big fatass WTF because setuptools is unclear about whether I can give a directory that can then be resolved by
    ## other resources
    ## here is the link to the terrible undocumented documentation: https://setuptools.readthedocs.io/en/latest/setuptools.html#including-data-files
    package_data = {
        "ive_tanim" : [
            "resources/*.json",
            ],
    }
)
