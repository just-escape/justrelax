from setuptools import setup


def get_requirements():
    with open("requirements.txt") as fh:
        return fh.readlines()


if __name__ == '__main__':
    setup(
        name="justrelax_node_decoration_belt_rotary",
        version="0.1",
        packages=["justrelax.node.decoration_belt_rotary", "twisted.plugins"],
        install_requires=get_requirements(),
        zip_safe=False,
    )
