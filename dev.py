#!/usr/bin/env python

import os
import click
from executor import execute


def python_source_files():
    import glob

    result = (glob.glob("*.py") + glob.glob("hobart/*.py"))
    result.remove("hobart/__init__.py")
    return result


@click.group()
def cli():
    pass


@cli.command()
def init():
    execute("pip3 install -r requirements_dev_py3.txt")


@cli.command()
def test():
    execute("nose2")


@cli.command()
def lint():
    execute("pyflakes", *python_source_files())


@cli.command()
def black():
    execute("black", *python_source_files())


@cli.command()
def black_check():
    execute("black", "--check", *python_source_files())


@cli.command()
def upload():
    execute("rm -rf dist/")
    execute("python setup.py sdist")
    execute("twine upload dist/*")


if __name__ == "__main__":
    os.chdir(os.path.abspath(os.path.dirname(__file__)))
    cli()
