"""
Programme qui convertit une matrice de tile en une matrice de bytes

Auteur: Adrien Buschbeck, Albert Stanislawek
"""

from itertools import product

def convertisseur(matrix: list[list[tuple[int, int, int]]]) -> bytes:
    """
    Convertit une matrice de tile en une matrice de bytes
    Au vu du fait que Adrien est en train de faire le typage, j'ai mis le truc du haut au lieu de Matrix car y a des
    bugs dans son trc
    """

    dim_x = len(matrix)
    dim_y = len(matrix[0])

    bytestr: bytes = b""
    for y in range(dim_y):
        for x in range(dim_x):
            cell = matrix[y][x] + (255,)
            bb = b""
            for i in cell:
                bbb = i.to_bytes(length=1, byteorder="big")
                bb += bbb
            bytestr += bb
    return bytestr


def convertisseur_tryhard(matrix: list[list[tuple[int, int, int]]]) -> bytes:
    """
    One-liner de TRTRTRTRTR- TRYHAAAAAAARD
    """

    return b"".join(
        [b"".join([i.to_bytes(length=1, byteorder="big") for i in matrix[y][x] + (255,)])
         for x, y in product(range(len(matrix)), range(len(matrix[0])))]
    )



if __name__ == "__main__":
    m = [
        [(5, 6, 7), (5, 6, 7)],
        [(5, 6, 7), (5, 6, 7)],
    ]

    print(convertisseur_tryhard(m))
