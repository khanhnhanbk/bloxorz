#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Run"""
import pygame
import sys
import os
import time
from model.solver import dfs_path, bfs_path, handle, hill_climbing, dfs_step_by_step, bfs_step_by_step
from model.geneticAlgorism import geneticAlgorism
from drawing.display import Display
from model.map import maps
from model.control import Control

class Algorithm:
    DFS = 1
    BFS = 2
    HILL= 3
    GA = 4

class Level:
    lv1  = "./level/1.json"
    lv2 = "./level/2.json"
    lv3 = "./level/3.json"
    lv4 = "./level/4.json"
    lv5 = "./level/5.json"
    lv6 = "./level/6.json"
    lv7 = "./level/7.json"
    lv8 = "./level/8.json"
    lv9 = "./level/9.json"
    lv10 = "./level/10.json"
    lv11 = "./level/11.json"
    lv12 = "./level/12.json"
    lv13 = "./level/13.json"
    lv14 = "./level/14.json"
    lv15 = "./level/15.json"
    
def deltatime(start_time):
    result = time.time() - start_time
    print("Time: ", result)

def flatMap(path):
    return [y for x in path for y in x]

def draw_path_3D(solution, timesleep=0.5, level=Level.lv1, map_size = (0,0)):
    pygame.init()
    display = Display(title='Bloxorz Game', map_size=map_size)
    if solution != None:
        print("Success!")
        print("Step: %d" % len(solution))
        print(solution)
        choiselv = maps(level)

        level = Control(choiselv)
        level.draw_StartBox()
        level.draw_StartMaps()
        display.update() 

        for path in solution:
            time.sleep(timesleep)
            level.current = path
            level.update_box_locaton_for_maps(path)
            
            if level.maps.refreshBox():
                level.update_current_location()
            else: 
                print("Solution Fail!")
                return

            level.draw_box() 
            level.draw_maps()   
            display.update()
        return
    else:
        print("Unable to find path for maps!")
        print("Dir Level: %s" % level)
        return

def draw_path_2D(solution, timesleep=0.5, level=Level.lv1):
    if solution != None:
        print("Success!")
        print("Step: %d" % len(solution))
        print(solution)
        choiselv = maps(level)

        level = Control(choiselv)
        level.print_maps()
        
        time.sleep(timesleep)

        for path in solution:
            os.system("clear")
            level.current = path
            level.update_box_locaton_for_maps(path)
            level.maps.refreshBox()

            if level.maps.refreshBox():
                level.update_current_location()
            else: 
                print("Solution Fail!")
                return

            level.print_maps()
            time.sleep(timesleep)
        return
    else:
        print("Unable to find path for maps!")
        print("Dir Level: %s" % level)
        return
    
def main(level=Level.lv1, Play_handle=True, algorithm=Algorithm.DFS, view='3'):
    print("Processing...")
    Maps = maps(level)
    size = Maps.size
    state = Control(Maps)
   
    if Play_handle:
        state.Play_handle = Play_handle
        handle(state, map_size=(size[0], size[1]))
    else:
        Start_Time = time.time()
        if algorithm == Algorithm.DFS:
            if view == '1':
                dfs_step_by_step(state)
            elif view == '2':
                result = dfs_path(state)
                deltatime(Start_Time)   
                draw_path_2D(result, level=level)
            elif view == '3':
                result = dfs_path(state)
                deltatime(Start_Time)
                draw_path_3D(result, level=level, map_size=(size[0], size[1]))
        elif algorithm == Algorithm.BFS:
            if view == '1':
                bfs_step_by_step(state)
            elif view == '2':
                result = bfs_path(state)
                deltatime(Start_Time)   
                draw_path_2D(result, level=level)
            elif view == '3':
                result = bfs_path(state)
                deltatime(Start_Time)
                draw_path_3D(result, level=level, map_size=(size[0], size[1]))
        elif algorithm == Algorithm.HILL:
            if view == '1':
                print("Hill Climbing do not support to View Step By Step !")
                return
            elif view == '2':
                result = hill_climbing(state)
                deltatime(Start_Time)   
                draw_path_2D(result, level=level)
            elif view == '3':
                result = hill_climbing(state)
                deltatime(Start_Time)
                draw_path_3D(result, level=level, map_size=(size[0], size[1]))
        elif algorithm == Algorithm.GA:
            if view == '1':
                print("GA do not support to View Step By Step !")
                return
            elif view == '2':
                result = geneticAlgorism(state)
                deltatime(Start_Time)   
                draw_path_2D(result, level=level)
            elif view == '3':
                result = geneticAlgorism(state)
                # print (result)
                deltatime(Start_Time)
                draw_path_3D(result, level=level, map_size=(size[0], size[1]))
    time.sleep(1)
    sys.exit()

if __name__=="__main__":
    # main(level="./level/1.json", Play_handle=False, algorithm=Algorithm.GA, view=3)
    if len(sys.argv) > 2:
        level = sys.argv[1]
        option = sys.argv[2]
        if option != "handle":
            view = sys.argv[3]
        if option == "handle": 
            main(level=level, Play_handle=True, algorithm=Algorithm.HILL)
        elif option == "dfs":
            main(level=level, Play_handle=False, algorithm=Algorithm.DFS, view=view)
        elif option == "bfs":
            main(level=level, Play_handle=False, algorithm=Algorithm.BFS, view=view)
        elif option == "hill":
            main(level=level, Play_handle=False, algorithm=Algorithm.HILL, view=view)
        elif option == "GA":
            main(level=level, Play_handle=False, algorithm=Algorithm.GA, view=view)
        else: 
            print("Error! Please read file README.md for more details. thanks")
    else:
        # Edit here
        main(level=Level.lv1, Play_handle=False, algorithm=Algorithm.GA, view='3')