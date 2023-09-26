# FastAPI_Application

## Overview
This Python project simulates rovers navigating a minefield represented as a 2D array, where each cell contains either a mine (non-zero) or is empty (zero). The rover can follow commands like turning left (L), turning right (R), moving forward (M), and digging (D). The code sequentially processes each rover's commands, starting at the initial position (0,0) facing south, and calculates the rover's path on the map. It marks the path with "*" symbols and handles scenarios where rovers encounter mines. If a rover doesn't dig a mine and moves, the mine explodes, and the remaining commands are ignored. The project is split into a Server and an Operator. The FastAPI HTTP server provides various endpoints that are to be used by the operator to control the rover. The server is deployed as a local container through Docker and then hosted as a web app on Azure.  The operator is a command line interface that takes keyboard inputs from the application's end user to control the rover. 

## Video Demo

## Operator
The operator interacts with the server by making HTTP requests to its endpoints. It allows the end user to perform various operations on the map, mines, and rovers, such as retrieving information, updating dimensions, creating/deleting objects, and dispatching rovers on their paths. The operator provides a menu of options for the end user to choose from and displays server responses in a readable and user-friendly manner.

## Server
The FastAPI HTTP server provides various endpoints that are to be used by the operator to control the rover. These endpoints allow the operator to create, modify, delete, or dispatch rovers and control them in real-time. The communication between the server and the operator is done using JSON format. The server is deployed as a local container through Docker and then hosted as a web app on Azure.

### Endpoints

#### Map

##### GET `/map`
Retrieves the 2D array of the field.

##### PUT `/map`
Updates the height and width of the field.

#### Mines

##### GET `/mines`
Retrieves the list of all mines, including their serial numbers and coordinates.

##### GET `/mines/:id`
Retrieves a specific mine by its ID.

##### DELETE `/mines/:id`
Deletes a specific mine by its ID.

##### POST `/mines`
Creates a new mine with coordinates and a serial number.

##### PUT `/mines/:id`
Updates a specific mine's coordinates and serial number.

#### Rovers

##### GET `/rovers`
Retrieves the list of all rovers, including their IDs and statuses.

##### GET `/rovers/:id`
Retrieves a specific rover by its ID, including its status, position, and list of commands.

##### POST `/rovers`
Creates a new rover with a list of commands.

##### DELETE `/rovers/:id`
Deletes a specific rover by its ID.

##### PUT `/rovers/:id`
Sends a list of commands to a rover by its ID.

##### POST `/rovers/:id/dispatch`
Dispatches a rover by its ID, providing information on its status, position, and executed commands.
