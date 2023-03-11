import os

from recompose import *
from split import *
from os import urandom

PARAMS = [
    (2, 1),
    (10, 10),
    (10, 9)
]

def test_chunk_null():
    chunk = int.from_bytes(b"\x00"*255, 'little', signed=False)
    for n, m in PARAMS:
        points, p = split_chunk(chunk, m, n)
        assert recover_chunk(points[:m], p) == chunk

def test_chunk_last():
    chunk = int.from_bytes(b"\xff"*255, 'little', signed=False)
    for n, m in PARAMS:
        points, p = split_chunk(chunk, m, n)
        assert recover_chunk(points[:m], p) == chunk

def test_chunk_random():
    for i in range(10):
        chunk = int.from_bytes(urandom(255), 'little', signed=False)
        for n, m in PARAMS:
            points, p = split_chunk(chunk, m, n)
            assert recover_chunk(points[:m], p) == chunk

def test_secret_null():
    with open("test.tmp", "wb") as fisier:
        fisier.write(b"\x00"*1024)

    for n, m in PARAMS:
        split_file("test.tmp", n, m)
        shares = [f"file{i+1}.secret" for i in range(n)]
        recover_file(shares[:m])
        assert open("test.tmp", 'rb').read() == open("test.tmp.recovered", 'rb').read()

        os.unlink("test.tmp.recovered")
        for share in shares:
            os.unlink(share)

    os.unlink("test.tmp")


def test_secret_last():
    with open("test.tmp", "wb") as fisier:
        fisier.write(b"\xff" * 1024)

    for n, m in PARAMS:
        split_file("test.tmp", n, m)
        shares = [f"file{i + 1}.secret" for i in range(n)]
        recover_file(shares[:m])
        assert open("test.tmp", 'rb').read() == open("test.tmp.recovered", 'rb').read()

        os.unlink("test.tmp.recovered")
        for share in shares:
            os.unlink(share)

    os.unlink("test.tmp")


def test_secret_random():
    for i in range(10):

        with open("test.tmp", "wb") as fisier:
            fisier.write(urandom(1024))

        for n, m in PARAMS:
            split_file("test.tmp", n, m)
            shares = [f"file{i + 1}.secret" for i in range(n)]
            recover_file(shares[:m])
            assert open("test.tmp", 'rb').read() == open("test.tmp.recovered", 'rb').read()

            os.unlink("test.tmp.recovered")
            for share in shares:
                os.unlink(share)

        os.unlink("test.tmp")