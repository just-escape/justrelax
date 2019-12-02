from setuptools import setup, find_packages


def get_requirements():
    with open("requirements.txt") as fh:
        return fh.readlines()


if __name__ == '__main__':
    setup(
        name="justrelax_node_jukebox",
        version="0.1",
        packages=find_packages(),
        scripts=[],
        install_requires=get_requirements(),
    )
