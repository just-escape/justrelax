import os
import sys
from setuptools import setup


def get_requirements():
    with open("requirements.txt") as fh:
        return fh.readlines()


if __name__ == '__main__':
    sys.path.append(os.path.expanduser(os.path.dirname(__file__)))

    setup(
        name="justrelax_node",
        version="0.1",
        packages=["justrelax.node", "twisted.plugins"],
        scripts=[],
        install_requires=get_requirements(),
    )

    try:
        from twisted.plugin import IPlugin, getPlugins  # NOQA: E402
    except ImportError:
        pass
    else:
        list(getPlugins(IPlugin))
