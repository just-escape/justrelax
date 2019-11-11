

def get_arg(request, name):
    encoded_name = name.encode('utf8')
    arg = request.args.get(encoded_name, None)
    if arg is None:
        return arg
    return arg[0].decode('utf8')
