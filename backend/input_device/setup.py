from setuptools import setup


def get_requirements():
    with open("requirements.txt") as fh:
        return fh.readlines()


if __name__ == '__main__':
    setup(
        name="justrelax_node_input_device",
        version="0.1",
        packages=["justrelax.node.input_device"],
        scripts=[
            "scripts/start-node-input-device",
            "scripts/start-node-persistent-input-device",
        ],
        install_requires=get_requirements(),
        zip_safe=False,
    )
