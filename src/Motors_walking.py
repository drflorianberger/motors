#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 15:59:25 2020

@author: flo
"""

# TO DO: 
# - Work on robustess by integrating exceptions. Maybe write a function that checks if a rate is negative?


from pylab import *
import numpy as np
import configparser

# reads out the motor activity of all motors
def read_out_motors_attachment_state(list_of_motors):
    data = []
    for motor in list_of_motors:
        data.append(motor.attachment_state)
    return data


# reads out the position of all motors
def read_out_motors_position(list_of_motors):
    data = []
    for motor in list_of_motors:
        data.append(motor.position)
    return data


# Class that defines the binding event
class Binding:
    def __init__(self, rate, motor):
        self.rate = rate
        self.motor = motor

    # Executing an binding event
    def execute(self):
        self.motor.attachment_state = 1

    # Returns the binding rate: if bound, the motor cannot bind anymore,
    # therefore the rate = 0
    def get_rate(self):
        # if bound
        if self.motor.attachment_state == 1:
            return 0
        else:
            return self.rate

# Class that is used to store all rates
class Rates:
    def __init__(self, binding_rate, unbinding_rate, stepping_rate):
        self.binding_rate = binding_rate
        self.unbinding_rate = unbinding_rate
        self.stepping_rate = stepping_rate               
        
# Class that defines the unbinding event
class Unbinding:
    def __init__(self, rate, motor):
        self.rate = rate
        self.motor = motor

# Executes an binding event
    def execute(self):
        self.motor.attachment_state = 0
        # If motor unbinds, its position is set to zero
        self.motor.position = 0

# Returns the unbinding rate: if bound, return unbinding rate, if unbound, return 0
    def get_rate(self):
        # if bound
        if self.motor.attachment_state == 1:
            return self.rate
        else:
            return 0

# Class that defines the stepping event
class Stepping:
    def __init__(self, rate, motor):
        self.rate = rate
        self.motor = motor
    
# a stepping event changes the position of the motor by 8 nm    
    def execute(self):
        self.motor.position += 8

# returns the stepping rate. Only if the motor is bound it can step    
    def get_rate(self):
        # if bound
        if self.motor.attachment_state == 1:
            return self.rate
        else:
            return 0


# Class that defines the motor
class Motor:
    def __init__(self, attachment_state, position):
        self.attachment_state = attachment_state
        self.position = position

def initalize_motors(num_of_motors, starting_state, starting_position):
    # List of all motors
    motors = []

    # Initialize all motors into the list
    for i in arange(0, num_of_motors):
    # All motors are bound, initializing with starting_state and starting_position
        motors.append(Motor(starting_state, starting_position))
    return motors

def initalize_events(motors, rates):
   # List of all events
   events = [] 
   # For each motor in the list, an binding and an unbinding event is initialzied in the list
   for m in motors:
       events.append(Binding(rates.binding_rate, m))
       events.append(Unbinding(rates.unbinding_rate, m))
       events.append(Stepping(rates.stepping_rate, m))
       
   return events

    
def simulation(total_time):
    # Simulation time
    t = 0
    # data
    data = []

    while t <= total_time:

        # sum of all rates
        sum_rates = 0
        for e in events:
            sum_rates += e.get_rate()
        if sum_rates == 0:
            raise ValueError("The sum of all rate is %s, which is a problem. If it is \
                             negative then something went really wrong. If it is zero\
                             no event will happen. Maybe no binding?" % (sum_rates))

    # waiting time from exp dist
        dt = np.random.exponential(1/sum_rates)

    # Checking which transition should happen
        r = np.random.uniform()

        prob = 0
        for e in events:
            prob += e.get_rate()/sum_rates
            if prob >= r:
                e.execute()
                break

        t += dt
        # md = read_out_motors(motors)
    
        pos = read_out_motors_position(motors)
        data.append([t] + pos)

    data = asarray(data)
    return data

def plot_data(data):
   # Plotting
   plt.figure()
   for i in arange(1, len(data[0])):
      plt.plot(data[:, 0], data[:, i], label='motor ' + str(i))

   plt.legend()
   plt.xlabel('time (s)')
   plt.ylabel('position (nm)')
   plt.show()
   # A figure is saved in /results/figures/
   savefig('../results/figures/motor_positions_vs_time.pdf', bbox_inches='tight') 


# Getting the parameters for the simulation from the parameters.ini file
config = configparser.ConfigParser()
config.read('test.ini')

# Number of motors in the simulation
num_of_motors = config['Parameters'].getint('number_of_motors')

# Total time for the simulation
total_time = config['Parameters'].getint('total_simulation_time')

# Starting state of the motors
starting_state = config['Parameters'].getint('starting_state')

# Starting position of the motors
starting_position = config['Parameters'].getint('starting_position')

# Binding rate
binding_rate = config['Parameters'].getint('binding_rate')

# Unbinding rate
unbinding_rate = config['Parameters'].getint('unbinding_rate')
if unbinding_rate < 0:
    raise ValueError("Expected an unbinding rate >= 0, but got %s" % (unbinding_rate))
    
# Stepping rate
stepping_rate = config['Parameters'].getint('stepping_rate')
if stepping_rate < 0:
    raise ValueError("Expected a stepping rate >= 0, but got %s" % (stepping_rate))

# Putting the rates into an object
rates = Rates(binding_rate, unbinding_rate, stepping_rate)

# Initalize motors into the list motors
motors = initalize_motors(num_of_motors, starting_state, starting_position)

# Intialize events for each motor
events = initalize_events(motors, rates)

# Simulate the system with a Gillespie algorithm
data = simulation(total_time)

# Plot data
plot_data(data)
