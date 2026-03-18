"""
Gère plusieurs opérations sur des matrcies

Auteur: Adrien Buschbeck, Albert ...
"""

from collections import Counter
import itertools as it
import random as ran


def create_matrix(dim: tuple[int, int] | list[int, int], element : object = 0) -> list:
    """retourne une matrice où chaque cellule est remplie par element
    dim[0] --> axe -y
    dim[1] --> axe x
    """
    return [[element for j in range(dim[1])] for i in range(dim[0])]


def up(matrix, position):
    """Retourne la position et la valeur d'une cellule en haut d'une cellule
    position[0] --> axe -y
    position[1] --> axe x
    """
    if position[0] == 0:
        return None 
    return ((position[0] - 1, position[1]) , matrix[position[0] - 1][position[1]])
    

def down(matrix, position):
    """Retourne la position et la valeur d'une cellule en bas d'une cellule
    position[0] --> axe -y
    position[1] --> axe x
    """
    if position[0] >= len(matrix) - 1 :
        return None
    return ((position[0] + 1, position[1]), matrix[position[0] + 1][position[1]])
    
    
def right(matrix, position):
    """"Retourne la position et la valeur d'une cellule à droite d'une cellule
    position[0] --> axe -y
    position[1] --> axe x
    """
    if position[1] == len(matrix[position[0]]) - 1:
        return None 
    return ((position[0], position[1] + 1), matrix[position[0]][position[1] + 1])
    
    
def left(matrix, position):
    """Retourne la position et la valeur d'une cellule à gauche d'une cellule
    position[0] --> axe -y
    position[1] --> axe x
    """
    if position[1] == 0:
        return None
    return ((position[0], position[1] - 1), matrix[position[0]][position[1] - 1])

def random_cell(matrix, coordinate = None):
    """Retourne la valeur et la position aléatoire
        d'une cellule cellule aléatoire d'une matrice
        
        coordinate[0] --> axe -y
        coordinate[1] --> axe x
    """
    coords = [(i, j) for j in range(len(matrix[len(matrix) - 1])) for i in range(len(matrix))]
    
    def ran_cell(matrix, coordinates = coords):
        position = ran.choice(coordinates)
        column = position[0]
        row = position[1]
        cell = matrix[column][row]
        return ((column, row), cell)
    
    if coordinate == None:
        return ran_cell(matrix)
    else:
        return ran_cell(matrix, coordinate)


def lobject_cell(matrix, coordinate = None):
    """Retourne la valeur et la position aléatoire
        de la cellule avec le moins d'éléments dans la matrice
        
        coordinate[0] --> axe -y
        coordinate[1] --> axe x
    """
    coords = [(i, j) for j in range(len(matrix[len(matrix) - 1])) for i in range(len(matrix))]
    
    def ob_cell(matrix, coordinates = coords):
        cell_min = [((coordinates[0][0], coordinates[0][1]), matrix[coordinates[0][0]][coordinates[0][1]])]
        for c in coordinates:
            column = c[0]
            row = c[1]
            cell = matrix[column][row]
            if len(list(Counter(cell).elements())) == len(list(Counter(matrix[cell_min[0][0][0]][cell_min[0][0][1]]).elements())):
                cell_min.append(((column, row), matrix[column][row]))
            
            elif len(list(Counter(cell).elements())) < len(list(Counter(matrix[cell_min[0][0][0]][cell_min[0][0][1]]).elements())):
                cell_min = [((c[0], c[1]), cell)]
        
        return ran.choice(cell_min)
    
    if coordinate == None:
        return ob_cell(matrix)
    else:
        return ob_cell(matrix, coordinate)

def matrix_change(matrix, coords, dict_val : dict):
    """Donne une valeur parmiuns liste de valeur à une matrice sur une série de coordonnées"""
    for i in coords:
        matrix[column][row] = ran.choice(list(Counter(dict_val.elements())))
    return matrix

if __name__ == "__main__":   
    a = create_matrix((4, 4))
    print('\n'.join([str(i) for i in a]))
    print(f"up {up(a, (2, 1))}")
    print(f"down {down(a, (2, 1))}")
    print(f"left {left(a, (2, 1))}")
    print(f"right {right(a, (2, 1))}")
    
    print("test hors map")
    print(f"up {up(a, (0, 2))}")
    print(f"down {down(a, (3, 2))}")
    print(f"left {left(a, (2, 0))}")
    print(f"right {right(a, (3, 3))}")