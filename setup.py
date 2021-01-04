import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wanikani-tools",
    version="0.0.1",
    author="Lukasz Kwasek",
    author_email="lukasz@kwasek.co.uk",
    description="A set of small tools to improve your japanese learning",
    url="https://github.com/pamput/wanikani-tools",
    packages=['flask', 'mako', 'request'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)