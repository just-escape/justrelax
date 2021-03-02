from setuptools import setup


def get_requirements():
    with open("requirements.txt") as fh:
        return fh.readlines()


if __name__ == '__main__':
    setup(
        name="justrelax_node_waffle_factory",
        version="0.1",
        packages=["justrelax.node.waffle_factory"],
        scripts=["scripts/start-node-waffle-factory"],
        install_requires=get_requirements(),
        zip_safe=False,
    )
