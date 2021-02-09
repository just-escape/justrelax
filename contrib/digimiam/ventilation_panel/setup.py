from setuptools import setup


def get_requirements():
    with open("requirements.txt") as fh:
        return fh.readlines()


if __name__ == '__main__':
    setup(
        name="justrelax_node_ventilation_panel",
        version="0.1",
        packages=["justrelax.node.ventilation_panel"],
        scripts=["scripts/start-node-ventilation-panel"],
        install_requires=get_requirements(),
        zip_safe=False,
    )
