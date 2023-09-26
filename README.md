# FastAPI_Application

## Overview
This Python project involves simulating rovers navigating a minefield represented as a 2D array, where each cell contains either a mine (non-zero) or is empty (zero).The rover can follow commands like turning left (L), turning right (R), moving forward (M), and digging (D). The code sequentially processes each rover's commands, starting at the initial position (0,0) facing south, and calculates the rover's path on the map. It marks the path with "*" symbols and handles scenarios where rovers encounter mines. If a rover doesn't dig a mine and moves, the mine explodes, and the remaining commands are ignored. The project is split into a Server and an Operator. The FastAPI HTTP server provides various endpoints that are to be used by the operator to control the rover. The operator is a command line interface that takes keyboard inputs from the end user of the application to control the rover. 

## Video Demo
