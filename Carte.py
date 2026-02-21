"""
Programme créant une carte

Auteur: Adrien Buschbeck
"""

import random as ran
import matrix_manager as mm
from grid_world import Tile
from collections import Counter

def w_f_c_simplified(matrix):
    """Retourne une matrix générée avec un wfc simplifié

    Les éléments de la matrix doivent être des listes
    """
    
    coordinates = [(i, j) for j in range(len(matrix[len(matrix) - 1])) for i in range(len(matrix))]
    test_value = len(matrix)*len(matrix[len(matrix) - 1])
    
    while test_value != 0:
        cell = mm.random_cell(matrix, coordinates)
        coordinates.remove((cell[0][0], cell[0][1]))
        if len(cell[1]) == 0:
            print("Contradiction atteinte")
            break
        #mettre respect condition ici
        c_cell = Counter(cell[1])
        list_cell = list(c_cell.elements())
        matrix[cell[0][0]][cell[0][1]] = ran.choice(list_cell)
        test_value -= 1
    return matrix


def condition():
    pass



if __name__ == "__main__":
    Plain = Tile("Plain", 1, 1, (124, 252, 0), {"Sea": 0,})
    Mountain = Tile("Mountain", 0.25, 10, (139, 137, 137), {"Sea": 0,})
    Forest = Tile("Forest", 1.25, 5, (34, 139, 34), {"Sea": 0, "Desert" : 0})
    Sea = Tile("Sea", 0, 10000, (28, 107, 160), {"Plain": 0, "Mountain" : 0, "Forest" : 0, "Desert" : 0})
    River = Tile("River", 0, 3, (70, 130, 180), {})
    Desert = Tile("Desert", 0.1, 0.5, (237, 201, 175), {"Sea": 0, "Forest" : 0})
    a = w_f_c_simplified(mm.create_matrix((10, 10), {"P":100, "M":1, "F":1, "D":1, "S":1, "R":1})) #{Plain:1, Mountain:1, Forest:1, Desert:1, Sea:1, River:1}
    print('\n'.join([str(i) for i in a]))