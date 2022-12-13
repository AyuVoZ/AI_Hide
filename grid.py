import numpy as np
import random
import math

class Grid():


    __VOID = 0
    __WALL = 1
    __TURRET = 2
    __PLAYER = 3


    
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



if __name__ == '__main__':
    grid = Grid(30)
    grid.show()
    grid.isHide()
    grid.show()
    

