def ensure_iterable(x):
    """
    The name is a bit fallacious because it does not really ensure that x is
    iterable but it does the trick for this project's needs
    """
    return x if isinstance(x, (list, tuple)) else (x,)
