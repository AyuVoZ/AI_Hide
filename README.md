# Explanation

An agent will learn to hide from a turret using reinforcement learning.

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

# Architecture

The program will create a new environment that will be printed in the CLI. The environment will be a grid 12x12 with obstacle and a turret in the center of the map.
The environment is created with Gym from OpenAI. The agent will be represented as a "x", the obstacles as a "M" and the rest as a ".".

# Results

This algorithm works well, the agent learns to hide from the turret in places that are near him. But sometimes he will walk into walls for the whole test.
