import RPi.GPIO as GPIO     # Importing the GPIO library for Raspberry Pi
import time     # Importing library for time-related function
from picarpro.control import move     # Importing the move module from the picarpro.control package for controlling movement

class LineFollower:
    def __init__(self):
        # Initializes the LineFollower object with GPIO pin numbers and sets up GPIO mode and pins.
        self.line_pin_right = 19 
        self.line_pin_middle = 16 
        self.line_pin_left = 20 
        self.setup()     # Calls the setup method to configure GPIO
        self.movement = move.Move()     # Initializes an instance of the move.Move class for movement control

    def setup(self):
        #Sets up the GPIO pins for input mode.
        GPIO.setwarnings(False)     # Disable GPIO warnings
        GPIO.setmode(GPIO.BCM)      # Set GPIO mode to BCM
        GPIO.setup(self.line_pin_right, GPIO.IN)
        GPIO.setup(self.line_pin_middle, GPIO.IN)
        GPIO.setup(self.line_pin_left, GPIO.IN)

    def run(self, max_time_search = 5):
        # Runs the line-following algorithm based on sensor inputs.
        start_time = time.time()     # Record the start time

        while True:
            # Read the status of all line sensors
            status_right = GPIO.input(self.line_pin_right)
            status_middle = GPIO.input(self.line_pin_middle)
            status_left = GPIO.input(self.line_pin_left)

            # Determine robot movement based on line sensor readings
            if status_middle == 1:
                start_time = time.time()     # Reset the start time
                self.movement.move(100, 'forward', 'no', 1)     # Move forward if middle line detected

            elif status_left == 1:
                start_time = time.time()     # Reset the start time
                self.movement.move(100, 'forward', 'right', 0.6)     # Turn right if left line detected

            elif status_right == 1:
                start_time = time.time()     # Reset the start time
                self.movement.move(100, 'forward', 'left', 0.6)     # Turn left if right line detected

            else:
                self.movement.move(100, 'backward', 'no', 1)     # Move backward if no line detected

                # Check if the maximum search time has elapsed
                if time.time() - start_time >= max_time_search:
                    break     # Exit the loop if maximum search time reached
    