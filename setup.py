from setuptools import find_packages, setup

version_info = {}
exec(open("hobart_svg/package_version.py").read(), version_info)


def load(filename):
    return open(filename, "rb").read().decode("utf-8")


setup(
    name="hobart-svg",
    version=version_info["__version__"],
    description="Render polygons, polylines, and mesh cross sections to SVG",
    long_description=load("README.md"),
    long_description_content_type="text/markdown",
    author="Metabolize",
    author_email="github@paulmelnikow.com",
    url="https://github.com/lace/hobart-svg",
    packages=find_packages(),
    python_requires=">=3.6, <3.9",
    install_requires=load("requirements.txt"),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Other Audience",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Artistic Software",
        "Topic :: Multimedia :: Graphics :: 3D Modeling",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
)
