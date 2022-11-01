#!/usr/bin/env pybricks-micropython

"""
Example LEGO® MINDSTORMS® EV3 Robot Arm Program
-----------------------------------------------

This program requires LEGO® EV3 MicroPython v2.0.
Download: https://education.lego.com/en-us/support/mindstorms-ev3/python-for-ev3

Building instructions can be found at:
https://education.lego.com/en-us/support/mindstorms-ev3/building-instructions#building-core
"""

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor, UltrasonicSensor
from pybricks.parameters import Port, Stop, Direction, Color
from pybricks.tools import wait

# Initialize the EV3 Brick
ev3 = EV3Brick()

# Configure the gripper motor on Port A with default settings.
gripper_motor = Motor(Port.A)

test = Motor(Port.D)

test.run(500)

# Configure the elbow motor. It has an 8-teeth and a 40-teeth gear
# connected to it. We would like positive speed values to make the
# arm go upward. This corresponds to counterclockwise rotation
# of the motor.
elbow_motor = Motor(Port.B, Direction.COUNTERCLOCKWISE, [8, 40])

# Configure the motor that rotates the base. It has a 12-teeth and a
# 36-teeth gear connected to it. We would like positive speed values
# to make the arm go away from the Touch Sensor. This corresponds
# to counterclockwise rotation of the motor.
base_motor = Motor(Port.C, Direction.COUNTERCLOCKWISE, [12, 36])

# Limit the elbow and base accelerations. This results in
# very smooth motion. Like an industrial robot.
elbow_motor.control.limits(speed=60, acceleration=120)
base_motor.control.limits(speed=60, acceleration=120)

# Set up the Touch Sensor. It acts as an end-switch in the base
# of the robot arm. It defines the starting point of the base.
base_switch = TouchSensor(Port.S1)

# set up distance sensor
#eye_sensor = UltrasonicSensor(Port.S2)

# Set up the 2nd touch Sensor. This sensor detects when the elbow
# is in the starting position. This is when the  sees the
# white beam up close.
elbow_sensor = TouchSensor(Port.S3)

# Set up color sensor
color_sensor = ColorSensor(Port.S4)



# Put the color sensor into COL-COLOR mode.
#color_sensor.mode = 'COL-COLOR'
# print(color_sensor.value)
# colors=('unknown','black','blue','green','yellow','red','white','brown')
# while not ts.value():    # Stop program by pressing touch sensor button
#     print(colors[color_sensor.value()])
#     #Sound.speak(colors[cl.value()]).wait()
#     sleep(1)
# Sound.beep()

# Initialize the elbow. First make it go down for one second.
# Then make it go upwards slowly (25 degrees per second) until
# the Touch Sensor detects the white beam. Then reset the motor
# angle to make this the zero point. Finally, hold the motor
# in place so it does not move.
elbow_motor.run_time(-30, 1000)
elbow_motor.run(25)
while not elbow_sensor.pressed():
    wait(10)
elbow_motor.reset_angle(0)
elbow_motor.hold()

# Initialize the base. First rotate it until the Touch Sensor
# in the base is pressed. Reset the motor angle to make this
# the zero point. Then hold the motor in place so it does not move.
base_motor.run(-90)
while not base_switch.pressed():
    wait(10)
base_motor.reset_angle(0)
base_motor.hold()

# Initialize the gripper. First rotate the motor until it stalls.
# Stalling means that it cannot move any further. This position
# corresponds to the closed position. Then rotate the motor
# by 90 degrees such that the gripper is open.
gripper_motor.run_until_stalled(200, then=Stop.COAST, duty_limit=50)
gripper_motor.reset_angle(0)
gripper_motor.run_target(200, -90)

POSSIBLE_COLORS = [Color.RED, Color.GREEN, Color.BLUE, Color.YELLOW]


def robot_pick(position):
    # This function makes the robot base rotate to the indicated
    # position. There it lowers the elbow, closes the gripper, and
    # raises the elbow to pick up the object.

    # Rotate to the pick-up position.
    base_motor.run_target(60, position)
    # Lower the arm.
    elbow_motor.run_target(150, -85)
    # Close the gripper to grab the wheel stack.
    gripper_motor.run_until_stalled(200, then=Stop.HOLD, duty_limit=50)
    # Raise the arm to lift the wheel stack.
    elbow_motor.run_target(60, 0)


def robot_release(position):
    # This function makes the robot base rotate to the indicated
    # position. There it lowers the elbow, opens the gripper to
    # release the object. Then it raises its arm again.

    # Rotate to the drop-off position.
    base_motor.run_target(60, position)
    # Lower the arm to put the wheel stack on the ground.
    elbow_motor.run_target(150, -85)
    # Open the gripper to release the wheel stack.
    gripper_motor.run_target(200, -90)
    # Raise the arm.
    elbow_motor.run_target(60, 0)




# Play three beeps to indicate that the initialization is complete.
# for i in range(3):
#     ev3.speaker.beep()
#     wait(100)

# Define the destinations for picking up and moving the wheels.

WEST = 200
NOWE = 140
NORTH = 100
NOES = 60
EAST= 5

stop = 1

def killswitch():
    global stop
    color = color_sensor.color()
    if color == color.RED:
        stop = 0


# This is the main part of the program. It is a loop that repeats endlessly.
#
# First, the robot moves the object on the left towards the middle.
# Second, the robot moves the object on the right towards the left.
# Finally, the robot moves the object that is now in the middle, to the right.
#
# Now we have a wheel stack on the left and on the right as before, but they
# have switched places. Then the loop repeats to do this over and over.
# Wait for the center button to be pressed or a color to be scanned.
while True:
    # Store the color measured by the Color Sensor.
    color = color_sensor.color()
    stop = 1
    # break out of the loop.
    if color in POSSIBLE_COLORS:
        if color == color.BLUE:
            while stop != 0:
                #Move a wheel stack from the left to the middle.
                robot_pick(WEST)
                killswitch()
                if stop == 0:
                    robot_release(WEST)
                else:
                    robot_release(NORTH)

                    # Move a wheel stack from the right to the left.
                    killswitch()
                    if stop == 0:
                        wait(10)
                    else:
                        robot_pick(EAST)
                        killswitch()
                        if stop == 0:
                            robot_release(EAST)
                        else:
                            robot_release(WEST)
             
                            #Move a wheel stack from the middle to the right.
                            killswitch()
                            if stop == 0:
                                wait(10)      
                            else:          
                                robot_pick(NORTH)
                                killswitch()
                                if stop == 0:
                                    robot_release(NORTH)
                                else:
                                    robot_release(EAST)
                   
        if color == color.GREEN:
            killswitch()
            while stop != 0:                
                robot_pick(NOES)
                killswitch()
                if stop == 0:
                    robot_release(NOES)
                else:
                    robot_release(NOWE)
                killswitch()
               
        if color == color.YELLOW:
             killswitch()
             while stop != 0:
                killswitch()
                # Play three beeps to indicate that the initialization is complete.
                ev3.speaker.beep()
                wait(200)