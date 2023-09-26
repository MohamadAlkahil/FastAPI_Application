from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
import numpy as np
import random
import string
import hashlib

app = FastAPI()

class Map(BaseModel):
    xdim: int
    ydim: int
    map: str

class UpMap(BaseModel):
    xdim: int
    ydim: int

class Mine(BaseModel):
    x: int
    y: int
    serial_num: int

class Rover(BaseModel):
    roverStatus:str
    x:int
    y:int
    moves:str

map_dic = {
    0: Map(xdim=30, ydim=30, map="000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001")
}

mines = {
    0: Mine(x=2, y=12, serial_num=2747236731),
    1: Mine(x=5, y=9, serial_num=6998631691),
    2: Mine(x=8, y=8, serial_num=8194841610),
    3: Mine(x=10, y=5, serial_num=1195863030),
    4: Mine(x=11, y=11, serial_num=2992722015),
    5: Mine(x=14, y=14, serial_num=7332598233),
    6: Mine(x=17, y=17, serial_num=8138960630),
    7: Mine(x=20, y=20, serial_num=7283568440),
    8: Mine(x=23, y=23, serial_num=7360826750),
    9: Mine(x=26, y=26, serial_num=5872908855),
    10: Mine(x=29, y=29, serial_num=4248912305)
}

rovers = {
    1:Rover(roverStatus="Not Started",x=0,y=0,moves="MMMMRMLRRRLRMLMRMLMMMLMMRMMLDMLMMMMMLRLLRDMMMLDMLRDMRLMRMRMRRMLRLLRMDRMRDLMDLM"),
    2:Rover(roverStatus="Not Started",x=0,y=0,moves="MRDRMMLMLRDRLLMRLLMMRDLMLDMLDLDLDLRLMRLMMRMRLMLMLMDMRLRMMMMMMM"),
    3:Rover(roverStatus="Not Started",x=0,y=0,moves="MMRLMRDLMMLLMMDMLMRMRDMMMMRDRMMMMMRRDMLMRMLRRLDMMRLMRRRRDLMMDMLMRLLLMRLDMRRRMLDM"),
    4:Rover(roverStatus="Not Started",x=0,y=0,moves="MLLMLDMMMLDLMRLMMDMMDRMRMMLMDRMMRMLLLLDRMMDMMDRMMMMRRDMLRMRLMDMRDRMRLMMRMRMDMRMMMDRLMMLRRDRLLMMRMLRMRLLLRMRLRRDMLRMMLMRRDMRMRMRRLMRMM"),
    5:Rover(roverStatus="Not Started",x=0,y=0,moves="MRMMMLRMRMMRMMLLMMMDLRRMMLMMLLMRMMLRMRLMLRLRMDMRDLMLLMRMMMMMLMDLMRRLMMMMMLLLMMLLDRLMLDMLRRMMLDRLRLMRMDLMLLDLMRMMM"),
    6:Rover(roverStatus="Not Started",x=0,y=0,moves="MMRMMMRRRLDMLLRMMRLRMLDMMMLMMRMRMMRMMMRMLRRLMRMRMLDLMMDMRLDMMRRLMLRDMDMMMMR"),
    7:Rover(roverStatus="Not Started",x=0,y=0,moves="RLDMMMMRLRRMMLMMMMMLMMDMDMLDMLMRLRMLMLMDMLMLMMLLMMRLMMDMLLMMDMDMMMDMMLMRLMRDLLMDMDMLLMDLRDMMMRRLRMMLMLRLMDMLMMDMMLDL"),
    8:Rover(roverStatus="Not Started",x=0,y=0,moves="DMLLLMDLDLMMMDRRMMLMMRRMMDLMRLDLLLLLMMMMMMMMRMRRMMMMDMMMMLDRLRMMRMDLLMLRMLRLLMMMMMRMMRMMMMLMDRRML"),
    9:Rover(roverStatus="Not Started",x=0,y=0,moves="DLMRMLMMRMDRRDLRLMLMLMMRMRLMMMRMMMMLMMRMMRMRLMRDMMMLLMRDMMRRLLLRMLLLMRMRRMRMLLRRDMMMML"),
    10:Rover(roverStatus="Not Started",x=0,y=0,moves="MMDMMLMLRLLRMRMMLMRDMLMLMLMMMLMRRMMLMMRDLLRMLMMMRMMMRMRMMRLMMRRR")
}

@app.get("/")
def read_root():
    return {"Hello": "Server"}

@app.get("/map")
def get_map():
    return {"MAP": map_dic[0]}

@app.put("/map")
def update_map(upmap: UpMap):
    current_x = map_dic[0].xdim
    current_y = map_dic[0].ydim
    mapstr = "0" * (upmap.xdim * upmap.ydim)
    for i in range(current_y):
        start = i * current_x
        end = start + current_x
        row = map_dic[0].map[start:end]
        mapstr = mapstr[:i*upmap.xdim] + row + "0"*(upmap.xdim-current_x) + mapstr[(i+1)*upmap.xdim:]
    if current_y < upmap.ydim:
        mapstr += "0" * (upmap.xdim * (upmap.ydim - current_y))
    map_dic[0] = Map(xdim=upmap.xdim, ydim=upmap.ydim, map=mapstr)
    return {"Sucessful Map Update"}

@app.get("/mines")
def get_mines()-> dict[str, dict[int, Mine]]:
    return {"mines" : mines}

@app.get("/mines/{mine_id}")
def get_mine(mine_id: int)-> Mine:
    if mine_id not in mines:
        HTTPException(status_code=404, detail=f"Mine with {mine_id=} does not exist.")

    return mines[mine_id]

def Switch(x, y, value):
    map_obj = map_dic[0]
    map_list = list(map_obj.map)
    index = y * map_obj.xdim + x
    map_list[index] = str(value)
    map_str = ''.join(map_list)
    new_map = Map(xdim=map_obj.xdim, ydim=map_obj.ydim, map=map_str)
    map_dic[0] = new_map

@app.delete("/mines/{mine_id}")
def delete_mine(mine_id: int) -> dict[str, Mine]:
        if mine_id not in mines:
            HTTPException(status_code=404, detail=f"Mine with {mine_id=} does not exist.")

        mine = mines.pop(mine_id)
        Switch(mine.x, mine.y, 0)
        for i in range(mine_id + 1, len(mines) + 1):
            mines[i - 1] = mines.pop(i)

        return {"deleted": mine}

@app.post("/mines")
def create_mine(mine: Mine):
    if mine.serial_num in mines:
        HTTPException(status_code=400, detail="Mine already exists")
    new_id = len(mines)
    mines[new_id] = mine
    Switch(mine.x, mine.y, 1)
    return {"id": new_id}

@app.put("/mines/{mine_id}")
def update_mine(mine: Mine, mine_id: int) -> dict[str, Mine]:
    Switch(mines[mine_id].x, mines[mine_id].y, 0)
    mines[mine_id] = mine
    Switch(mine.x, mine.y, 1)
    return {"updated": mine}

@app.get("/rovers")
def get_rovers()-> dict[str, dict[int, Rover]]:
    return {"rovers" : rovers}

@app.get("/rovers/{rover_id}")
def get_rovers(rover_id: int)-> Rover:
    if rover_id not in rovers:
        HTTPException(status_code=404, detail=f"Rover with {rover_id=} does not exist.")
    return rovers[rover_id]

@app.post("/rovers")
def create_rovers(rover: Rover):
    new_id = len(rovers)+1
    rovers[new_id] = rover
    return {"id" : new_id }

@app.delete("/rovers/{rover_id}")
def delete_rovers(rover_id: int) -> dict[str, Rover]:
    if rover_id not in rovers:
        HTTPException(status_code=404, detail=f"Rover with {rover_id=} does not exist.")

    rover = rovers.pop(rover_id)
    for i in range(rover_id, len(rovers) + 1):
        rovers[i] = rovers.pop(i+1)
    return {"deleted": rover}

@app.put("/rovers/{rover_id}")
def update_rover(rover: Rover, rover_id: int) -> dict[str, Rover]:
    rovers[rover_id] = rover
    return {"updated": rover}

@app.post("/rovers/{rover_id}/dispatch")
def dispatch_rovers(rover_id: int):
    if rover_id not in rovers:
        HTTPException(status_code=404, detail=f"Rover with {rover_id=} does not exist.")
    path, executed = walk_path(rovers[rover_id],rover_id, map_dic[0])
    path_into_file(map_dic[0].xdim, map_dic[0].ydim, path, rover_id)

    return {"Rover Id": rover_id, "Rover Status": rovers[rover_id].roverStatus, "x": rovers[rover_id].x, "y": rovers[rover_id].y, "Executed Moves": executed}

def Map_str_to_arr(xdim, ydim, out):
    count = 0
    map = np.zeros(shape=(xdim, ydim))
    for i in range(xdim):
        for j in range(ydim):
            map[i, j] = out[count]
            count += 1
    return map

def get_serial(y, x):
    for i in range(len(mines)):
        if mines[i].x == x and mines[i].y == y:
            serial_num = str(mines[i].serial_num)
    return serial_num

def dig(r, serial):
    check=False
    while(check == False):
        pin = ''.join(random.choice(string.digits) for i in range(12))
        temporary_mine_key = pin+str(serial)
        result = hashlib.sha256(temporary_mine_key.encode()).hexdigest()
        if(r==1 and result[0:6]=="000000"):
            check=True
        elif (r!=1):
            check = True
    return result

def walk_path(Rover, rover_id,Map):
    xdim = Map.xdim
    ydim = Map.xdim
    path = Map_str_to_arr(xdim, ydim, Map.map)
    rover = rover_id
    moves = Rover.moves
    Rover.roverStatus = "Moving"
    facing="S"
    x_dir=0
    y_dir=0
    path[y_dir, x_dir] = "8"
    executed = ""
    for i in moves:
        Rover.x = x_dir
        Rover.y = y_dir
        executed += i
        if i != "D" and path[y_dir, x_dir] == 9:
            Rover.roverStatus = "Eliminated"
            break
        elif i == "D" and path[y_dir, x_dir] == 9:
            serial_num = get_serial(y_dir, x_dir)
            dig(int(rover), serial_num)
            path[y_dir, x_dir] = "8"
        elif i == "M":
            if facing == "N" and y_dir > 0:
                y_dir -= 1
                if path[y_dir, x_dir] == 1:
                    path[y_dir, x_dir] = "9"
                else:
                    path[y_dir, x_dir] = "8"
            elif facing == "S" and y_dir < ydim:
                y_dir += 1
                if path[y_dir, x_dir] == 1:
                    path[y_dir, x_dir] = "9"
                else:
                    path[y_dir, x_dir] = "8"
            elif facing == "E" and x_dir < xdim:
                x_dir += 1
                if path[y_dir, x_dir] == 1:
                    path[y_dir, x_dir] = "9"
                else:
                    path[y_dir, x_dir] = "8"
            elif facing == "W" and x_dir > 0:
                x_dir -= 1
                if path[y_dir, x_dir] == 1:
                    path[y_dir, x_dir] = "9"
                else:
                    path[y_dir, x_dir] = "8"
        elif i == "R":
            if facing == "N" and x_dir < xdim:
                facing = "E"
                x_dir += 1
                if path[y_dir, x_dir] == 1:
                    path[y_dir, x_dir] = "9"
                else:
                    path[y_dir, x_dir] = "8"
            elif facing == "S" and x_dir > 0:
                facing = "W"
                x_dir -= 1
                if path[y_dir, x_dir] == 1:
                    path[y_dir, x_dir] = "9"
                else:
                    path[y_dir, x_dir] = "8"
            elif facing == "E" and y_dir < ydim:
                facing = "S"
                y_dir += 1
                if path[y_dir, x_dir] == 1:
                    path[y_dir, x_dir] = "9"
                else:
                    path[y_dir, x_dir] = "8"
            elif facing == "W" and y_dir > 0:
                facing = "N"
                y_dir -= 1
                if path[y_dir, x_dir] == 1:
                    path[y_dir, x_dir] = "9"
                else:
                    path[y_dir, x_dir] = "8"
        elif i == "L":
            if facing == "N" and x_dir > 0:
                facing = "W"
                x_dir -= 1
                if path[y_dir, x_dir] == 1:
                    path[y_dir, x_dir] = "9"
                else:
                    path[y_dir, x_dir] = "8"
            elif facing == "S" and x_dir < xdim:
                facing = "E"
                x_dir += 1
                if path[y_dir, x_dir] == 1:
                    path[y_dir, x_dir] = "9"
                else:
                    path[y_dir, x_dir] = "8"
            elif facing == "E" and y_dir > 0:
                facing = "N"
                y_dir -= 1
                if path[y_dir, x_dir] == 1:
                    path[y_dir, x_dir] = "9"
                else:
                    path[y_dir, x_dir] = "8"
            elif facing == "W" and y_dir < ydim:
                facing = "S"
                y_dir += 1
                if path[y_dir, x_dir] == 1:
                    path[y_dir, x_dir] = "9"
                else:
                    path[y_dir, x_dir] = "8"
    if Rover.roverStatus != "Eliminated":
        Rover.roverStatus = "Finished"

    return path,executed

def path_into_file(xdim, ydim,path, rover):
    file_name="path_"+str(rover)+".txt"
    f = open(file_name, "w")
    for j in range(ydim):
        for i in range(xdim):
            if path[j,i] == 8 or path[j,i] == 9:
                f.write("*")
            else:
                f.write("0")
    f.close()

