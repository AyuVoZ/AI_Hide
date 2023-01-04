Gwendal Le Mouel
Nicolas Gautier

# Objectives

An agent will learn to hide from a turret using a reinforcement learning algorithm. The agent will use virtual sensors (simulating a real robot) to choose the best action to perform. The final task will be to have an agent that can deal with a previously unseen environment.

# Installation

This program is using stable-baselines3 and python3.7+. To install the package you can use pip by executing this command :
```
pip install stable-baselines3[extra]
```
It will install the package and some other optional packages.

# Testing

The program can be run by using this command
```
python3 hide.py
```

# High-level description

The program will create procedural environments with which the agent will interact. The environment consists of a 20x20 grid (adjustable) with some random structures behind which the agent can hide. The turret is in the middle of the grid and the agent will be randomly placed in a position visible by the turret. The environment is shown using pygame. The environment is created with Gym from OpenAI.

The agent uses the PPO reinforcement learning algorithm from [Stable-Baselines3]{https://stable-baselines3.readthedocs.io/en/master/index.html} to learn:

* The only action the robot can perform is to move in one of the following directions: left, right, up and down.
* The robot receives the following information from its sensors:
    + the distances of the nearest obstacles up to 10 cases (range distance of the sensors) in 9 directions (left, right, up, left and the 4 diagonals).
    + the direction of the turret (north, northwest, west, ...)
    + its position in the grid  
* The robot will receive a positive reward (proportional to the time needed to hide) when it is hidden from the turret and a negative reward when it tries to perform a forbidden action (moving into a wall for example).


# Results

This algorithm works well in a known environment where it can find the fastest way to hide from the turret.

It works much less well when it trains in different environments to be able to generalize. One solution might be to learn the agent for a much longer time.

****************************** video **********************************


# Challenges

* Creating a procedural environment: one of the goals was to train the agent in a generated environment. It was necessary to generate complex and realistic environments that are neither too easy nor too difficult to solve. We also had to add methods to get feedback from the map (e.g. raycast to know if the agent is hidden or to simulate the sensors).

* choosing best parameters

* generalize on unseen environment

# Future work

# Takeaways



Challenges (1 paragraph): Describe the challenges you faced and how you overcame them.
Future work (1 paragraph): If you had more time, how would you improve your implementation?
Takeaways