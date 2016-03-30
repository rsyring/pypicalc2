import os
import os.path as osp

from setuptools import setup

cdir = os.path.abspath(os.path.dirname(__file__))
README = open(osp.join(cdir, 'readme.rst')).read()
CHANGELOG = open(osp.join(cdir, 'changelog.rst')).read()

version_fpath = osp.join(cdir, 'pypicalc', 'version.py')
version_globals = {}
with open(version_fpath) as fo:
    exec(fo.read(), version_globals)


setup(
    name='PyPI Calc 2',
    version=version_globals['VERSION'],
    description='<short description>',
    author='Randy Syring',
    author_email='randy.syring@level12.io',
    url='',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.4',
    ],
    packages=['pypicalc'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # use this for libraries; or
        # use requirements folder/files for apps
    ],
    entry_points='''
        [console_scripts]
        pypicalc = pypicalc.cli:cli_entry
    ''',
)
