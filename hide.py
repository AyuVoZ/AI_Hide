import numpy as np
import gym
from gym import spaces
from stable_baselines3.common.env_checker import check_env
from stable_baselines3 import PPO, A2C, DQN # DQN coming soon	
from stable_baselines3.common.env_util import make_vec_env
import grid


class GoLeftEnv(gym.Env):
	"""
	Custom Environment that follows gym interface.
	This is a simple env where the agent must learn to hide from a turret. 
	"""
	# Because of google colab, we cannot implement the GUI ('human' render mode)
	metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}
	# Define constants for clearer code
	LEFT = 0
	RIGHT = 1
	UP = 2
	DOWN = 3

	def __init__(self, grid_size=12, render_mode=None):
		super(GoLeftEnv, self).__init__()

		self.grid_size = grid_size
		self.grid = grid.Grid(grid_size)

		self.agent_pos = self.grid.getAgentPos()

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

		assert render_mode is None or render_mode in self.metadata["render_modes"]
		self.render_mode = render_mode

	def reset(self):
		"""
		Important: the observation must be a numpy array
		:return: (np.array) 
		"""
		# Initialize the agent randomly and reset the number of steps
		del self.grid
		self.grid = grid.Grid(self.grid_size)
		self.nb_step = 0
		self.agent_pos = self.grid.getAgentPos()

		self.grid.show(self.render_mode, self.metadata["render_fps"])

		# here we convert to float32 to make it more general (in case we want to use continuous actions)
		return np.array(self.agent_pos, dtype=np.float32)

	def step(self, action):
		self.nb_step += 1
		# Check the position of the agent (if there is a wall or is out of bounds)
		next_pos, tmp_reward = self.check_pos_move(action)
		self.grid.setAgentPos(next_pos)
		self.agent_pos = self.grid.getAgentPos()

		# Is he hidded
		done = self.grid.isHide()
		# He gets a better reward if he finds it quick
		reward = tmp_reward if not done else 10/self.nb_step

		# Optionally we can pass additional info, we are not using that for now
		info = {}

		if self.render_mode == "human":
			self.grid.show(self.render_mode, self.metadata["render_fps"])

		return np.array(self.agent_pos, dtype=np.float32), reward, done, info

	def render(self, mode="human"):
		if self.render_mode == "rgb_array":
			return self.grid.show(self.render_mode, self.metadata["render_fps"])

	def check_pos_move(self, action):
		"""
			Return the future position of the agent if it not goes in walls or out of bounds
		"""
		future_pos = [self.grid.getAgentPos()[0], self.grid.getAgentPos()[1]]
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
			return self.agent_pos, -1

		if self.grid.isWall(future_pos[0], future_pos[1]):
			return self.agent_pos, -1
		elif self.grid.isTurret(future_pos[0], future_pos[1]):
			return self.agent_pos, -1
		else:
			return future_pos, 0
	
def main():
	# Instantiate the env
	env = GoLeftEnv(grid_size=20)
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
	model.save("Hidding")

	env = GoLeftEnv(grid_size=20, render_mode="human")
	model = PPO.load("Hidding", env=env)

	# Test the trained agent
	obs = env.reset()
	n_steps = 50
	for i in range(10):
		for step in range(n_steps):
			action, _ = model.predict(obs, deterministic=True)
			print("Step {}".format(step + 1))
			print("Action: ", action)
			obs, reward, done, info = env.step(action)
			print('obs=', obs, 'reward=', reward, 'done=', done)
			if done:
				# Note that the VecEnv resets automatically
				# when a done signal is encountered
				print("Goal reached!", "reward=", reward)
				break
		print("")
		print("=========================================")
		obs = env.reset()

if __name__ == '__main__':
	main()
