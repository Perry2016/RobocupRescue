import orientation
from hub import port, light_matrix, button
import runloop
import motor_pair

async def main():
    driving_velocity = 250

    # pair motors
    motor_pair.pair(motor_pair.PAIR_1, port.C, port.D)

    # define the ride function
    async def ride():
        await light_matrix.write(str(driving_velocity))
        await motor_pair.move_for_degrees(motor_pair.PAIR_1, 720, 0, velocity = driving_velocity)

    # set conditions for moving forward and setting velocity
    while True:
        if button.pressed(button.LEFT):
            driving_velocity -= 50
            await ride()
            await runloop.sleep_ms(3000)
        elif button.pressed(button.RIGHT):
            driving_velocity += 50
            await ride()
            await runloop.sleep_ms(3000)

runloop.run(main())

runloop.run(main())
import orientation
import motor
from hub import port
