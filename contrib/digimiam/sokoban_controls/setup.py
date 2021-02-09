from setuptools import setup


def get_requirements():
    with open("requirements.txt") as fh:
        return fh.readlines()


if __name__ == '__main__':
    setup(
        name="justrelax_node_sokoban_controls",
        version="0.1",
        packages=["justrelax.node.sokoban_controls"],
        scripts=["scripts/start-node-sokoban-controls"],
        install_requires=get_requirements(),
        zip_safe=False,
    )
