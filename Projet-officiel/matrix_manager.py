"""
Gère plusieurs opérations sur des matrcies

Auteur: Adrien Buschbeck, Albert Stanislawek
"""

from collections import Counter
import random as ran
from typing import cast
from math import inf

type Position = tuple[int, int]
type Matrix[T] = list[list[T]]


def create_matrix[T](dim: tuple[int, int], element: T = 0) -> Matrix[T]:
    """
    Retourne une matrice où chaque cellule est remplie par element
    dim[0] --> axe -y
    dim[1] --> axe x
    """
    return [[element for _ in range(dim[1])] for _ in range(dim[0])]


def set[T](matrix: Matrix[T], element: T, position: Position) -> Matrix[T]:
    """
    Donne une valeur à une cellule d'une matrice
    position[0] --> axe -y
    position[1] --> axe x
    """
    matrix[position[0]][position[1]] = element
    return matrix


def get[T](matrix: Matrix[T], position: Position) -> T:
    """
    Retourne une valeur d'une cellule d'une matrice
    position[0] --> axe -y
    position[1] --> axe x
    """
    return matrix[position[0]][position[1]]


def up[T](matrix: Matrix[T], position: Position) -> tuple[Position, T] | None:
    """
    Retourne la position et la valeur d'une cellule en haut d'une cellule
    position[0] --> axe -y
    position[1] --> axe x
    """
    if position[0] == 0:
        return None
    return (
        (position[0] - 1, position[1]),
        matrix[position[0] - 1][position[1]],
    )


def down[T](
    matrix: Matrix[T], position: Position
) -> tuple[Position, T] | None:
    """
    Retourne la position et la valeur d'une cellule en bas d'une cellule
    position[0] --> axe -y
    position[1] --> axe x
    """
    if position[0] >= len(matrix) - 1:
        return None
    return (
        (position[0] + 1, position[1]),
        matrix[position[0] + 1][position[1]],
    )


def right[T](
    matrix: Matrix[T], position: Position
) -> tuple[Position, T] | None:
    """
    Retourne la position et la valeur d'une cellule à droite d'une cellule
    position[0] --> axe -y
    position[1] --> axe x
    """
    if position[1] == len(matrix[position[0]]) - 1:
        return None
    return (
        (position[0], position[1] + 1),
        matrix[position[0]][position[1] + 1],
    )


def left[T](
    matrix: Matrix[T], position: Position
) -> tuple[Position, T] | None:
    """
    Retourne la position et la valeur d'une cellule à gauche d'une cellule
    position[0] --> axe -y
    position[1] --> axe x
    """
    if position[1] == 0:
        return None
    return (
        (position[0], position[1] - 1),
        matrix[position[0]][position[1] - 1],
    )


def random_cell[T](
    matrix: Matrix[T], coordinate: list[Position] | None = None
) -> tuple[Position, T]:
    """
    Retourne la valeur et la position aléatoire
    d'une cellule cellule aléatoire d'une matrice
    parmi une série de coordonnées

    coordinate[0] --> axe -y
    coordinate[1] --> axe x
    """
    coords = [
        (i, j)
        for j in range(len(matrix[len(matrix) - 1]))
        for i in range(len(matrix))
    ]

    def ran_cell(
        matrix: Matrix[T], coordinates: list[Position] = coords
    ) -> tuple[Position, T]:
        position = ran.choice(coordinates)
        column = position[0]
        row = position[1]
        cell = matrix[column][row]
        return ((column, row), cell)

    if coordinate is None:
        return ran_cell(matrix)
    else:
        return ran_cell(matrix, coordinate)


def lobject_cell[T](
    matrix: Matrix[T | dict[T, int]], coordinate: list[Position] | None = None
) -> tuple[Position, dict[T, int]]:
    """
    Retourne la valeur et la position aléatoire
    de la cellule avec le moins d'éléments dans la matrice

    coordinate[0] --> axe -y
    coordinate[1] --> axe x
    """

    if coordinate is None:
        coordinate = [
            (i, j)
            for j in range(len(matrix[len(matrix) - 1]))
            for i in range(len(matrix))
        ]

    cell_min: list[tuple[Position, dict[T, int]]] = []
    valmin = inf
    for c in coordinate:
        column = c[0]
        row = c[1]
        cell = get(matrix, (column, row))
        if isinstance(cell, dict):

            cell = cast(dict[T, int], cell)

            lencell = len(cell)

            if lencell == valmin:
                cell_min.append(((column, row), cell))

            elif lencell < valmin:
                valmin = lencell
                cell_min = [((column, row), cell)]

    return ran.choice(cell_min)


def matrix_change[T](
    matrix: Matrix[T], coordinate: list[Position], dict_val: dict[T, int]
) -> Matrix[T]:
    """
    Donne une valeur parmi une liste de valeur
    à une matrice sur une série de coordonnées
    """
    for i in coordinate:
        matrix[i[0]][i[1]] = ran.choice(list(Counter(dict_val).elements()))
    return matrix


def fill[T](matrix: Matrix[T], position_cell: Position) -> Matrix[T]:
    """
    Regarde si une cellule est entourée de cellule de la même valeur
    le cas échéant, donne la même valeur à la cellule
    Ne marche pas avec une matrice 1X1
    """
    test_value = True

    if up(matrix, position_cell) is None:
        print(down(matrix, position_cell))
        value_desired = cast(tuple[Position, T], down(matrix, position_cell))[
            1
        ]
    else:
        value_desired = cast(tuple[Position, T], up(matrix, position_cell))[1]

    for i in range(4):
        match i:
            case 0:
                func = up
            case 1:
                func = down
            case 2:
                func = right
            case 3:
                func = left
            case _:
                raise ValueError("the number must stay 4")
        cell = func(matrix, position_cell)
        if cell is not None:
            if cell[1] != value_desired:
                test_value = False
    if test_value:
        matrix[position_cell[0]][position_cell[1]] = value_desired
    return matrix


def random_walk[T](
    matrix: Matrix[T],
    starting_pos: list[Position],
    steps: int,
    max_lenght: int,
    value: T,
):
    """
    Réalise l'algorythme de random walk
    """
    for p in starting_pos:
        actual_position = p
        for _ in range(steps):
            direction = ran.randint(0, 3)
            match direction:
                case 0:
                    func = up
                case 1:
                    func = down
                case 2:
                    func = right
                case 3:
                    func = left
                case _:
                    raise ValueError("the number must stay between 0 and 3")

            lenght = ran.randint(0, max_lenght)
            for _ in range(lenght):
                cell_test = func(matrix, actual_position)
                if cell_test is not None:
                    actual_position = cell_test[0]
                matrix[actual_position[0]][actual_position[1]] = value
    return matrix


def in_concact[T](
    matrix: Matrix[T],
    position_cell: Position,
    value_desired: T,
    except_value: T,
) -> bool:
    """
    Regarde si une cellule est en contact
    d'une cellule d'une certaine valeur
    sauf si la valeur de la cellue est except_value
    """
    test_value = False

    for i in range(4):
        match i:
            case 0:
                func = up
            case 1:
                func = down
            case 2:
                func = right
            case 3:
                func = left
            case _:
                raise ValueError("the number must stay 4")
        cell_test = func(matrix, position_cell)
        if cell_test is not None:
            if cell_test[1] == value_desired:
                if get(matrix, position_cell) != except_value:
                    test_value = True
                    break

    return test_value


def test():
    matrix_test = create_matrix((10, 10), "0")

    matrix_test[1][0] = "left"
    matrix_test[1][2] = "right"
    matrix_test[0][1] = "up"
    matrix_test[2][1] = "down"
    # test in map
    assert cast(tuple[Position, object], up(matrix_test, (1, 1)))[1] == "up"
    assert (
        cast(tuple[Position, object], down(matrix_test, (1, 1)))[1] == "down"
    )
    assert (
        cast(tuple[Position, object], left(matrix_test, (1, 1)))[1] == "left"
    )
    assert (
        cast(tuple[Position, object], right(matrix_test, (1, 1)))[1] == "right"
    )
    # test hors map
    assert up(matrix_test, (0, 2)) is None
    assert down(matrix_test, (9, 2)) is None
    assert left(matrix_test, (5, 0)) is None
    assert right(matrix_test, (9, 9)) is None
    print("tous les tests sont passés")


if __name__ == "__main__":
    test()
