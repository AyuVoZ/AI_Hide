import numpy as np
import gym
from gym import spaces
from stable_baselines3.common.env_checker import check_env
from stable_baselines3 import PPO, A2C, DQN # DQN coming soon	
from stable_baselines3.common.env_util import make_vec_env


class GoLeftEnv(gym.Env):
	"""
	Custom Environment that follows gym interface.
	This is a simple env where the agent must learn to hide from a turret. 
	"""
	# Because of google colab, we cannot implement the GUI ('human' render mode)
	metadata = {'render.modes': ['console']}
	# Define constants for clearer code
	LEFT = 0
	RIGHT = 1
	UP = 2
	DOWN = 3

	def __init__(self, grid_size=12):
		super(GoLeftEnv, self).__init__()

		# Size of the grid
		self.grid_size = grid_size
		# Initialize the agent randomly
		self.agent_pos = self.rand_agent_pos()

		# Define action and observation space
		# They must be gym.spaces objects
		# Here we have 4 actions left, right up, down
		n_actions = 4
		self.action_space = spaces.Discrete(n_actions)
		# The observation will be the coordinate of the agent
		# this can be described both by Discrete and Box space
		self.observation_space = spaces.Box(low=0, high=self.grid_size,
											shape=(2,), dtype=np.float32)
		self.nb_step = 0

	def reset(self):
		"""
		Important: the observation must be a numpy array
		:return: (np.array) 
		"""
		# Initialize the agent randomly and reset the number of steps
		self.agent_pos = self.rand_agent_pos()
		self.nb_step = 0
		# here we convert to float32 to make it more general (in case we want to use continuous actions)
		return np.array(self.agent_pos, dtype=np.float32)

	def step(self, action):
		self.nb_step += 1
		# Check the position of the agent (if there is a wall or is out of bounds)
		self.agent_pos = self.check_pos_move(action)

		# Is he hidded
		done = self.is_Finished()
		# He gets a better reward if he finds it quick
		reward = 0 if not done else 10/self.nb_step

		# Optionally we can pass additional info, we are not using that for now
		info = {}

		return np.array(self.agent_pos, dtype=np.float32), reward, done, info

	def render(self, mode='console'):
		if mode != 'console':
			raise NotImplementedError()
		# agent is represented as a cross, the walls as a M and the rest as a dot
		for i in range(self.grid_size):
			for j in range(self.grid_size):
				if self.agent_pos[1]==i:
					if self.is_Wall([j,i]):
						print("M", end="")
					elif self.agent_pos[0]==j:
						print("x", end="")
					else:
						print(".", end="")
				else:
					if self.is_Wall([j,i]):
						print("M", end="")
					else:
						print(".", end="")
			print("")

	def rand_agent_pos(self):
		"""
			Randomize the postion of the agent so it's not in walls and not already hidded
		"""
		agent_x = np.random.randint(0,self.grid_size-1,1)
		agent_y = np.random.randint(0,self.grid_size-1,1)
		grid = self.grid_size
		while agent_x<=4 and (agent_y <=4 or agent_y >= grid-4) or agent_x <=3 and agent_y >= grid-5 or agent_x >= grid-4 and (agent_y<=4 or agent_y >= grid-4) or agent_x==6 and agent_y==6:
			agent_x = np.random.randint(0,self.grid_size-1,1)
			agent_y = np.random.randint(0,self.grid_size-1,1)
		return [agent_x[0], agent_y[0]]

	def check_pos_move(self, action):
		"""
			Return the future position of the agent if it not goes in walls or out of bounds
		"""
		future_pos = [self.agent_pos[0], self.agent_pos[1]]
		if action == self.LEFT:
			future_pos[0] -= 1
		elif action == self.RIGHT:
			future_pos[0] += 1
		elif action == self.UP:
			future_pos[1] -= 1
		elif action == self.DOWN:
			future_pos[1] += 1

		# Check the bounds of the map
		if future_pos[0]<0 or future_pos[0]>=self.grid_size or future_pos[1]<0 or future_pos[1]>=self.grid_size:
			return self.agent_pos

		if self.is_Wall(future_pos):
			return self.agent_pos
		else:
			return future_pos

	def is_Wall(self, pos):
		"""
			Return a boolean to see if the position is in walls
		"""
		if (pos[0]>=2 and pos[0]<=4 and pos[1]>=2 and pos[1]<=4) or (pos[0]==2 and pos[1]==1):
			return True
		elif (pos[0]>=2 and pos[0]<=4 and pos[1]>=8 and pos[1]<=9) or (pos[0]==4 and pos[1]==10) or (pos[0]==3 and pos[1]==7):
			return True
		elif (pos[0]>=8 and pos[0]<=9 and pos[1]>=8 and pos[1]<=10) or (pos[0]==10 and pos[1]==8):
			return True
		elif (pos[0]>=8 and pos[0]<=10 and pos[1]>=2 and pos[1]<=3) or (pos[0]==8 and pos[1]==1) or (pos[1]==4 and pos[0]>=8 and pos[0]<=9):
			return True
		else:
			return False

	def is_Finished(self):
		"""
			Return a boolean to see if the agent is hidded
		"""
		agent_x = self.agent_pos[0]
		agent_y = self.agent_pos[1]
		if (agent_x<=4 and (agent_y <=4 or agent_y >= 8)) or (agent_x <=3 and agent_y >= 7) or (agent_x >= 8 and (agent_y<=4 or agent_y >= 8)):
			if not self.is_Wall(self.agent_pos):
				return True
		return False
	
def main():
	# Instantiate the env
	env = GoLeftEnv(grid_size=12)
	# If the environment don't follow the interface, an error will be thrown
	check_env(env, warn=True)

	# Here we can try the environement by sending actions to move the player
	# obs = env.reset()
	# env.render()

	# print(env.observation_space)
	# print(env.action_space)
	# print(env.action_space.sample())

	# n_steps = 100
	# for step in range(n_steps):
	# 	print("Step {}".format(step + 1))
	# 	move = int(input("Direction"))
	# 	obs, reward, done, info = env.step(move)
	# 	print('obs=', obs, 'reward=', reward, 'done=', done)
	# 	env.render()
	# 	if done:
	# 		print("Goal reached!", "reward=", reward)
	# 		break


	# We vectorize the environement, choose a model and make it learn how to hide
	env = make_vec_env(lambda: env, n_envs=1)
	model = PPO('MlpPolicy', env, verbose=1, batch_size=256, n_epochs=50, n_steps=4096).learn(100000, progress_bar=True)

	# Test the trained agent
	obs = env.reset()
	n_steps = 10
	for i in range(10):
		for step in range(n_steps):
			action, _ = model.predict(obs, deterministic=True)
			print("Step {}".format(step + 1))
			print("Action: ", action)
			obs, reward, done, info = env.step(action)
			print('obs=', obs, 'reward=', reward, 'done=', done)
			if not done:
				env.render(mode='console')
			else:
				# Note that the VecEnv resets automatically
				# when a done signal is encountered
				print("Goal reached!", "reward=", reward)
				break
		obs = env.reset()
		print("")
		print("=========================================")
		input("Press ENTER to view another trained agent")
		
if __name__ == '__main__':
	main()
