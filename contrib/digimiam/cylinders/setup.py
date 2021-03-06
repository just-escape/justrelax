from setuptools import setup


def get_requirements():
    with open("requirements.txt") as fh:
        return fh.readlines()


if __name__ == '__main__':
    setup(
        name="justrelax_node_cylinders",
        version="0.1",
        packages=["justrelax.node.cylinders"],
        scripts=["scripts/start-node-cylinders"],
        install_requires=get_requirements(),
        zip_safe=False,
    )
