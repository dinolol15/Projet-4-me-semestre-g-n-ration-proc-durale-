"""
Programme créant une carte

Auteur: Adrien Buschbeck
"""

import random as ran
import matrix_manager as mm

def w_f_c_simplified(matrix):
    """Retourne une matrix générée avec un wfc simplifié

    Les éléments de la matrix doivent être des listes
    """
    
    coordinates = [(i, j) for j in range(len(matrix[len(matrix) - 1])) for i in range(len(matrix))]
    test_value = len(matrix)*len(matrix[len(matrix) - 1])
    
    while test_value != 0:
        cell = mm.random_cell(matrix, coordinates)
        coordinates.remove((cell[0][0], cell[0][1]))
        #mettre respect condition ici (peut-être try except)
        matrix[cell[0][0]][cell[0][1]] = ran.choice(cell[1])
        test_value -= 1
    return matrix


def condition():
    pass



if __name__ == "__main__":
    a = w_f_c_simplified(mm.create_matrix((10, 10), [1, 2, 3, 4]))
    print('\n'.join([str(i) for i in a]))