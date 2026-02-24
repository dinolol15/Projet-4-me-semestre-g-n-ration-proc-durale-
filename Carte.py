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
        
        matrix[cell[0][0]][cell[0][1]] = ran.choice(list(Counter(cell[1]).elements()))
        condition(matrix, ((cell[0][0], cell[0][1]), matrix[cell[0][0]][cell[0][1]]))
        test_value -= 1
    
            
    return matrix


def condition(matrix, cell):
    """Enlève les possibilitées impossibles

    position[0] : axe -y
    position[1] : axe x
    """
    position = (cell[0][0], cell[0][1])
    cell = matrix[position[0]][position[1]]
    for i in range(4):
        if i == 0:
            cell1 = mm.up(matrix, position)
        elif i == 1:
            cell1 = mm.down(matrix, position)
        elif i == 2:
            cell1 = mm.right(matrix, position)
        elif i == 3:
            cell1 = mm.left(matrix, position)
        
        try:
            list(Counter(cell1[1]))
        except TypeError:
            continue
        
        matrix[cell1[0][0]][cell1[0][1]] = {tile: count for tile, count in cell1[1].items() if tile.Name not in cell.wfc_coeficient}
            
            
            


if __name__ == "__main__":
    #Base est pour que le tuple en soit vraiment u et pas un str
    Plain = Tile("Plain", 1, 1, (124, 252, 0), ("Sea", "Base"))
    Mountain = Tile("Mountain", 0.25, 10, (139, 137, 137), ("Sea", "Base"))
    Forest = Tile("Forest", 1.25, 5, (34, 139, 34), ("Sea", "Desert"))
    Sea = Tile("Sea", 0, 10000, (28, 107, 160), ("Plain", "Mountain", "Forest", "Desert"))
    River = Tile("River", 0, 3, (70, 130, 180), ())
    Desert = Tile("Desert", 0.1, 0.5, (237, 201, 175), ("Sea", "Forest"))
    
    a = w_f_c_simplified(mm.create_matrix((10, 10), {Plain:3, Mountain:1, Forest:2, Desert:2, Sea:1, River:2})) #{Plain:1, Mountain:1, Forest:1, Desert:1, Sea:1, River:1}
    print('\n'.join([str(i) for i in a]))