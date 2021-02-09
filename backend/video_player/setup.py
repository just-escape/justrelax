from setuptools import setup


def get_requirements():
    with open("requirements.txt") as fh:
        return fh.readlines()


if __name__ == '__main__':
    setup(
        name="justrelax_node_video_player",
        version="0.1",
        packages=["justrelax.node.video_player"],
        scripts=["scripts/start-node-video-player"],
        install_requires=get_requirements(),
        zip_safe=False,
    )
