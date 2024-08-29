from hub import light_matrix, port # this adds ports
import runloop, motor_pair, color_sensor, color
motors = motor_pair #this shortens long code
colour = color_sensor 

motors.pair(motor_pair.PAIR_1, port.A, port.B) # this pairs the two motor ports


def followline():
    lgreen = colour.color(port.C) #finding the color the sensors are seeing
    rgreen = colour.color(port.D)
    lcolour = colour.reflection(port.C) #this finds the reflected colour of the sensors
    rcolour = colour.reflection(port.D)
    
    if lgreen is color.GREEN or rgreen is color.GREEN:# this move me left or right
        if lgreen is color.GREEN: # if the left sensor discovers green then...
            #motors.move_for_degrees(motors.PAIR_1, 3600, 0, velocity = 10)
            motors.move_for_degrees(motors.PAIR_1, 310, -45, velocity = 360) # the robot turns left
        if rgreen is color.GREEN: # if the right sensor discovers green then...
            #motors.move_for_degrees(motors.PAIR_1, 3600, 0, velocity = 10)
            motors.move_for_degrees(motors.PAIR_1, 310, 45, velocity = 360) # the robot turns right

    else: # if there are no green squares
        
        direction = (lcolour - rcolour) * 2 # this calculates the angle to go forward
        motors.move(motors.PAIR_1, direction, velocity = 360) #this moves the robot along the line


while colour.reflection(port.C) < 80 or colour.reflection(port.D) < 80:
    followline() #this runs the function
motor_pair.stop(motor_pair.PAIR_1)
