"""
Gère plusieurs opérations sur des matrcies

Autreur: Adrien Buschbeck
"""


def create_matrix(dim: tuple[int, int] | list[int, int]) -> list:
    """retourne une matrice
    dim[0] --> axe x
    dim[1] --> axe y
    """
    return [[j+2*i for j in range(dim[0])] for i in range(dim[1])]


def up(matrix, cell):
    """Retourne la cellule en haut d'une cellule
    cell[0] --> axe x
    cell[1] --> axe -y
    """
    if cell[1] == 0:
        return None 
    return matrix[cell[1] - 1][cell[0]]
    


def down(matrix, cell):
    """Retourne la cellule en bas d'une cellule
    cell[0] --> axe x
    cell[1] --> axe -y
    """
    if cell[1] == len(matrix):
        return None
    return matrix[cell[1] + 1][cell[0]]
    
    
    
def right(matrix, cell):
    """"Retourne la cellule à droite d'une cellule
    cell[0] --> axe x
    cell[1] --> axe -y
    """
    if cell[0] == len(matrix[cell[1]]):
        return None 
    return matrix[cell[1]][cell[0] + 1]
    
    
def left(matrix, cell):
    """Retourne la cellule à gauche d'une cellule
    cell[0] --> axe x
    cell[1] --> axe -y
    """
    if cell[0] == 0:
        return None
    return matrix[cell[1]][cell[0] - 1]

if __name__ == "__main__":   
    a = create_matrix((4, 4))
    print('\n'.join([str(i) for i in a]))
    print(f"up {up(a, (2, 1))}")
    print(f"down {down(a, (2, 1))}")
    print(f"left {left(a, (2, 1))}")
    print(f"right {right(a, (2, 1))}")
    
    print("test hors map")
    print(f"up {up(a, (2, 0))}")
    print(f"down {down(a, (2, 1))}")
    print(f"left {left(a, (0, 1))}")
    print(f"right {right(a, (2, 1))}")