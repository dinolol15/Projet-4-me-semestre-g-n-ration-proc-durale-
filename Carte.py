"""
Programme créant une carte

Auteur: Adrien Buschbeck
"""

import random as ran
import matrix_manager as mm

def w_f_c_simplified(matrice):
    """Retourne une matrice générée avec un wfc simplifié

    Les éléments de la matrice doit être des listes
    """
    a = 100
    test_value = len(matrice)*len(matrice[len(matrice) - 1])
    
    while (a > 0 and test_value != 0):
        column = ran.randint(0, len(matrice) - 1)
        row = ran.randint(0, len(matrice[len(matrice) - 1]) - 1)
        cell = matrice[column][row]
        
        try:
            len(cell)
        except TypeError:
            a -= 1
            continue
        matrice[column][row] = ran.choice(cell)
        
        test_value -= 1
    return matrice


def condition():
    pass



if __name__ == "__main__":
    a = w_f_c_simplified(mm.create_matrix((4, 4), [1, 2, 3, 4]))
    print('\n'.join([str(i) for i in a]))