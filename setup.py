from setuptools import setup

setup(
    name='handywrapper',
    version='2.0.0',
    description='A Python wrapper for the Handshake API',
    url='https://github.com/skunk-ink/handywrapper',
    download_url='https://github.com/skunk-ink/handywrapper/archive/refs/tags/v2.0.0.tar.gz',
    keywords=['handywrapper'],
    author='skunk-ink',
    author_email='murray.crawford85@gmail.com',
    license='MIT',
    packages=['handywrapper'],
    install_requires=['requests>=2.22.0'],
    python_requires='>=3.6',
    extras_require={
        'test': ['pytest', 'responses>=0.23'],
    },

    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)
