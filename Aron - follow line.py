from hub import light_matrix, port
import runloop, motor_pair, color_sensor, color
motors = motor_pair #this shortens long code
colour = color_sensor 

motors.pair(motor_pair.PAIR_1, port.A, port.B) # this pairs the two motor ports


def followline(): # this is the function
    lgreen = colour.color(port.C) #finding the color the sensors are seeing
    rgreen = colour.color(port.D)
    if lgreen is color.GREEN or rgreen is color.GREEN:# this move me left or right
        if lgreen is color.GREEN:
            motors.move_for_degrees(motors.PAIR_1, 360, -45, velocity = 90)
        if rgreen is color.GREEN:
            motors.move_for_degrees(motors.PAIR_1, 360, 45, velocity = 90)

    else:
        lcolour = colour.reflection(port.C) #this finds the reflected colour of the sensors
        rcolour = colour.reflection(port.D)
        direction = (lcolour - rcolour) # this calculates the angle to go
        motors.move(motors.PAIR_1, direction, velocity = 360) #this moves the robot along the line

while True:
    followline() #this runs the function
