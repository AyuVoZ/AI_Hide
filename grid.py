import numpy as np
import random
import math
import pygame
import time

class Grid():


	__VOID = 0
	__WALL = 1
	__TURRET = 2
	__PLAYER = 3

	__LEFT = 0
	__RIGHT = 1
	__UP = 2
	__DOWN = 3

	__NORTH = 0
	__NORTH_EAST = 1
	__EAST = 2
	__SOUTH_EAST = 3
	__SOUTH = 4
	__SOUTH_WEST = 5
	__WEST = 6
	__NORTH_WEST = 7


	
	def __init__(self, gridSize):
		self.__size = gridSize
		self.__generate()

		self.__window_size = 700

		self.window = None
		self.clock = None

	#procedural generation of the grid
	def __generate(self, nObstacles = 7, p = 0.05, nLenght = 12):
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
		self.placeAgentRandom()


		
	def placeAgentRandom(self, reset = False):

		#if the agent was previously instantiated we remove it before creating another one
		if(reset):
			self.__grid[self.__posAgent[0], self.__posAgent[1]] = self.__VOID

		correct = False
		while(not correct):
			self.__posAgent = [np.random.randint(0,self.__size-1), np.random.randint(0,self.__size-1)]
			if((self.__grid[self.__posAgent[0], self.__posAgent[1]]== self.__VOID) and not self.isHide()):
				correct = True

		self.__grid[self.__posAgent[0], self.__posAgent[1]] = self.__PLAYER

	#show the state of the grid in a terminal
	def show(self, mode='human', fps=3):
		if self.window is None and mode == "human":
			pygame.init()
			pygame.display.init()
			self.window = pygame.display.set_mode((self.__window_size, self.__window_size))
		if self.clock is None and mode == "human":
			self.clock = pygame.time.Clock()

		canvas = pygame.Surface((self.__window_size, self.__window_size))
		canvas.fill((255, 255, 255))
		pix_square_size = (
			self.__window_size / self.__size
		)

		for j in range(self.__size):
			for i in range(self.__size):
				if(self.__grid[i,j]== self.__VOID):
					pass
				elif(self.__grid[i,j]== self.__WALL):
					pygame.draw.rect(canvas,(0, 0, 0),pygame.Rect([j*pix_square_size,i*pix_square_size],(pix_square_size, pix_square_size),),)
				elif(self.__grid[i,j]== self.__TURRET):
					pygame.draw.circle(canvas,(255, 0, 0),[(j + 0.5) * pix_square_size,(i + 0.5) * pix_square_size],pix_square_size / 3,)
				elif(self.__grid[i,j]== self.__PLAYER):
					pygame.draw.circle(canvas,(0, 0, 255),[(j + 0.5) * pix_square_size,(i + 0.5) * pix_square_size],pix_square_size / 3,)
		
		# Finally, add some gridlines
		for x in range(self.__size + 1):
			pygame.draw.line(
				canvas,
				0,
				(0, pix_square_size * x),
				(self.__window_size, pix_square_size * x),
				width=3,
			)
			pygame.draw.line(
				canvas,
				0,
				(pix_square_size * x, 0),
				(pix_square_size * x, self.__window_size),
				width=3,
			)

		if mode == "human":
			# The following line copies our drawings from `canvas` to the visible window
			self.window.blit(canvas, canvas.get_rect())
			pygame.event.pump()
			pygame.display.update()

			# We need to ensure that human-rendering occurs at the predefined framerate.
			# The following line will automatically add a delay to keep the framerate stable.
			self.clock.tick(fps)
		else:  # rgb_array
			return np.transpose(
				np.array(pygame.surfarray.pixels3d(canvas)), axes=(1, 0, 2)
			)

	#return the size of the grid
	def size(self):
		return self.__size

	def isWall(self, x, y):
		return self.__grid[x,y] == self.__WALL

	def isTurret(self, x, y):
		return self.__grid[x,y] == self.__TURRET

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
		if (x<0 or y<0 or x>=self.__size or y>=self.__size):
			return False
		
		#already an object at new position 
		if(self.__grid[x,y]==self.__WALL or self.__grid[x,y]==self.__TURRET ):
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
			return -2

		#upfate position on the grid
		self.__grid[self.__posAgent[0],self.__posAgent[1]] = self.__VOID
		self.__grid[x,y] = self.__PLAYER
		self.__posAgent[0], self.__posAgent[1] = x,y  

		return 0

	def getPosAgent(self):
		return self.__posAgent
		

	#return the values of the virtual sensors of the robot
	def getSensors(self):
		nLenght = 10
		nDir = 8
		sensors = np.zeros(nDir, dtype=np.float32)

		x,y = self.getPosAgent()

		#for each direction
		for i in range(nDir):
			for j in range(1, nLenght+1):
				sensors[i] = j
				if (i== self.__NORTH):
					if(y-j<0):
						break
					if(self.__grid[x,y-j]!=self.__VOID):
						break
				elif (i==self.__NORTH_EAST):
					if(y-j<0 or x+j>=self.__size):
						break
					if(self.__grid[x+j,y-j]!=self.__VOID):
						break
				elif (i==self.__EAST):
					if(x+j>=self.__size):
						break
					if(self.__grid[x+j,y]!=self.__VOID):
						break	
				elif (i==self.__SOUTH_EAST):
					if(y+j>=self.__size or x+j>=self.__size):
						break
					if(self.__grid[x+j,y+j]!=self.__VOID):
						break
				elif (i==self.__SOUTH):
					if(y+j>=self.__size):
						break
					if(self.__grid[x,y+j]!=self.__VOID):
						break
				elif (i==self.__SOUTH_WEST):
					if(y+j>=self.__size or x-j<0):
						break
					if(self.__grid[x-j,y+j]!=self.__VOID):
						break
				elif (i==self.__WEST):
					if(x-j<0):
						break
					if(self.__grid[x-j,y]!=self.__VOID):
						break
				elif (i==self.__NORTH_WEST):
					if(y-j<0 or x-j<0):
						break
					if(self.__grid[x-j,y-j]!=self.__VOID):
						break
				if(j==nLenght):
					sensors[i]=0

		return sensors
		

if __name__ == '__main__':
	grid = Grid(20)
	print(grid.getSensors())
	grid.show()
	time.sleep(50000)
	grid.isHide()
	print(grid.getPosAgent())

	grid.getSensors()
 


	

