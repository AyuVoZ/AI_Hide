import numpy as np
import random

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


if __name__ == '__main__':
    grid = Grid(30)
    grid.show()
    

