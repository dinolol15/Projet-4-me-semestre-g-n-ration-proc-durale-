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
    
    test_value = len(matrix)*len(matrix[len(matrix) - 1])
    error = test_value*100
    
    while (error > 0 and test_value != 0):
        column = ran.randint(0, len(matrix) - 1)
        row = ran.randint(0, len(matrix[len(matrix) - 1]) - 1)
        cell = matrix[column][row]
        try:
            len(cell)
        except TypeError:
            error -= 1
            continue
        #mettre respect condition ici (peut-être try except)
        matrix[column][row] = ran.choice(cell)
        test_value -= 1
    return matrix


def condition():
    pass



if __name__ == "__main__":
    a = w_f_c_simplified(mm.create_matrix((20, 20), [1, 2, 3, 4]))
    print('\n'.join([str(i) for i in a]))