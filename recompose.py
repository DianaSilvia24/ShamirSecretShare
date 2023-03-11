def recover_chunk(points, p):
    """Recupereaza un chunk din fisierul original utilizand formula pentru
        interpolarea Lagrange pentru termenul liber"""
    secret = 0
    for x, y in points:
        product = y
        for x_prime, _ in points:
            if x == x_prime:
                continue
            invers = pow(x_prime - x, -1, p)
            product *= (x_prime * invers) % p
        secret = (secret + product) % p

    return secret


def recover_file(shares):
    """ Recupereaza fisierul original pe baza celor minim m fisiere date ca parametru"""
    m = 0
    secret_filename = ""
    shares = [ open(share, "r") for share in shares ]

    for share in shares:
        share_secret_filename = share.readline().strip()
        if secret_filename == "":
            secret_filename = share_secret_filename
        else:
            if secret_filename != share_secret_filename:
                print("Not same file!")
                exit(2)

        share_m = int(share.readline().strip())
        if m == 0:
            m = share_m
        else:
            if m != share_m:
                print("Not same file!")
                exit(2)

    if len(shares) < m:
        print("Not enough shares!")
        exit(2)

    with open(secret_filename+".recovered", "wb") as secret_file:
        finished_processing_chunks = False
        while not finished_processing_chunks:
            points = []
            p = 0
            chunk_size = 0
            for share in shares:
                line = next(share, None)
                if line is None:
                    finished_processing_chunks = True
                    break

                share_chunk_size, share_p, x, y = [ int(i) for i in line.strip().split(";") ]

                if chunk_size == 0:
                    chunk_size = share_chunk_size
                else:
                    if chunk_size != share_chunk_size:
                        print("Not same file")
                        exit(2)

                if p == 0:
                    p = share_p
                else:
                    if p != share_p:
                        print("Not same file")
                        exit(2)

                points.append((x, y))
            else:
                chunk = recover_chunk(points, p)
                secret_file.write(chunk.to_bytes(chunk_size, 'little', signed=False))

    for share in shares:
        share.close()

