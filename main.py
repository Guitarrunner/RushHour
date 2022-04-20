from curses import KEY_DOWN
from datetime import datetime
from tkinter import RIGHT
import pygame
from pygame.locals import *
from board import *
import sys
import time 
from astar import *

pygame.init()

width = 900
height= 800
stride_x  = 100
stride_y = 100
screen = pygame.display.set_mode((width,height)) 
bg_img = pygame.image.load("./img/board_img.jpg")
bg_img = pygame.transform.scale(bg_img, (width,height))
pygame.display.set_caption("Rush Hour")
font = pygame.font.SysFont("Roboto", 32)


def mainMenu():
    run=True
    click = False
    while run:
        screen.blit(bg_img, (0,0))
        exitButton = pygame.Rect(350,250,200,50)
        playButton = pygame.Rect(350,150,200,50)

        textQ = font.render("Quit", True, (249,249,249))
        textP = font.render("Play", True, (249,249,249))

        mx,my = pygame.mouse.get_pos()

        if exitButton.collidepoint((mx,my)):
            if click:
                run=False
        
        if playButton.collidepoint((mx,my)):
            if click:
                setGame()
        
        pygame.draw.rect(screen, (255, 159, 28), exitButton)
        pygame.draw.rect(screen, (255, 159, 28), playButton)
        screen.blit(textP,(425,155))
        screen.blit(textQ,(425,255))
                
        for event in pygame.event.get():
            if event.type == QUIT:
                run = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click=True 

        pygame.display.update()  

def setGame():
    run=True
    click = False
    level = ''
    ownLevel = ''
    activeLevel= False
    activeOwnLevel = False
    while run:
        screen.blit(bg_img, (0,0))
        selectLevel = pygame.Rect(200, 300, 200, 50)
        putLevel = pygame.Rect(600,300, 200, 200)
        playLevel = pygame.Rect(200,400,200,50)
        playOwn = pygame.Rect(590,550,240,50)

        textL = font.render("Pick Level", True, (249,249,249))
        textO = font.render("Write your own", True, (249,249,249))
        levelText = font.render(level, True, (0,0,0))
        ownLevelText = font.render(ownLevel, True, (0,0,0))

        mx,my = pygame.mouse.get_pos()

        if playLevel.collidepoint((mx,my)):
            if click:
                click=False
                try:
                    if 0<int(level)<41:
                        game(level)
                    else:
                        level=''
                        error = font.render("Choose a level between 1 and 40", True, (255,0,0))
                        screen.blit(error,(250,500))
                        pygame.display.update()  
                        time.sleep(1)
                except:
                    level=''
                    error = font.render("Choose a level between 1 and 40", True, (255,0,0))
                    screen.blit(error,(250,500))
                    pygame.display.update()  
                    time.sleep(1)

        
                    
        
        if playOwn.collidepoint((mx,my)):
            if click:
                click=False
                try:
                    file = open("./problems/p0","w")
                    file.write(ownLevel)
                    file.close()
                    board = Board("0")
                    board.putVehicles()
                    game("0")
                except:
                    ownLevel=''
                    error = font.render("Wrong composition", True, (255,0,0))
                    screen.blit(error,(350,500))
                    pygame.display.update()  
                    time.sleep(1)

        
        pygame.draw.rect(screen, (255, 255, 255), selectLevel)
        pygame.draw.rect(screen, (255, 255, 255), putLevel)
        pygame.draw.rect(screen, (255, 159, 28), playOwn)
        pygame.draw.rect(screen, (255, 159, 28), playLevel)
        screen.blit(textO,(605,560))
        screen.blit(textL,(230,405))
        screen.blit(levelText,(200,300))
        screen.blit(ownLevelText,(600,300))
        for event in pygame.event.get():
            if event.type == QUIT:
                run = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click=True 
                if selectLevel.collidepoint(event.pos):
                    activeLevel= True
                    activeOwnLevel=False
                if putLevel.collidepoint(event.pos):
                    activeOwnLevel= True
                    activeLevel= False
            elif event.type == pygame.KEYDOWN:
                if activeLevel:
                    if event.key == K_RETURN:
                        pass
                    elif event.key == K_BACKSPACE:
                        level = level[:-1]
                    else:
                        level += event.unicode
                if activeOwnLevel:
                    if event.key == K_BACKSPACE:
                        ownLevel = ownLevel[:-1]
                    else:
                        ownLevel += event.unicode

        pygame.display.update()  

def game(problem):
    board = Board(problem)
    board.putVehicles()
    won = False
    car=""
    playing = True
    filename = board.path
    with open(filename) as rushhour_file:
        rushhour = load_file(rushhour_file)

    #
    h4 = DistanceFromTargetToExit()
    aStar = AStar(h4)
    
    start_time = datetime.now()
    sol = aStar.aStar(rushhour)
    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))
    #print(sol['Solution'],"\n steps", sol['Steps'],'\n ',sol['Expanded Nodes'])
    for solutions in sol['Solution']:
        print(solutions.lastmove)
    #
    #results = breadth_first_search(rushhour, max_depth=100)

    #print ('{0} Solutions found'.format(len(results['solutions'])))
    #for solution in results['solutions']:
        #print ('Solution: {0}'.format(', '.join(solution_steps(solution))))

    #print ('{0} Nodes visited'.format(len(results['visited'])))


    while playing:
        
        for event in pygame.event.get():
            if event.type == QUIT:
                playing = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if not won:
                    if event.key == K_ESCAPE:
                        setGame()
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
                        for solution in sol['Solution']:
                            steps = solution.lastmove
                            if len(steps)!=0:
                                car = steps[0]
                            else:
                                steps="ZZ"
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
            time.sleep(2)
            mainMenu()
mainMenu()