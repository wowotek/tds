from PIL import Image
import numpy as np

from shared import *

def loadMap(path: str):
    print(f"Loading Map ({path})")
    img = Image.open(path)

    map_data = np.array(img).tolist()
    map_ent: list[list[Static | Entity]] = []
    for i in range(len(map_data)):
        row: list[Static | Entity] = []
        for j in range(len(map_data[i])):
            g = map_data[i][j]
            c = (g[0], g[1], g[2], g[3])
            
            if   c == (0, 0, 0, 255):
                row.append(Wall((j, i)))
            elif c == (0, 0, 255, 255):
                row.append(Forcefield((j, i)))
            elif c == (255, 0, 0, 255):
                row.append(BombArea((j, i), "A"))
            elif c == (0, 255, 0, 255):
                row.append(BombArea((j, i), "B"))
            elif c == (255, 0, 255, 255):
                row.append(Box((j, i)))
            elif c == (255, 255, 0, 255):
                row.append(Barrel((j, i)))
            elif c == (100, 100, 255, 255):
                row.append(Player((j, i)))
            elif c == (100, 100, 0, 255):
                row.append(Player((j, i)))
            else:
                row.append(" ")
    
        map_ent.append(row)

    walls: list[Wall] = []
    for i in map_ent:
        wall_start: None | Wall = None
        for j in i:
            if type(j) == Wall:
                if wall_start == None:
                    wall_start = j
                    continue
                else:
                    j: Wall = j
                    wall_start.tr = j.tr
                    wall_start.br = j.br
            else:
                if wall_start != None:
                    walls.append(wall_start)
                    wall_start = None
        
        if wall_start != None:
            walls.append(wall_start)
    
    other = []
    for i in map_ent:
        for j in i:
            if type(j) == Wall or type(j) == str: continue
            other.append(j)
    
    r = walls + other
    entities = [i for i in r if i.stype == "ENTITY"]
    statics = [i for i in r if i.stype == "STATIC"]
    return {
        "entities": entities,
        "statics": statics
    }
    
loadMap("res/map1.png")