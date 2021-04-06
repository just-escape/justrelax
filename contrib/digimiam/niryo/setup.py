from setuptools import setup


if __name__ == '__main__':
    setup(
        name="justrelax_node_niryo",
        version="0.1",
        packages=["justrelax.node.niryo"],
        scripts=["scripts/start-node-niryo"],
        zip_safe=False,
    )
