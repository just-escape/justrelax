import os
import requests
from importlib import import_module

from justrelax.common.logging import logger


def ensure_iterable(x):
    """
    The name is a bit fallacious because it does not really ensure that x is
    iterable but it does the trick for this project's needs
    """
    return x if isinstance(x, (list, tuple)) else (x,)


def abs_path_if_not_abs(path, folder_path):
    if os.path.isabs(path):
        return path

    return os.path.normpath(os.path.join(folder_path, path))


def import_string(path):
    """
    Import a dotted module path and return the attribute/class designated by the
    last name in the path. Raise ImportError if the import failed.

    Django's implementation
    """
    try:
        module_path, class_name = path.rsplit('.', 1)
    except ValueError as err:
        raise ImportError("'{}' is not a module path".format(path)) from err

    module = import_module(module_path)

    try:
        return getattr(module, class_name)
    except AttributeError as err:
        raise ImportError("'{}' not found in '{}'".format(
            class_name, module)) from err


def human_readable_size(num, suffix='B'):
    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(num) < 1024.0:
            return "{:3.1f} {}{}".format(num, unit, suffix)
        num /= 1024.0
    return "{:.1f} {}{}".format(num, 'Y', suffix)


def download_file(url, path):
    logger.info("Downloading file at {}".format(url))
    response = requests.get(url)
    if response.status_code != 200:
        logger.error("Error downloading file ({} - {}): skipping".format(
            response.status_code, response.text))
        return False

    with open(path, 'w+') as f:
        f.write(response.text)

    return True
