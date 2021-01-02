import setuptools

setuptools.setup(
    name="azsctl",
    version="1.0",
    packages=setuptools.find_packages(),
    scripts=['azsctl.completion.sh'],
    entry_points={"console_scripts": ["azsctl=azsctl.__main__:main"]},
    author="Frode Hus",
    author_email="frode.hus@outlook.com",
    description="Simple tool that lets you control Azure Sentinel",
    url="https://www.frodehus.dev",
    python_requires=">=3.6",
    install_requires=["requests", "knack", "msal", "alive_progress", "pyinquirer"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)