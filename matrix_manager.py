"""
Gère plusieurs opérations sur des matrcies

Auteur: Adrien Buschbeck, Albert ...
"""

import itertools as it
import random as ran

def create_matrix(dim: tuple[int, int] | list[int, int], element : object = 0) -> list:
    """retourne une matrice où chaque cellule est remplie par element
    dim[0] --> axe -y
    dim[1] --> axe x
    """
    return [[element for j in range(dim[1])] for i in range(dim[0])]


def up(matrix, cell):
    """Retourne la cellule en haut d'une cellule
    cell[0] --> axe -y
    cell[1] --> axe x
    """
    if cell[0] == 0:
        return None 
    return matrix[cell[0] - 1][cell[1]]
    


def down(matrix, cell):
    """Retourne la cellule en bas d'une cellule
    cell[0] --> axe -y
    cell[1] --> axe x
    """
    if cell[0] >= len(matrix) - 1 :
        return None
    return matrix[cell[0] + 1][cell[1]]
    
    
    
def right(matrix, cell):
    """"Retourne la cellule à droite d'une cellule
    cell[0] --> axe -y
    cell[1] --> axe x
    """
    if cell[1] == len(matrix[cell[0]]) - 1:
        return None 
    return matrix[cell[0]][cell[1] + 1]
    
    
def left(matrix, cell):
    """Retourne la cellule à gauche d'une cellule
    cell[0] --> axe -y
    cell[1] --> axe x
    """
    if cell[1] == 0:
        return None
    return matrix[cell[0]][cell[1] - 1]

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