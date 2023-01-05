import numpy as np
import gym
from gym import spaces
from stable_baselines3.common.env_checker import check_env
from stable_baselines3 import DQN
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

	def __init__(self, grid_size=12, render_mode=None, sameMap=True):
		super(GoLeftEnv, self).__init__()

		self.grid_size = grid_size
		self.grid = grid.Grid(grid_size)
		self.sameMap = sameMap

		self.agent_pos = self.grid.getPosAgent()

		# Define action and observation space
		# They must be gym.spaces objects
		# Here we have 4 actions left, right up, down
		n_actions = 4
		self.action_space = spaces.Discrete(n_actions)
		# The observation will be the coordinate of the agent
		# this can be described both by Discrete and Box space
		self.observation_space = spaces.Box(0, 10, shape=(9,), dtype=np.float32)
		self.nb_step = 0

		assert render_mode is None or render_mode in self.metadata["render_modes"]
		self.render_mode = render_mode

	# def _get_obs(self):
	# 	return {"agent": self.agent_pos, "sensors": self.sensors}

	def reset(self):
		"""
		Important: the observation must be a numpy array
		:return: (np.array) 
		"""
		# Initialize the agent randomly and reset the number of steps
		if(self.sameMap):
			self.grid.placeAgentRandom(reset=True)
		else:
			del self.grid
			self.grid = grid.Grid(self.grid_size)
		
		self.nb_step = 0
		#self.agent_pos = np.array(self.grid.getPosAgent(), dtype=np.float32)
		self.sensors = np.array(self.grid.getSensors(), dtype=np.float32)

		self.grid.show(self.render_mode, self.metadata["render_fps"])

		# here we convert to float32 to make it more general (in case we want to use continuous actions)
		#return self.grid.getSensors()
		return self.sensors
	

	def step(self, action):
		self.nb_step += 1

		tmp_reward = self.grid.move(action)

		# Is he hidded
		done = self.grid.isHide()
		# He gets a better reward if he finds it quick
		reward = tmp_reward if not done else 10/self.nb_step

		# Optionally we can pass additional info, we are not using that for now
		info = {}

		#self.agent_pos = np.array(self.grid.getPosAgent(), dtype=np.float32)
		self.sensors = np.array(self.grid.getSensors(), dtype=np.float32)

		if self.render_mode == "human":
			self.grid.show(self.render_mode, self.metadata["render_fps"])

		return self.sensors, reward, done, info

	def render(self, mode="human"):
		if self.render_mode == "rgb_array":
			return self.grid.show(self.render_mode, self.metadata["render_fps"])

	def change_render_mode(self, mode):
		self.render_mode = mode
	
def main():
	# Instantiate the env
	env = GoLeftEnv(grid_size=20, sameMap=False)
	# If the environment don't follow the interface, an error will be thrown
	check_env(env, warn=True)

	# We vectorize the environement, choose a model and make it learn how to hide
	# env = make_vec_env(lambda: env, n_envs=1)
	model = DQN('MlpPolicy', env).learn(200000, progress_bar=True)
	env.change_render_mode("human")

	input("Press Enter to continue...")

	# Test the trained agent
	obs = env.reset()
	n_steps = 20
	for i in range(20):
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
