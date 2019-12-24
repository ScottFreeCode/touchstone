from setuptools import setup, find_packages

setup(
    name='touchstone',
    version='0.1.0',
    description='End-to-end and exploratory testing made easy.',
    url='https://github.com/shane-jansen/touchstone',
    author='Shane Jansen',
    author_email='shanejjansen@gmail.com',
    license='MIT',
    packages=find_packages(where='/touchstone', exclude='/touchstone/tests'),
    install_requires=['pyfiglet', 'click'],
    entry_points={
        'console_scripts': [
            'touchstone = touchstone.cli:cli'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3'
    ]
)
