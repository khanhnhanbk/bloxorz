#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import time
import random

from model.control import Control
from model.map import maps
from drawing.display import Display
from drawing.box import Box
from model.box import Box as cube
import pygame
from copy import deepcopy

def print_stack(stack, algorithm):
    if algorithm=="dfs":
        print("STACK: ")
        for state in stack[::-1]:
            print("( %s ) " % state[0])
    elif algorithm=="bfs":
        print("QUEUE: ")
        for state in stack:
            print("( %s ) " % state[0])

def dfs(state: Control):
    while state.stack:
        current_state = state.stack.pop()
        current_maps = state.stack_maps.pop()
        state.visited.append((current_state, current_maps))
        for move in state.moves:
            state.set_state(current_state, current_maps)
            if move():
                if state.check_goal():
                    return

def dfs_recursion(state: Control):
    if state.check_goal():
        return
    current_state = state.stack.pop()
    current_maps = state.stack_maps.pop()
    state.visited.append((current_state, current_maps))
    for move in state.moves:
        state.set_state(current_state, current_maps)
        if move():
            dfs_recursion(state)

def bfs(state: Control):
    while state.stack:
        current_state = state.stack.pop(0)
        current_maps = state.stack_maps.pop(0)
        state.visited.append((current_state, current_maps))
        for move in state.moves:
            state.set_state(current_state, current_maps)
            if move():
                if state.check_goal():
                    return

def dfs_step_by_step(state: Control, timesleep=0.1):
    pygame.init()
    display = Display(title='Bloxorz Game', map_size=(state.size[0], state.size[1]))

    while state.stack:
        current_state, current_maps = state.stack.pop()
        
        print("POP: ( %s )" % current_state)
        
        state.visited.append((current_state, current_maps))

        for move in state.moves:
            state.set_state(current_state, current_maps)

            print_stack(state.stack, "dfs")
            state.maps.print_current()
            state.draw_box()
            state.draw_maps()
            display.update()
            time.sleep(timesleep)
            os.system("clear")

            if move():
                print_stack(state.stack, "dfs")
                state.maps.print_current()
                time.sleep(timesleep)
                os.system("clear")
                if state.check_goal():
                    print("WINNER!")
                    state.maps.print_current()
                    state.draw_box()
                    state.draw_maps()
                    display.update()
                    time.sleep(timesleep)
                    return state
        os.system("clear")
        

def bfs_step_by_step(state: Control, timesleep=0.2):
    pygame.init()
    display = Display(title='Bloxorz Game', map_size=(state.size[0], state.size[1]))

    while state.stack:
        current_state, current_maps = state.stack.pop(0)

        print("POP: ( %s )" % current_state)

        state.visited.append((current_state, current_maps))

        for move in state.moves:
            state.set_state(current_state, current_maps)

            print_stack(state.stack, "bfs")
            state.maps.print_current()
            state.draw_box()
            state.draw_maps()
            display.update()
            time.sleep(timesleep)
            os.system("clear")

            if move():
                print_stack(state.stack, "bfs")
                state.maps.print_current()
                time.sleep(timesleep)
                os.system("clear")
                if state.check_goal():
                    print("WINNER!")
                    state.maps.print_current()
                    state.draw_box()
                    state.draw_maps()
                    display.update()
                    time.sleep(timesleep)
                    return state
                    
            os.system("clear")

def dfs_path(state: Control):
    stack = [[state.start], ]
    while state.stack:
        current_state, current_maps = state.stack.pop()
        path = stack.pop()
        state.visited.append((current_state, current_maps))
        for move in state.moves:
            state.set_state(current_state, current_maps)
            if move():
                if state.check_goal():
                    result = path + [state.current]
                    return result 
                stack.append(path + [state.current])
                
    return None

def bfs_path(state: Control):
    stack = [[state.start], ]
    while state.stack:
        current_state, current_maps = state.stack.pop(0)
        path = stack.pop(0)
        state.visited.append((current_state, current_maps))
        for move in state.moves:
            state.set_state(current_state, current_maps)
            if move():
                if state.check_goal():
                    result = path + [state.current]
                    return result
                stack.append(path + [state.current])
                
    return None

    
def hill_climbing(state: Control):
    state.eval_func()
    print("Eval_Maps")
    print(state.eval_maps)
    count = 0
    path = [] 
    all_accept_state = []
    best_state = []

    while True:
        current_state = state.get_state()
        current_maps = state.get_maps()
        current_eval = state.evaluate()

        path.append(current_state)
        accept_state = []

        state.visited.append((current_state, current_maps))

        for move in state.moves:
            if move():
                delta = state.evaluate()
                if delta <= current_eval:
                    better_state = state.get_state()
                    get_maps = state.get_maps()
                    accept_state.append((delta, better_state, get_maps))
                
            state.set_state(current_state, current_maps)
                  
        if accept_state != []:
            next_eval, next_state, next_maps = min(accept_state)
            best_state.append(next_state)
            all_accept_state.extend(sorted(accept_state))

            if next_state == state.end:
                path.append(next_state)
                return path

            state.set_state(next_state, next_maps)
        else: 
            try:
                count +=1
                print("Try again!", count)
                print(path)
                while True:
                    next_eval, next_state, next_maps = all_accept_state.pop()
                    if next_state in best_state:
                        path.pop()
                        continue
                    else:
                        path.pop()
                        state.set_state(next_state, next_maps)
                    break
            except:
                return None
                



def handle(state: Control, map_size= (0,0)):
    state.Play_handle = True
    pygame.init()
    display = Display(title='Bloxorz Game', map_size=map_size)
    result = True
    print("Press Space Key to Exit!")
    while True:
        # os.system("clear")
        for event in pygame.event.get():
            if state.Play_handle:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                    result = state.move_up()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                    result = state.move_down()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                    result = state.move_right()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                    result = state.move_left()
                
            if display.quit(event):
                return
        state.draw_maps()
        state.draw_box()
        # state.print_maps()
        display.update()

        if state.check_goal():
            print("WINNER!")
            return
        if result == False:
            print("LOSER!")
            return