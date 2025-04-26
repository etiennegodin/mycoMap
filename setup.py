from setuptools import setup, find_packages

setup(
    name='mycoMap',  # The name of your package
    version='0.1.0',  # A semantic version number
    packages=find_packages(),  # Automatically discover your package(s)
    install_requires=[ 
        
        'pyGbif',
        'pandas',
        'geopandas'
    ],
    author='Etienne Godin',
    author_email='etiennegodin@duck.com',
    description='MycoMap package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/my_package',  # Optional URL for your project
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',  # Choose your license
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)