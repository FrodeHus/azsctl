import setuptools

setuptools.setup(
    name="azsctl",
    version="0.2.5",
    packages=setuptools.find_packages(),
    scripts=['azsctl','azsctl.completion.sh'],
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
