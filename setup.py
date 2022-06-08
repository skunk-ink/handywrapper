from setuptools import setup

setup(
    name='handywrapper',
    version='1.0.6',    
    description='A Python wrapper for the Handshake API',
    url='https://github.com/skunk-ink/handywrapper',
    download_url='https://github.com/skunk-ink/handywrapper/archive/refs/tags/v1.0.6.tar.gz',
    keywords=['handywrapper'],
    author='skunk-ink',
    author_email='murray.crawford85@gmail.com',
    license='MIT',
    packages=['handywrapper'],
    install_requires=['requests>=2.22.0'],

    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
