# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 15:34:18 2025

@author: Icham
"""
# Import necessary modules
import time
import os
from pynput import keyboard
from pynput.keyboard import Key
import copy

# Define variables
length = 10
height = 10
cells = []
for i in range(height):
    cells.append(['0' for _ in range(length)])
cur_i = 0
cur_j = 0
starting = True
born = [False,False,False,True,True,False,False,False,False] # Mask defining when a cell is born
surv = [False,False,False,True,True,False,False,False,False] # Mask defining when a cell survives
    
# Function to display the grid in the terminal
def display_grid():
    os.system('cls')
    for i in range(height):
        for j in range(length):
            if starting and cur_i == i and cur_j == j:
                print('#',end='')
            else:
                print(cells[i][j],end='')
        print()

# Function to read key presses
def on_press(key):
    global cur_i,cur_j,starting
    
    # Move cursor
    if key == Key.up:
        if cur_i > 0:
            cur_i -= 1
    if key == Key.down:
        if cur_i < height-1:
            cur_i += 1
    if key == Key.left:
        if cur_j > 0:
            cur_j -= 1
    if key == Key.right:
        if cur_j < length-1:
            cur_j += 1
    # Change cell to alive / dead
    if key == Key.space:
        if cells[cur_i][cur_j] == '0':
            cells[cur_i][cur_j] = '1'
        else:
            cells[cur_i][cur_j] = '0'
    # End starting phase
    if key == Key.enter:
        starting = False
        listener.stop()
    
    # Exit program entirely
    if key == keyboard.Key.esc:
        exit()
    
    # Display grid
    if starting:
        display_grid()

# Function to get the number of alive neighbors of a cell given its coordinates
def countNeighbors(i_c,j_c):
    res = 0
    for x in [-1,0,1]:
        for y in [-1,0,1]:
            if 0 <= i_c+x < height and 0 <= j_c+y < length and (x,y) != (0,0): # In boundaries, excludes itself
                if cells[i_c+x][j_c+y] == '1':
                    res += 1
    return res

# Function to get the next generation from the current one
def next_gen(gen):
    new_gen = copy.deepcopy(gen)
    for i_c in range(height):
        for j_c in range(length):
            n = countNeighbors(i_c, j_c)
            if gen[i_c][j_c] == '1':
                if surv[n]:
                    new_gen[i_c][j_c] = '1'
                else:
                    new_gen[i_c][j_c] = '0'
            else:
                if born[n]:
                    new_gen[i_c][j_c] = '1'
                else:
                    new_gen[i_c][j_c] = '0'
    return new_gen
  
# Add the starting cells
display_grid()
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()

# Run the simulation
while True:
    display_grid()
    cells = next_gen(cells)
    time.sleep(0.5)