def subgen():
    message = yield
    print('Subgen received:', message)


def coroutine(func):

    def inner(*args, **kwargs):
        g = func(*args, **kwargs)
        g.send(None)
        return g

    return inner
