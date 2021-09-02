# -*- coding: utf-8 -*-
from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from codecs import open  # To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='''ckanext-bpatogalaxy''',
    version='0.0.1',
    description='''BPA to Galaxy extension''',
    long_description=long_description,
    url='https://github.com/BioplatformsAustralia/ckanext-bpatogalaxy',
    author='Bioplatforms Australia',
    author_email='help@bioplatforms.com',
    license='GPL3',
    keywords='''CKAN Galaxy galaxy''',
    packages=['ckanext.bpatogalaxy'],
    namespace_packages=['ckanext'],
    include_package_data=True,
    package_dir={'ckanext.bpatogalaxy': 'ckanext/bpatogalaxy'},
    package_data={'ckanext.bpatogalaxy': ['*.json', 'templates/*.html', 'templates/*/*.html', 'templates/*/*/*.html', 'static/*.css', 'static/*.png', 'static/*.jpg', 'static/*.css', 'static/*.ico']},
    entry_points='''
        [ckan.plugins]
        bpatogalaxy=ckanext.bpatogalaxy.plugin:BpatogalaxyPlugin
    ''',
    
    # ########################################
    # TODO remove entries that are not needed 
    # ########################################

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        # 3 - Alpha
        # 4 - Beta
        # 5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
    ],
    install_requires=[
      # CKAN extensions should not list dependencies here, but in a separate
      # ``requirements.txt`` file.
      #
      # http://docs.ckan.org/en/latest/extensions/best-practices.html#add-third-party-libraries-to-requirements-txt
    ],
    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages.
    # see http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    data_files=[],
    # If you are changing from the default layout of your extension, you may
    # have to change the message extractors, you can read more about babel
    # message extraction at
    # http://babel.pocoo.org/docs/messages/#extraction-method-mapping-and-configuration
    message_extractors={
        'ckanext': [
            ('**.py', 'python', None),
            ('**.js', 'javascript', None),
            ('**/templates/**.html', 'ckan', None),
        ],
    }
)
