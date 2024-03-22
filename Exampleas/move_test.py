from picarpro.control import move  # Imports the move module from picarpro.control package

speed_set = 30  # Sets the speed for movement
movement = move.Move()  # Instantiates an object of the Move class
movement.move(speed_set, 'forward', 'no', 0.0,7.0)  # Moves forward without turning
movement.move(speed_set, 'no', 'right', 1.3,7.0)  # Turns right without moving forward
movement.move(speed_set, 'forward', 'no', 0.0,7.0)  # Moves forward again
movement.motorStop()  # Stops the motors
movement.destroy()  # Cleans up GPIO resources


