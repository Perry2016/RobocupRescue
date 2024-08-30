from hub import port # this adds ports
from hub import motion_sensor
import motor
import runloop, motor_pair, color_sensor, color, distance_sensor
import motor_pair
import time

motors = motor_pair #this shortens long code
colour = color_sensor
speed = 360

motor_pair.pair(motor_pair.PAIR_1, port.A, port.B)
# this pairs the two motor ports

async def main():
    #motion_sensor.reset_yaw_angle(0)

    await motors.move_for_degrees(motor_pair.PAIR_1,150,100, velocity= speed)
    #motors.move(motor_pair.PAIR_1, -100, velocity= 90)
    while True:
        if distance_sensor.distance(port.E) > 400 or distance_sensor.distance(port.E) ==-1:
            motors.move(motor_pair.PAIR_1, -100, velocity= 50)
        else:
            motor_pair.stop(motor_pair.PAIR_1)
            time.sleep_ms(1000)
            distance_for_can = distance_sensor.distance(port.E)
            if distance_sensor.distance(port.E) > 400 or distance_sensor.distance(port.E) ==-1:
                continue
            break
    await motor.run_for_degrees(port.F, 200, -100)
    # Turn 180
    await motors.move_for_degrees(motor_pair.PAIR_1,245,100, velocity= 50)# turn 180 calibrate in competition
    # Go to catch the can
    #print(distance_for_can)
    await motors.move_for_degrees(motor_pair.PAIR_1, int((distance_for_can/10-13)/17.6*360),0, velocity = 0 - speed)
    await motor.run_for_degrees(port.F, 300, 100)
    #Back to silver bar
    while colour.reflection(port.C) < 80 and colour.reflection(port.D) < 80:
        motors.move(motor_pair.PAIR_1, 0, velocity= 90)
    motor_pair.stop(motor_pair.PAIR_1)

    if motion_sensor.tilt_angles()[0] < 0:
        while motion_sensor.tilt_angles()[0] < -5:
            motors.move(motor_pair.PAIR_1, 100, velocity= 50)
        motor_pair.stop(motor_pair.PAIR_1)
    else:
        while motion_sensor.tilt_angles()[0] > 5:
            motors.move(motor_pair.PAIR_1, -100, velocity= 50)
        motor_pair.stop(motor_pair.PAIR_1)

    await motors.move_for_degrees(motor_pair.PAIR_1,630,0, velocity= 0 - speed)
    await motor.run_for_degrees(port.F, 100, -100)
    await motors.move_for_degrees(motor_pair.PAIR_1,150,0, velocity= - 180)
    await motor.run_for_degrees(port.F, 200, -100)
    await motors.move_for_degrees(motor_pair.PAIR_1, 700, 0, velocity= speed)

async def followline():

    lgreen = colour.color(port.C)
#finding the color the sensors are seeing
    rgreen = colour.color(port.D)
    lcolour = colour.reflection(port.C)
#this finds the reflected colour of the sensors
    rcolour = colour.reflection(port.D)
    if lgreen is color.GREEN or rgreen is color.GREEN:# this move me left or right
        if lgreen is color.GREEN: # if the left sensor discovers green then...
            await motors.move_for_degrees(motors.PAIR_1,60,0, velocity = speed)
            await motors.move_for_degrees(motors.PAIR_1,140,-50, velocity = speed)
    # the robot turns left
        if rgreen is color.GREEN: # if the right sensor discovers green then...
            await motors.move_for_degrees(motors.PAIR_1,60,0, velocity = speed)
            await motors.move_for_degrees(motors.PAIR_1,140,50, velocity = speed)
    # the robot turns right
    else:
    # this calculates the angle to go forward
        motors.move(motors.PAIR_1, (lcolour - rcolour) * 3, velocity = speed)


async def tower():
    await motor_pair.move_for_degrees(motors.PAIR_1,100,0, velocity = 0 - speed)
    await motors.move_for_degrees(motor_pair.PAIR_1,120,100, velocity= speed)
    await motors.move_for_degrees(motor_pair.PAIR_1,120,-20, velocity= speed)
    while colour.color(port.D) is not color.BLACK:
        motor_pair.move(motor_pair.PAIR_1,-15,velocity=speed)
    motor_pair.stop(motor_pair.PAIR_1)
    await motors.move_for_degrees(motor_pair.PAIR_1,30,0, velocity= speed)
    await motors.move_for_degrees(motor_pair.PAIR_1,100,100, velocity= speed)
    

#this moves the robot along the line

while colour.reflection(port.C) < 80 and colour.reflection(port.D) < 80:
    if distance_sensor.distance(port.E) > 50 or distance_sensor.distance(port.E) ==-1: 
            runloop.run(followline())
    else:
            runloop.run(tower())
motor_pair.stop(motor_pair.PAIR_1)
runloop.run(main())

