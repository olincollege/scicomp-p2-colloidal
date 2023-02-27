# Modelling Brownian Motion
by Annabelle Platt 

## Overview
The purpose of this repository is to replicate Brownian motion with colliding particles. 


## Running the Code 
To run the code, you can simply run `model.py`. This creates an instance of the model and runs the loop. 

This one line is all you need: 

`model = Model(.01, 25, 50)`

You can modify the timestep, size, and number of particles to create here.The first parameter is timestep. Keeping it small makes collisions work better. The second is size. Keeping it smaller means particles are more likely to collide with each other but you can play around with it. The third parameter is the number of particles. With large numbers of particles they can sometimes get stuck in each other. This is okay for now and they can unstick eventually, but should be fixed in the final version. 

## Modelling Decisions

### Assumptions
I am assuming no friction and no viscosity, and that all particles have the same mass. 

## Benchmarking
Not implemented yet, but will be a log-log plot of average x and y displacement that should show a slope of 1. 

## Limitations
Many. Will elaborate in final version. 