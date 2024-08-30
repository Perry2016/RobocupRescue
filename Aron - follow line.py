from hub import light_matrix, port, motion_sensor # this adds ports
import runloop, motor_pair, color_sensor, color, distance_sensor
motors = motor_pair #this shortens long code
colour = color_sensor 
speed = 400
gyro = motion_sensor
motors.pair(motor_pair.PAIR_1, port.A, port.B) # this pairs the two motor ports


async def main():
    await gyro.set_yaw_face.gyro.FRONT
    if gyro.tilt_angles()[0] < -80:
        grab_angle = -1
    elif gyro.tilt_angles()[0] < 80:
        grab_angle = 1
    else:
        grab_angle = 0
    print(grab_angle)
    await motors.move_for_degrees(motor_pair.PAIR_1, 45, 0, velocity= 0 - speed)
    await motors.move_for_degrees(motor_pair.PAIR_1, 150, 90, velocity= speed)
    #motors.move(motor_pair.PAIR_1, -100, velocity= 90)
    while True:
        if distance_sensor.distance(port.E) > 500 or distance_sensor.distance(port.E) == -1:
            motors.move(motors.PAIR_1, -100, velocity= 90)
        else:
            distance_for_can = distance_sensor.distance(port.E)
            angle_for_can = gyro.tilt_angles[0]
            motors.stop(motor_pair.PAIR_1)
            break
    if grab_angle == -1:
        while gyro.tilt_angles()[0] < 89:
            motors.move(motors.PAIR_1, 100, 90)
        motors.stop(motors.PAIR_1)
    elif grab_angle == 1:
        while gyro.tilt_angles()[0] > -89:
            motors.move(motors.PAIR_1, -100, 90)
        motors.stop(motors.PAIR_1)
    elif grab_angle == 0:
        while gyro.tilt_angles()[0] < 187:
            motors.move(motors.PAIR_1, 100, 90)
        motors.stop(motors.PAIR_1)

def followline():
        lgreen = colour.color(port.C) #finding the color the sensors are seeing
        rgreen = colour.color(port.D)
        lcolour = colour.reflection(port.C) #this finds the reflected colour of the sensors
        rcolour = colour.reflection(port.D)

        if lgreen is color.GREEN or rgreen is color.GREEN:# this move me left or right
            if lgreen is color.GREEN: # if the left sensor discovers green then...
                motors.move_for_degrees(motors.PAIR_1, 3600, 0, velocity = 10)
                motors.move_for_degrees(motors.PAIR_1, 310, -45, velocity = speed) # the robot turns left
            if rgreen is color.GREEN: # if the right sensor discovers green then...
                motors.move_for_degrees(motors.PAIR_1, 3600, 0, velocity = 10)
                motors.move_for_degrees(motors.PAIR_1, 310, 45, velocity = speed) # the robot turns right

        else: # if there are no green squares

            direction = (lcolour - rcolour) * 2 # this calculates the angle to go forward
            motors.move(motors.PAIR_1, direction, velocity = speed) #this moves the robot along the line


gyro.reset_yaw(0)
while colour.reflection(port.C) < 80 or colour.reflection(port.D) < 80:
    followline() #this runs the function
motor_pair.stop(motor_pair.PAIR_1)
runloop.run(main())
'''
while distance_sensor.distance(port.F) > 50:
    print("1")
    motors.move(motor_pair.PAIR_1, -100, velocity= 360)
motor_pair.stop(motor_pair.PAIR_1)
'''
