class Bunch(object):
    """Convert a dictionary to a class."""
    def __init__(self, adict):
        self.__dict__.update(adict)


def static_vars(**kwargs):
    """Enable static variables for functions persistent over several calls."""
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate


def flatten(container):
    """Flatten a nested list."""
    for i in container:
        if isinstance(i, (list, tuple)):
            for j in flatten(i):
                yield j
        else:
            yield i


def unflatten(flat_list, skeleton):
    """Recreate a nested list from a flattened list."""
    it = iter(flat_list)

    def rec(skel):
        result = []
        for cursk in skel:
            if isinstance(cursk, int):
                for i in range(cursk):
                    result.append(next(it))
            else:
                result.append(rec(cursk))
        return result

    result = rec(skeleton)
    # check if all elements traversed
    try:
        next(it)
        raise IndexError
    except StopIteration:
        return result
