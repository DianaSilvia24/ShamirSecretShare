from os.path import basename
from Crypto.Util import number

def eval_polynom(coef, _x,p):
    """Rezultatul evaluarii polinomului cu coeficientii coef in x, mod p"""
    x = 1
    y = 0
    for c in coef:
        y += x * c
        x *= _x
    return y % p

def split_chunk(chunk, m, n):
    """Imparte un chunk in n puncte folosind un polinom cu m coeficienti, totul mod p"""

    p = number.getPrime(2048)
    while p <= chunk:
        p = number.getPrime(2048)

    coef = [chunk]
    for i in range(m-1):
        coef.append(number.getRandomRange(1, p))

    points = []
    for x in range(1, n+1):
        y = eval_polynom(coef, x, p)
        points.append((x, y))
    return points, p



def split_file(file_path, n, m):
    """Aplica Shamir secret sharing pe chunk-uri de 255 de bytes din file_path"""

    for i in range(n):
        with open(f"file{i+1}.secret", "w") as share:
            share.write(basename(file_path)+"\n")
            share.write(f"{m}\n")

    with open(file_path, "rb") as reader:
        # citim 255 de bytes ca sa ne asiguram ca exista
        # un numar prim de 2048 de biti mai mare decat reprezentarea numerica
        data = reader.read(255)
        while data:
            points, p = split_chunk(int.from_bytes(data, 'little', signed = False), m, n)
            for (x, y), i in zip(points, range(n)):
                with open(f"file{i+1}.secret", "a") as share:
                    share.write(f"{len(data)};{p};{x};{y}\n")
            data=reader.read(255)
