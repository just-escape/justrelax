from setuptools import setup


def get_requirements():
    with open("requirements.txt") as fh:
        return fh.readlines()


if __name__ == '__main__':
    setup(
        name="justrelax_node_rotary",
        version="0.1",
        packages=["justrelax.node.rotary"],
        scripts=["scripts/start-node-rotary"],
        install_requires=get_requirements(),
        zip_safe=False,
    )
