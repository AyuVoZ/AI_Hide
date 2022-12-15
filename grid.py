import numpy as np
import random
import math

class Grid():


    __VOID = 0
    __WALL = 1
    __TURRET = 2
    __PLAYER = 3

    __LEFT = 0
    __RIGHT = 1
    __UP = 2
    __DOWN = 3


    
    def __init__(self, gridSize):
        self.__size = gridSize
        self.__generate()

    #procedural generation of the grid
    def __generate(self, nObstacles = 4, p = 0.05, nLenght = 10):
        self.__grid = np.zeros((self.__size, self.__size))
        self.__posTurret = [int(self.__size/2), int(self.__size/2)]
        
        #place random walls in the grid
        for i in range(nObstacles):
            pos = [random.randint(0, self.__size -1), random.randint(0, self.__size -1)]
            if(pos!= self.__posTurret):
                self.__grid[pos[0],pos[1]] = self.__WALL

        #generate random walls arround existing walls to form bigger structures
        for t in range(nLenght):
            grid_copy = self.__grid.copy()
            for i in range(0, self.__size):
                for j in range(0, self.__size):
                    
                    neighbor = grid_copy[max(0,i-1):min(i+2, self.__size+1),max(0,j-1):min(j+2, self.__size+1)]

                    if(self.__WALL in neighbor):
                        if(random.random()<=p):
                            self.__grid[i][j] = self.__WALL

        #place the turret in the center of the grid
        self.__grid[self.__posTurret[0], self.__posTurret[1]] = self.__TURRET

        #place the player randomly on the map
        correct = False
        while(not correct):
            self.__posAgent = [np.random.randint(0,self.__size-1), np.random.randint(0,self.__size-1)]
            if((self.__grid[self.__posAgent[0], self.__posAgent[1]]== self.__VOID) and not self.isHide()):
                correct = True

        self.__grid[self.__posAgent[0], self.__posAgent[1]] = self.__PLAYER

    #show the state of the grid in a terminal
    def show(self, mode='console'):
        if mode != 'console':
            return

        for j in range(self.__size):
            for i in range(self.__size):
                if(self.__grid[i,j]== self.__VOID):
                    print(".", end="")
                elif(self.__grid[i,j]== self.__WALL):
                    print("M", end="")
                elif(self.__grid[i,j]== self.__TURRET):
                    print("T", end="")
                elif(self.__grid[i,j]== self.__PLAYER):
                    print("X", end="")
            print("")
        print("\n")
       
    #return the size of the grid
    def size(self):
        return self.__size

    def isWall(self, x, y):
        return self.__grid[x,y] == self.__WALL

    def isHide(self):
        
        x = self.__posTurret[0]
        y = self.__posTurret[1]

        xa = self.__posAgent[0]
        ya = self.__posAgent[1]

        while(x!=xa or y!=ya):
            angle = int(((math.atan2(ya-y, xa-x)+math.pi/16)%math.pi)/(math.pi/8))%8
            signX = int(math.copysign(1, xa-x))
            signY = int(math.copysign(1, ya-y))

            if(angle == 0 ):
                nx, ny = 1,0
            elif(angle == 1 or angle == 7):
                nx, ny = 2,1
            elif(angle == 2 or angle == 6):
                nx, ny = 1,1
            elif(angle == 3 or angle == 5):
                nx, ny = 1,2
            else:
                nx, ny = 0,1
            
            for i in range(nx):
                x += signX
                if(self.__grid[x,y] == self.__WALL ):
                    return True
            for j in range(ny):
                y += signY
                if(self.__grid[x,y] == self.__WALL ):
                    return True
            
        return False


    #verify that the agent action is legal
    def validMove(self, x, y):

        #new position out of the grid
        if (x<0 or y<0 or x>self.__size or y>self.__size):
            return False
        
        #already an object at new position 
        if(self.__grid[x,y]!=self.__WALL):
            return False
        
        return True

    #move the agent according to the action 
    def move(self,action):
        #compute new coordinates
        x,y = self.__posAgent[0], self.__posAgent[1]
        if action == self.__LEFT:
            x-=1
        elif action == self.__RIGHT:
            x += 1
        elif action == self.__UP:
            y -= 1
        elif action == self.__DOWN:
            y += 1

        #assure new position is valid
        if(not self.validMove(x,y)):
            return

        #upfate position on the grid
        self.__grid[self.__posAgent[0],self.__posAgent[1]] = self.__WALL
        self.__grid[x,y] = self.__PLAYER
        self.__posAgent[0], self.__posAgent[1] = x,y  


if __name__ == '__main__':
    grid = Grid(30)
    grid.show()
    grid.isHide()
    grid.show()
    

