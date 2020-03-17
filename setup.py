import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="kurapy",
    version="0.0.1",
    description="Simulation of Kuramoto model in a 2D lattice",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/arckpx/kurapy",
    author="Kun Hee Park",
    author_email="arckp.x@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    packages=["kurapy"],
    install_requires=["numpy"],
)
