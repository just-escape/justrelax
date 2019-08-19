import re


def validate_node_name(n):
    return isinstance(n, str) and validate_one_or_more_alphanumeric(n)


def validate_channel(c):
    return isinstance(c, str) and validate_one_or_more_alphanumeric(c)


def validate_one_or_more_alphanumeric(string):
    return re.search("^\w+$", string)
