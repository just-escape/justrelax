from setuptools import setup


def get_requirements():
    with open("requirements.txt") as fh:
        return fh.readlines()


if __name__ == '__main__':
    setup(
        name="justrelax_node_emergency_exit",
        version="0.1",
        packages=["justrelax.node.emergency_exit"],
        scripts=["scripts/start-node-emergency-exit"],
        install_requires=get_requirements(),
        zip_safe=False,
    )
