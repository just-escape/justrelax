from setuptools import setup


def get_requirements():
    with open("requirements.txt") as fh:
        return fh.readlines()


if __name__ == '__main__':
    setup(
        name="justrelax_node_music_player",
        version="0.1",
        packages=["justrelax.node.music_player"],
        scripts=["scripts/start-node-music-player"],
        install_requires=get_requirements(),
        zip_safe=False,
    )
