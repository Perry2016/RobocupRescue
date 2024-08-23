
import motor_pair
import color_sensor
from hub import port
import runloop
motor_pair.pair(motor_pair.PAIR_1, port.A, port.B)



async def main():
    while True:
        reflection_rateE = color_sensor.reflection(port.E)
        reflection_rateF = color_sensor.reflection(port.F)   
         
        print(reflection_rateE)

        # turn left
        if reflection_rateE <= 35:
            motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, 100, 0, 1000)
            print("turn left")

        # turn right
        if reflection_rateF <= 35:
            motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, 100, 1000, 0)
            print("turn right")

        # left color sensor detecting green
        if reflection_rateE > 45 and reflection_rateE <= 70:

            motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, 50, 0, 1000)
            print("left sensor detected green")

        # right color sensor detecting green
        if reflection_rateF > 45 and reflection_rateF <= 70:
            motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, 50, 1000, 0)
            print("left sensor detected green")

        
        if reflection_rateE >= 55 and reflection_rateF >= 55:
            motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, 50, 100, 100)
            print("go straight")

runloop.run(main())
