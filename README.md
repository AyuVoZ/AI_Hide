# Explanation

An agent will learn to hide from a turret using reinforcment learning.

# Installation

This programm is using stable-baselines3 and python3.7+. To install the package you can use pip by executing this command :
```
pip install stable-baselines3[extra]
```
It will install the package and some other optional packages.

# Testing

The programm can be run by using this command
```
python3 hide.py
```

# Architecture

The programm will create a new environnement that will be printed in the CLI. The environement will be a grid 12x12 with obstacle and a turret at the center of the map.
The environnement is created with Gym from OpenAI. The agent will be represented as a "x", the obstacles as a "M" and the rest as a ".".

# Results

This algorithm is working well, the agent learns to hide from the turret in places that are near him. But some times he will walk into walls for the whole test.
