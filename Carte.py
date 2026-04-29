"""
Programme créant une carte

Auteur: Adrien Buschbeck
"""

from collections import Counter
import dataclasses as dc
from dataclasses import dataclass
import random as ran
import matrix_manager as mm


def water_placement(matrix: mm.Matrix, coordinate: mm.Coordinate, humidity,
                    set_of_value: dict=None): #toDo fix ahh bug
    """
    Place des zones d'eau de départ
    humidity --> nombres de point d'eau aux départs
    """
    coords_water = []
    for _ in range(humidity):
        coord = ran.choice(coordinate)
        coords_water.append(coord)
        coordinate.remove(coord)
    matrix = mm.matrix_change(matrix, coords_water, {Water: 1})
    return (coordinate, matrix, coords_water)


def w_f_c_evolved(matrix: mm.Matrix, water_p_val: int,
                  ran_wal_value: tuple[int, int, object], humidity: int=1):
    """
    Retourne une matrix générée avec un wfc simplifié

    Les éléments de la matrix doivent être des listes    
    ne marche qu'avec un triple élément
    
    water_p_val --> nombre de tuiles d'eau placées au départ
    """
    
    COORDINATES = [(i, j) for j in range(len(matrix[len(matrix) - 1])) for i in range(len(matrix))]
    coordinates = COORDINATES
    MATRIX_SIZE = (len(matrix), len(matrix[len(matrix) - 1]))
    coordinates, matrix, water_coordinates = water_placement(matrix,
                                                             coordinates,
                                                             water_p_val)
    
    for i in range(humidity):
        matrix = mm.random_walk(matrix, water_coordinates,
                                ran_wal_value[0], ran_wal_value[1],
                                ran_wal_value[2])
    
    for p in COORDINATES:
        matrix = mm.in_concact(matrix, p, Water, Coast, Water)
        if matrix[p[0]][p[1]] != Water and  matrix[p[0]][p[1]] != Coast:
            matrix[p[0]][p[1]] = Ground
    
    for p in COORDINATES:
        matrix = mm.fill(matrix, p)
    
    return matrix


def w_f_c_simplified(matrix: mm.Matrix):
    """
    Retourne une matrix générée avec un wfc simplifié

    Les éléments de la matrix doivent être des listes
    """
    
    COORDINATES = [(i, j) for j in range(len(matrix[len(matrix) - 1])) for i in range(len(matrix))]
    coordinates = [(i, j) for j in range(len(matrix[len(matrix) - 1])) for i in range(len(matrix))]
    MATRIX_SIZE = (len(matrix), len(matrix[len(matrix) - 1]))
    test_value = len(matrix)*len(matrix[len(matrix) - 1])
    
    
    while test_value != 0:
        cell = mm.lobject_cell(matrix, coordinates)
        coordinates.remove((cell[0][0], cell[0][1]))
        if len(cell[1]) == 0:
            print("Contradiction atteinte")
            print(test_value)
            break
        
        matrix[cell[0][0]][cell[0][1]] = ran.choice(list(Counter(cell[1])
                                                         .elements()))
        condition(matrix, ((cell[0][0], cell[0][1]),
                           matrix[cell[0][0]][cell[0][1]]))
        test_value -= 1
    
    for i in COORDINATES:
        matrix = mm.fill(matrix, i)
    
    return matrix


def condition(matrix: mm.Matrix, cell):
    """
    Enlève les possibilitées impossibles avec l'argument wfc_delete

    position[0] : axe -y
    position[1] : axe x
    """
    position = (cell[0][0], cell[0][1])
    cell = matrix[position[0]][position[1]]
    for i in range(4):
        match i:
            case 0:
                cell1 = mm.up(matrix, position)
            case 1:
                cell1 = mm.down(matrix, position)
            case 2:
                cell1 = mm.right(matrix, position)
            case 3:
                cell1 = mm.left(matrix, position)
        
        try:
            list(Counter(cell1[1]))
        except TypeError:
            continue
        
        matrix[cell1[0][0]][cell1[0][1]] = {tile: count for tile, count in cell1[1].items() if tile.Name not in cell.wfc_delete}                
        
            
@dataclass(eq=True, frozen=True)
class Tile:
    """
    Classe représentant les différents types de terrains
    Name --> Nom
    Colour --> couleur par laquelle le terrain va être représenté (systèem RGB)
    wfc_delete --> terrain qui ne peuvent pas être à côté (conectivité 4)
    """
    
    Name: str
    Color: tuple[int, int, int] = dc.field(default_factory=tuple[int, int, int])
    wfc_delete: tuple = dc.field(default_factory=tuple)
    #wealth: float will add if time and if Albert
    #wildness: float will add if time and if Albert
    
    def __repr__(self):
        return self.Name[0]


Placeholer = Tile("Placeholer", (255, 255, 255), (),) #(0, 0,)
Plain = Tile("Plain", (124, 252, 0), ("Sea", "River")) #(1, 1,)
Mountain = Tile("Mountain", (139, 137, 137), ("Sea", "River")) #(0.25, 10,)
Forest = Tile("Forest", (34, 139, 34), ("Sea", "Desert", "River")) #(1.25, 5,)
Sea = Tile("Sea", (28, 107, 160), ("Plain", "Mountain", "Forest", "Desert")) #(0, 10000,)
River = Tile("River", (70, 130, 180), ("Plain", "Mountain", "Forest")) #(0, 3,)
Desert = Tile("Desert", (237, 201, 175), ("Sea", "Forest")) #(0.1, 0.5,)

#obligatoire pour w_f_c_evolved
Water = Tile("Water",  (70, 130, 180), ("Ground",)) #(1, 1,)
Coast = Tile("Coast", (237, 201, 175), ()) #(1, 1,)
Ground = Tile("Ground", (34, 139, 34), ("Water",)) #(1, 1,)

if __name__ == "__main__":
    
    
    a = w_f_c_simplified(mm.create_matrix((10, 10), {Plain:3, Mountain:1,
                                                     Forest:2, Desert:2,
                                                     Sea:1, River:2}))
    
    b = w_f_c_evolved(mm.create_matrix((10, 10), {Water:1, Ground:1, Coast:1}),
                      5, [25, 1, Water])
    
    print('\n'.join([str(i) for i in b]))