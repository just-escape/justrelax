from setuptools import setup


def get_requirements():
    with open("requirements.txt") as fh:
        return fh.readlines()


if __name__ == '__main__':
    setup(
        name="justrelax_node_human_authenticator",
        version="0.1",
        packages=["justrelax.node.human_authenticator"],
        scripts=["scripts/start-node-human-authenticator"],
        install_requires=get_requirements(),
        zip_safe=False,
    )
