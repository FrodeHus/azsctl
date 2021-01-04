import setuptools

setuptools.setup(
    name="azsctl",
    version="0.2.1",
    packages=setuptools.find_packages(),
    scripts=['azsctl.completion.sh'],
    entry_points={"console_scripts": ["azsctl=azsctl.__main__:main"]},
    author="Frode Hus",
    author_email="frode.hus@outlook.com",
    description="Simple tool that lets you work with Azure Sentinel",
    url="https://github.com/frodehus/azsctl",
    python_requires=">=3.6",
    install_requires=["requests", "knack", "msal", "alive_progress", "pyinquirer", "urwid"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
