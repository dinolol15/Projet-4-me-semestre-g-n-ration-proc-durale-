"""
Gère plusieurs opérations sur des matrcies

Autreur: Adrien Buschbeck
"""
import itertools as it


def create_matrix(dim: tuple[int, int] | list[int, int]) -> list:
    """retourne une matrice
    dim[0] --> axe -y
    dim[1] --> axe x
    """
    liste = [0,1,2,3,4,5,6,7,8,9,10,11]
    return [[ j + i**2 for j in range(dim[1])] for i in range(dim[0])]


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