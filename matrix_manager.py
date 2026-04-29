"""
Gère plusieurs opérations sur des matrcies

Auteur: Adrien Buschbeck, Albert Stanislawek
"""

from collections import Counter
import dataclasses as dc
from dataclasses import dataclass
import itertools as it
import random as ran
from typing import TypeAlias

Position: TypeAlias = tuple[int, int]
Coordinate: TypeAlias = list[Position,]
Matrix: TypeAlias = list[list[object, ...],]

def create_matrix(dim: tuple[int, int] | list[int, int],
                  element : object = 0) -> list:
    """
    Retourne une matrice où chaque cellule est remplie par element
    dim[0] --> axe -y
    dim[1] --> axe x
    """
    return [[element for j in range(dim[1])] for i in range(dim[0])]


def up(matrix: Matrix, position: Position):
    """
    Retourne la position et la valeur d'une cellule en haut d'une cellule
    position[0] --> axe -y
    position[1] --> axe x
    """
    if position[0] == 0:
        return None 
    return ((position[0] - 1, position[1]),
            matrix[position[0] - 1][position[1]])
    

def down(matrix: Matrix, position: Position):
    """
    Retourne la position et la valeur d'une cellule en bas d'une cellule
    position[0] --> axe -y
    position[1] --> axe x
    """
    if position[0] >= len(matrix) - 1 :
        return None
    return ((position[0] + 1, position[1]),
            matrix[position[0] + 1][position[1]])
    
    
def right(matrix: Matrix, position: Position):
    """
    Retourne la position et la valeur d'une cellule à droite d'une cellule
    position[0] --> axe -y
    position[1] --> axe x
    """
    if position[1] == len(matrix[position[0]]) - 1:
        return None 
    return ((position[0], position[1] + 1),
            matrix[position[0]][position[1] + 1])

    
def left(matrix: Matrix, position: Position):
    """
    Retourne la position et la valeur d'une cellule à gauche d'une cellule
    position[0] --> axe -y
    position[1] --> axe x
    """
    if position[1] == 0:
        return None
    return ((position[0], position[1] - 1),
            matrix[position[0]][position[1] - 1])

def random_cell(matrix: Matrix, coordinate: Coordinate = None):
    """
    Retourne la valeur et la position aléatoire
    d'une cellule cellule aléatoire d'une matrice
    parmi une série de coordonnées 
     
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


def lobject_cell(matrix: Matrix, coordinate: Coordinate = None):
    """
    Retourne la valeur et la position aléatoire
    de la cellule avec le moins d'éléments dans la matrice
        
    coordinate[0] --> axe -y
    coordinate[1] --> axe x
    """
    coords = [(i, j) for j in range(len(matrix[len(matrix) - 1])) for i in range(len(matrix))]
    
    def ob_cell(matrix, coordinates = coords):
        cell_min = [((coordinates[0][0], coordinates[0][1]),
                     matrix[coordinates[0][0]][coordinates[0][1]])]
        for c in coordinates:
            column = c[0]
            row = c[1]
            cell = matrix[column][row]
            
            vartest = len(list(Counter(matrix[cell_min[0][0][0]][cell_min[0][0][1]])
                               .elements()))
            
            if len(list(Counter(cell).elements())) == vartest:
                cell_min.append(((column, row), matrix[column][row]))
            
            elif len(list(Counter(cell).elements())) < vartest:
                cell_min = [((c[0], c[1]), cell)]
        
        return ran.choice(cell_min)
    
    if coordinate == None:
        return ob_cell(matrix)
    else:
        return ob_cell(matrix, coordinate)

def matrix_change(matrix: Matrix, coordinate: Coordinate, dict_val : dict):
    """
    Donne une valeur parmiuns liste de valeur
    à une matrice sur une série de coordonnées
    """
    for i in coordinate:
        matrix[i[0]][i[1]] = ran.choice(list(Counter(dict_val).elements()))
    return matrix


def fill(matrix: Matrix, position_cell : Position):
    """
    Regarde si une cellule est entourée de cellule de la même valeur
    le cas échéant, donne la même valeur à la cellule
    """
    test_value = True
    
    if up(matrix, position_cell) == None:
        print(down(matrix, position_cell))
        value_desired = down(matrix, position_cell)[1]
    else: 
        value_desired = up(matrix, position_cell)[1]
        
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
        if func(matrix, position_cell) != None :
            if func(matrix, position_cell)[1] != value_desired:
                test_value = False
    if test_value:
        matrix[position_cell[0]][position_cell[1]] = value_desired
    return matrix

            
def random_walk(matrix: Matrix, starting_pos: Coordinate,
                steps: int, max_lenght: int, value: object):        
        """
        Réalise l'algorythme de random walk
        """
        for p in starting_pos:
            actual_position = p
            for i in range(steps):
                direction = ran.randint(0,3)
                match direction:
                    case 0:
                        func = up
                    case 1:
                        func = down
                    case 2:
                        func = right
                    case 3:
                        func = left
                
                lenght = ran.randint(0, max_lenght)
                for _ in range(lenght):
                    if func(matrix, actual_position) != None:
                        actual_position = func(matrix, actual_position)[0]
                    matrix[actual_position[0]][actual_position[1]] = value
        return matrix
                

def in_concact(matrix: Matrix, position_cell: Position,
               value_desired: object, value_given: object,
               except_value: object):
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
        if func(matrix, position_cell) != None:
            if func(matrix, position_cell)[1] == value_desired:
                if matrix[position_cell[0]][position_cell[1]] != except_value:
                    test_value = True
                    break
    
    if test_value:
        matrix[position_cell[0]][position_cell[1]] = value_given
    return matrix

def test():
    matrix_test = create_matrix((10, 10))
    
    matrix_test[1][0] = "left"
    matrix_test[1][2] = "right"
    matrix_test[0][1] = "up"
    matrix_test[2][1] = "down"
    #test in map
    assert up(matrix_test, (1, 1))[1] == "up"
    assert down(matrix_test, (1, 1))[1] == "down"
    assert left(matrix_test, (1, 1))[1] == "left"
    assert right(matrix_test, (1, 1))[1] == "right"
    #test hors map
    assert up(matrix_test, (0, 2)) == None
    assert down(matrix_test, (9, 2)) == None
    assert left(matrix_test, (5, 0)) == None
    assert right(matrix_test, (9, 9)) == None
    print("tous les tests sont passés")
        

if __name__ == "__main__":   
    test()