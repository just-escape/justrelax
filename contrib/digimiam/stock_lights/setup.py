from setuptools import setup


def get_requirements():
    with open("requirements.txt") as fh:
        return fh.readlines()


if __name__ == '__main__':
    setup(
        name="justrelax_node_stock_lights",
        version="0.1",
        packages=["justrelax.node.stock_lights"],
        scripts=["scripts/start-stock-lights"],
        install_requires=get_requirements(),
        zip_safe=False,
    )
