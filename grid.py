import numpy as np
import random
import math
import pygame

class Grid():


	__VOID = 0
	__WALL = 1
	__TURRET = 2
	__PLAYER = 3


	
	def __init__(self, gridSize):
		self.__size = gridSize
		self.__generate()

		self.__window_size = 700

		self.window = None
		self.clock = None

	#procedural generation of the grid
	def __generate(self, nObstacles = 6, p = 0.05, nLenght = 10):
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
	   
	def getAgentPos(self):
		return self.__posAgent

	def setAgentPos(self, future_pos):
		tmp_agent_pos = self.__posAgent
		self.__posAgent = future_pos
		self.__grid[tmp_agent_pos[0], tmp_agent_pos[1]] = self.__VOID
		self.__grid[future_pos[0], future_pos[1]] = self.__PLAYER

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



if __name__ == '__main__':
	grid = Grid(20)
	grid.show()
	grid.isHide()
	grid.show()

	while True:
		grid.show()
	

