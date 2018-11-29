import gym
from gym import error, spaces, utils
from gym.utils import seeding
from random import randint

class Env(gym.Env):
	metadata = {'render.modes': ['human']}

	# States
	# 	State 0 = car is not in your lane
	# 	State 1 = car is in your lane, but not close
	# 	State 2 = car is in your lane and close
	#	State 3 = crash
	# Actions
	# 	Action 0 = maintain speed
	# 	Action 1 = decrease speed
	# 	Action 2 = increase speed
	# 	Action 3 = swerve

	def __init__(self, num_states=4, put_in_danger=0.2):
		self.num_states = num_states
		self.put_in_danger = put_in_danger
		self.state = randint(0, 1)
		self.action_space = spaces.Discrete(4)
		self.observation_space = spaces.Discrete(self.num_states)
		self.seed()
		self.action0changes = { # maintain speed
			0: [100, 0],
			1: [50, 1],
			2: [-50, 3],
		}
		self.action1changes = { # decrease speed
			0: [-50, 0],
			1: [20, 1], # might be 0
			2: [75, 1],
		}
		self.action2changes = { # increase speed
			0: [30, 0],
			1: [-50, 2],
			2: [-100, 3],
		}
		self.action3changes = { # swerve
			0: [-100, 1],
			1: [-100, 0],
			2: [100, 0],
		}

	def seed(self, seed=None):
		self.np_random, seed = seeding.np_random(seed)
		return [seed]

	def step(self, action):
		assert self.action_space.contains(action)
		if action == 0:
			reward, self.state = self.action0changes[self.state]
		if action == 1:
			reward, self.state = self.action1changes[self.state]
		if action == 2:
			reward, self.state = self.action2changes[self.state]
		if action == 3:
			reward, self.state = self.action3changes[self.state]
		if self.np_random.rand() < self.put_in_danger and self.state != 3:
			self.state = 2
		done = (self.state == 3)
		return self.state, reward, done, {}

	def reset(self):
		self.state = randint(0, 1)
		return self.state

	def render(self, mode='human', close=False):
		pass