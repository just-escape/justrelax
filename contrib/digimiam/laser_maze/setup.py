from setuptools import setup


def get_requirements():
    with open("requirements.txt") as fh:
        return fh.readlines()


if __name__ == '__main__':
    setup(
        name="justrelax_node_laser_maze",
        version="0.1",
        packages=["justrelax.node.laser_maze"],
        scripts=["scripts/start-node-laser-maze"],
        install_requires=get_requirements(),
        zip_safe=False,
    )
