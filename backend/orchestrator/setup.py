from setuptools import setup


def get_requirements():
    with open("requirements.txt") as fh:
        return fh.readlines()


if __name__ == '__main__':
    setup(
        name="justrelax_orchestrator",
        version="0.1",
        packages=["justrelax.orchestrator", "twisted.plugins"],
        install_requires=get_requirements(),
        zip_safe=False,
    )

    try:
        from twisted.plugin import IPlugin, getPlugins  # NOQA: E402
    except ImportError:
        pass
    else:
        list(getPlugins(IPlugin))
