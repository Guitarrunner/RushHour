path = "./problems/p17"
from cars import *

class Board:
    def __init__(self, rows=6, cols=6):
        self.rows=rows
        self.cols= cols
        self.grid=[]
        self.gridSpace(self.rows)
        self.level = 0
        self.vehicles = {}
        self.stage = []
        self.path = path

        with open(path,"r") as levelFile:
            for line in levelFile:
                block=[]
                for letter in line:
                    if letter.isdigit():
                        block.append(int(letter))
                    elif letter!='\n':
                        block.append(letter)
                self.stage.append(block)

         

    def gridSpace(self, size):
        for i in range(size):
            self.grid.append([0]*size)

    def putVehicles(self):
        self.clearGrid()
        self.vehicles = {}
        for vehicle in self.stage:
            self.addVehicle(Cars(vehicle[0],vehicle[1],vehicle[2],vehicle[3],False))
    
    def addVehicle(self,car):
        cPosX = car.x
        cPosY = car.y
        cDir = car.orientation
        cLen = car.length
        cID = car.id

        if cDir == "H":
            self.vehicles[cID] = car
            for i in range(cPosX,cPosX+cLen):
                self.grid[i][cPosY] = cID
        
        if cDir == "V":
            self.vehicles[cID] = car
            for i in range(cPosY,cPosY+cLen):
                self.grid[cPosX][i] = cID


    def clearGrid(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                self.grid[i][j]=0

    def print(self):
        step=0
        pivot=0
        while (step<len(self.grid)):
            print(self.grid[pivot][step], end = '')
            pivot=pivot +1
            if (pivot==len(self.grid[0])):
                pivot=0
                step = step+1
                print()

    def isPlaying(self, car):
        if car not in self.vehicles:
            return False
        else:
            return True

    def move(self,car, mov):
        if car not in self.vehicles:
            return False
        thisCar =self.vehicles[car]
        cPosX = thisCar.x
        cPosY = thisCar.y
        cDir = thisCar.orientation
        cLen = thisCar.length
        cID = thisCar.id

        changed = True

        if car == "X" and cPosX ==4:
            self.vehicles["X"].x = 6
            self.vehicles["X"].y = 2
            return True

        if cDir == "H":
            if cPosX + mov < 0 or cPosX + mov > self.cols - cLen or cPosY < 0 or cPosY > self.rows - 1:
                return False

            for i in range(cPosX + mov, cPosX+mov+cLen):
                if self.grid[i][cPosY] != 0:
                    if self.grid[i][cPosY] != cID:
                        changed = False
                        return False

            if changed:
                if mov > 0:
                    self.grid[cPosX][cPosY] = 0
                else:
                    self.grid[cPosX + cLen - 1][cPosY]=0
                self.vehicles[cID].x += mov
                cPosX = thisCar.x
                cPosY = thisCar.y

                for i in range(cPosX, cPosX + cLen):
                    self.grid[i][cPosY] = cID
                return True
        
        if cDir == "V":
            if cPosX < 0 or cPosX > self.cols - 1 or cPosY+mov < 0 or cPosY +mov> self.rows - cLen:
                return False

            for i in range(cPosY + mov, cPosY+mov+cLen):
                if self.grid[cPosX][i] != 0:
                    if self.grid[cPosX][i] != cID:
                        changed = False
                        return False

            if changed:
                if mov > 0:
                    self.grid[cPosX][cPosY] = 0
                else:
                    self.grid[cPosX][cPosY+ cLen - 1]=0
                self.vehicles[cID].y += mov
                cPosX = thisCar.x
                cPosY = thisCar.y
                self.grid[cPosX][cPosY - mov] = 0
                for i in range(cPosY, cPosY + cLen):
                    self.grid[cPosX][i] = cID
                return True
    
    def gameWon(self):
        carX = self.vehicles["X"]
        if carX.x >= 4 and carX.y == 2:
            self.vehicles["X"].x=6
            self.vehicles["X"].y=2
            return True
        else:
            return False


