import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bui",
    version="0.3.3",
    author="Vincent Le Goff",
    author_email="vincent.legoff.srs@gmail.com",
    description="The Blind User Interface: the interface you can design with your eyes closed.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vincent-lg/bui/",
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires = [
        'Logbook == 1.5.2',
        'wxPython == 4.2.0; platform_system=="Windows"',
        'Pypubsub == 4.0.3; platform_system=="Windows"',
    ],
    extras_require={
        'demo':  [
            "aiodns==2.0.0", "aiofiles==0.4.0",
            "aiohttp==3.5.4", "cchardet==2.1.4",
        ],
    },
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)