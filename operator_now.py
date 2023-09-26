import requests
import numpy as np
import json
from pydantic import BaseModel


def getMap():
    response = requests.get("http://127.0.0.1:8000/map").json()
    xdim = response['MAP']['xdim']
    ydim = response['MAP']['ydim']
    out = response['MAP']['map']
    count = 0
    map = np.zeros(shape=(xdim, ydim))
    for i in range(xdim):
        for j in range(ydim):
            map[i, j] = out[count]
            count += 1

    print("xdim:",xdim)
    print("ydim:", ydim)
    print("Map:\n",map)

def putMap(x, y):
    upmap ={"xdim": x, "ydim": y}
    response = requests.put("http://127.0.0.1:8000/map/",json=upmap).json()
    print(response)

def getMines():
    response = requests.get("http://127.0.0.1:8000/mines").json()
    print(response)

def getMinesid(id):
    response = requests.get("http://127.0.0.1:8000/mines/"+str(id)).json()
    print(response)

def deleteMine(id):
    response = requests.delete("http://127.0.0.1:8000/mines/" + str(id)).json()
    print(response)

def postMine(x, y, serial_num):
    mine ={"x": x, "y": y, "serial_num": serial_num}
    response = requests.post("http://127.0.0.1:8000/mines/",json=mine).json()
    print(response)

def putMine(id, x, y, serial_num):
    mine ={"x": x, "y": y, "serial_num": serial_num}
    response = requests.put("http://127.0.0.1:8000/mines/"+ str(id) + "/",json=mine).json()
    print(response)

def getrovers():
    response = requests.get("http://127.0.0.1:8000/rovers").json()
    print(response)

def getroversid(id):
    response = requests.get("http://127.0.0.1:8000/rovers/"+str(id)).json()
    print(response)

def postRover(moves):
    rover ={"roverStatus": "Not Started","x": 0, "y": 0, "moves": moves}
    response = requests.post("http://127.0.0.1:8000/rovers/",json=rover).json()
    print(response)

def deleterover(id):
    response = requests.delete("http://127.0.0.1:8000/rovers/" + str(id)).json()
    print(response)

def putRover(id, roverStatus, x, y, moves):
    rover = {"roverStatus": roverStatus, "x": x, "y": y, "moves": moves}
    response = requests.put("http://127.0.0.1:8000/rovers/" + str(id) + "/", json=rover).json()
    print(response)

def dispatchRover(id):
    response = requests.post("http://127.0.0.1:8000/rovers/"+ str(id) + "/dispatch").json()
    print(response)

def start_message():
    print("Enter one of the following integers to run a command:\n")
    print("1: Retrieve Map")
    print("2: Update Map")
    print("3: Retrieve Mines")
    print("4: Retrieve Mine by Id")
    print("5: Delete Mine by Id")
    print("6: Create Mine")
    print("7: Update Mine")
    print("8: Retrieve Rovers")
    print("9: Retrieve Rover by Id")
    print("10: Create Rover")
    print("11: Delete Rover")
    print("12: Update Rover")
    print("13: Dispatch Rover")
    print("q: Quit")
    print("\n")


while(True):
    start_message()
    key = input()
    if(key == 'q'):
        print("The Operator is now closed.")
        break
    if (key == '1'):
        getMap()
    if (key == '2'):
        xdim = input('Enter the new xdim:')
        ydim = input('Enter the new ydim:')
        putMap(xdim, ydim)
    if (key == '3'):
        getMines()
    if (key == '4'):
        id = input('Enter the mine id of interest:')
        getMinesid(id)
    if (key == '5'):
        id = input('Enter the mine id of interest:')
        deleteMine(id)
    if (key == '6'):
        x = int(input('Enter the x coordinate of the mine:'))
        y = int(input('Enter the y coordinate of the mine:'))
        serial_num = int(input('Enter the serial number of the mine:'))
        postMine(x, y, serial_num)
    if (key == '7'):
        id = input('Enter the mine id of interest:')
        x = int(input('Enter the x coordinate of the mine:'))
        y = int(input('Enter the y coordinate of the mine:'))
        serial_num = int(input('Enter the serial number of the mine:'))
        putMine(id, x, y, serial_num)
    if (key == '8'):
        getrovers()
    if (key == '9'):
        id = input('Enter the rover id of interest:')
        getroversid(id)
    if (key == '10'):
        moves = input('Enter the moves of the rover:')
        postRover(moves)
    if (key == '11'):
        id = input('Enter the rover id of interest:')
        deleterover(id)
    if (key == '12'):
        id = input('Enter the rover id of interest:')
        roverStatus = input('Enter the rover status  (Not Started, Finished, Moving, or Eliminated):')
        x = int(input('Enter the x coordinate of the rover:'))
        y = int(input('Enter the y coordinate of the rover:'))
        moves = input('Enter the moves of the rover:')
        putRover(id, roverStatus, x, y, moves)
    if (key == '13'):
        id = input('Enter the rover id of interest:')
        dispatchRover(id)