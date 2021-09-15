from time import time


def gen(s):
    for i in s:
        yield i


def gen_filename():
    while True:
        pattern = 'file-{}.jpeg'
        t = int(time() * 1000)
        yield pattern.format(str(t))
