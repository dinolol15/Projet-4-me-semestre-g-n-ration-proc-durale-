"""
Programme créant une carte

Auteur: Adrien Buschbeck
"""

import random as ran


def matrice_creation(dimension_y: int, dimension_x: int) -> list:
    """Fonction créant une matrice"""
    matrice = []
    for i in range(dimension_y):
        matrice.append([])
        for y in range(dimension_x):
            matrice[i].append(0)
    return matrice

def modification(matrice):
    """Modifie une matrice"""
    for i in matrice:
        for j in range(len(i)):
            i[j] = ran.randint(1, 3)
            
    return matrice


def condition():
    pass



if __name__ == "__main__":
    print(modification(matrice_creation(4, 4)))