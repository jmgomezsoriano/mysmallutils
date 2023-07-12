import glob
from shutil import rmtree

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


class CleanCommand(setuptools.Command):
    """ Custom clean command to tidy up the project root. """
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        rmtree('build', ignore_errors=True)
        rmtree('dist', ignore_errors=True)
        for file in glob.glob('*.egg-info'):
            rmtree(file)


setuptools.setup(
    cmdclass={'clean': CleanCommand},
    name='mysmallutils',
    version='2.0.12',
    url='https://github.com/jmgomezsoriano/mysmallutils',
    license='LGPL2',
    author='José Manuel Gómez Soriano',
    author_email='jmgomez.soriano@gmail.com',
    long_description=long_description,
    long_description_content_type='text/markdown',
    description='Small Python utils to do life easier.',
    packages=setuptools.find_packages(exclude=["test"]),
    package_dir={'mysutils': 'mysutils'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7,<4'
)
