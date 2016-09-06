try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'version': '1.0.0',
    'description': 'YAML Bulk Edit',
    'author': 'Alex Harvey',
    'author_email': 'alexharv074@gmail.com',
    'license': 'MIT',
    'url': 'https://github.com/alexharv074/yaml-bulk-edit.git',
    'download_url': 'https://github.com/alexharv074/yaml-bulk-edit.git',
    'install_requires': ['nose', 'ruamel.yaml>=0.12.7'],
    'packages': ['yaml-bulk-edit'],
    'scripts': [],
    'name': 'YAML Bulk Edit'
}

setup(**config)
