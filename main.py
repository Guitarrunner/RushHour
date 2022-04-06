from curses import KEY_DOWN
from tkinter import RIGHT
import pygame
from pygame.locals import *
from board import *
import sys
import time 
from algorithm import *

pygame.init()

board = Board()
board.putVehicles()

width = 900
height= 800
stride_x  = 100
stride_y = 100
screen = pygame.display.set_mode((width,height)) 
bg_img = pygame.image.load("./img/board_img.jpg")
bg_img = pygame.transform.scale(bg_img, (width,height))
pygame.display.set_caption("Rush Hour")
font = pygame.font.SysFont("Roboto", 32)
won = False
car=""
playing = True
filename = board.path
with open(filename) as rushhour_file:
    rushhour = load_file(rushhour_file)

results = breadth_first_search(rushhour, max_depth=100)

print ('{0} Solutions found'.format(len(results['solutions'])))
for solution in results['solutions']:
    print ('Solution: {0}'.format(', '.join(solution_steps(solution))))

print ('{0} Nodes visited'.format(len(results['visited'])))


while playing:
    
    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        elif event.type == pygame.KEYDOWN:
            if not won:
                if event.key == K_a:
                    car = "A"
                elif event.key == K_b:
                    car = "B"
                elif event.key == K_c:
                    car = "C"
                elif event.key == K_d:
                    car = "D"
                elif event.key == K_e:
                    car = "E"
                elif event.key == K_f:
                    car = "F"
                elif event.key == K_g:
                    car = "G"
                elif event.key == K_h:
                    car = "H"
                elif event.key == K_i:
                    car = "I"
                elif event.key == K_j:
                    car = "J"
                elif event.key == K_k:
                    car = "K"
                elif event.key == K_o:
                    car = "O"
                elif event.key == K_p:
                    car = "P"
                elif event.key == K_q:
                    car = "Q"
                elif event.key == K_r:
                    car = "R"
                elif event.key == K_x:
                    car = "X"
                elif event.key == K_8:
                    for solution in results['solutions']:
                        solution1=solution_steps(solution)
                    for steps in solution1:
                        car = steps[0]
                        if steps[1]=="L" or steps[1]=="U":
                            board.move(car, -1)
                            screen.blit(bg_img, (0,0))
                            for v in board.vehicles:
                                curr_v = board.vehicles[v]
                                screen.blit(curr_v.image, (curr_v.x * stride_x + 100  , curr_v.y * stride_y + 100))    

                            for v in board.vehicles:
                                selectedCar = board.vehicles[v]

                            pygame.display.update() 
                            time.sleep(1)
                        else:
                            board.move(car, 1)
                            screen.blit(bg_img, (0,0))
                            for v in board.vehicles:
                                curr_v = board.vehicles[v]
                                screen.blit(curr_v.image, (curr_v.x * stride_x + 100  , curr_v.y * stride_y + 100))    

                            for v in board.vehicles:
                                selectedCar = board.vehicles[v]

                            pygame.display.update() 
                            time.sleep(1)
                
                elif event.key == pygame.K_LEFT:
                    if board.isPlaying(car):
                        if board.vehicles[car].orientation == "H":
                            if board.move(car, -1):
                                #board.print()
                                print()
                elif event.key == pygame.K_RIGHT:
                    if board.isPlaying(car):
                        if board.vehicles[car].orientation == "H":
                            if board.move(car, 1):
                                #board.print()
                                print()
                elif event.key == pygame.K_UP:
                    if board.isPlaying(car):
                        if board.vehicles[car].orientation == "V":
                            if board.move(car, -1):
                                #board.print()
                                print()
                elif event.key == pygame.K_DOWN:
                    if board.isPlaying(car):
                        if board.vehicles[car].orientation == "V":
                            if board.move(car, 1):
                                #board.print()
                                print()
    screen.blit(bg_img, (0,0))
    for v in board.vehicles:
        curr_v = board.vehicles[v]
        screen.blit(curr_v.image, (curr_v.x * stride_x + 100  , curr_v.y * stride_y + 100))    

    for v in board.vehicles:
        selectedCar = board.vehicles[v]

    pygame.display.update()   

    if not won:
        won = board.gameWon()

    if won:
        print("won")
        break
  
pygame.quit()