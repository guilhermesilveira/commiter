
def to_int(params):
    return [int(p) for p in params]


def to_parts(args):
    parts = [to_int(arg.split(":")) for arg in args]
    return parts
