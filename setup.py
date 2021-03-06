from setuptools import setup, find_packages

setup(
    name="wanikani-tools",
    version="0.0.1",
    author="Lukasz Kwasek",
    author_email="lukasz@kwasek.co.uk",
    description="A set of small tools to improve your japanese learning",
    url="https://github.com/pamput/wanikani-tools",
    packages=['wanikani-tools'],
    install_requires=[
        'flask',
        'mako',
        'requests'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9.0',
)