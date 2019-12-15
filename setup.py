from setuptools import setup

setup(
    name='beancount-coinmarketcap',
    version='1.0',
    description='Coinmarketcap price source for Beancount',
    packages=['price_sources'],
    license='MIT',
    install_requires=['requests', 'beautifulsoup4'],
)
