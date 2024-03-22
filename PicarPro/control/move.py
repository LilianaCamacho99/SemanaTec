from .move import *

'''
For comprehensive insights into this module, please refer to the following link:
https://www.adeept.com/learn/detail-50.html. Additionally, it is recommended 
to extract the contents of the zip file provided on the webpage. 
For further guidance, please consult Lesson 6. Moreover, you can find relevant 
information within the module documentation enclosed within the adeeptpicarpro package.
'''

import time     # Library for time-related functions
import RPi.GPIO as GPIO     # Library for Raspberry Pi GPIO control

class Move:
    def __init__(self):
        #Initializes the Move object.
        #Sets up GPIO pins for motor control and initializes PWM variables.

        # Motor pins: The motor on the left is connected to the MOTOR-B port; 
        #the motor on the right is connected to the MOTOR-A port.
        self.Motor_A_EN = 4
        self.Motor_B_EN = 17
        self.Motor_A_Pin1 = 26
        self.Motor_A_Pin2 = 21
        self.Motor_B_Pin1 = 27
        self.Motor_B_Pin2 = 18

        # Direction constants
        self.Dir_forward = 0
        self.Dir_backward = 1
        self.left_forward = 1
        self.left_backward = 0
        self.right_forward = 0
        self.right_backward = 1

        # PWM variables
        self.pwm_A = 0
        self.pwm_B = 0

        self.setup()

    def motorStop(self):
        #Stops both motors by setting all motor pins to LOW.
        GPIO.output(self.Motor_A_Pin1, GPIO.LOW)
        GPIO.output(self.Motor_A_Pin2, GPIO.LOW)
        GPIO.output(self.Motor_B_Pin1, GPIO.LOW)
        GPIO.output(self.Motor_B_Pin2, GPIO.LOW)
        GPIO.output(self.Motor_A_EN, GPIO.LOW)
        GPIO.output(self.Motor_B_EN, GPIO.LOW)

    def setup(self):
        #Sets up GPIO pins for motor control
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.Motor_A_EN, GPIO.OUT)
        GPIO.setup(self.Motor_B_EN, GPIO.OUT)
        GPIO.setup(self.Motor_A_Pin1, GPIO.OUT)
        GPIO.setup(self.Motor_A_Pin2, GPIO.OUT)
        GPIO.setup(self.Motor_B_Pin1, GPIO.OUT)
        GPIO.setup(self.Motor_B_Pin2, GPIO.OUT)
        self.motorStop()

        # Initialize PWM objects for motor control with a frequency of 1000 Hz
        try:
            self.pwm_A = GPIO.PWM(self.Motor_A_EN, 1000)
            self.pwm_B = GPIO.PWM(self.Motor_B_EN, 1000)
        except:
            pass

    def motor_left(self, status, direction, speed):
        #Controls the left motor.

        if status == 0:     #Motor status (0 for stop, 1 for move).
            GPIO.output(self.Motor_B_Pin1, GPIO.LOW)
            GPIO.output(self.Motor_B_Pin2, GPIO.LOW)
            GPIO.output(self.Motor_B_EN, GPIO.LOW)
        else:
            if direction == self.Dir_backward:     # If direction is backward
                GPIO.output(self.Motor_B_Pin1, GPIO.HIGH)     # Set motorB pin 1 to HIGH (backward direction)
                GPIO.output(self.Motor_B_Pin2, GPIO.LOW)     # Set motorB pin 2 to LOW
                self.pwm_B.start(100)    # Start PWM with 100% duty cycle
                self.pwm_B.ChangeDutyCycle(speed)     # Set PWM duty cycle to control speed
            elif direction == self.Dir_forward:     # If direction is forward
                GPIO.output(self.Motor_B_Pin1, GPIO.LOW)     # Set motorB pin 1 to LOW
                GPIO.output(self.Motor_B_Pin2, GPIO.HIGH)     # Set motorB pin 2 to HIGH (forward direction)
                self.pwm_B.start(0)     # Start PWM with 0% duty cycle (stopped)
                self.pwm_B.ChangeDutyCycle(speed)     # Set PWM duty cycle to control speed

    def motor_right(self, status, direction, speed):
        #Controls the right motor.
    
        if status == 0:     #Motor status (0 for stop, 1 for move).
            GPIO.output(self.Motor_A_Pin1, GPIO.LOW)
            GPIO.output(self.Motor_A_Pin2, GPIO.LOW)
            GPIO.output(self.Motor_A_EN, GPIO.LOW)
        else:
            if direction == self.Dir_forward:     # If direction is forward
                GPIO.output(self.Motor_A_Pin1, GPIO.HIGH)     # Set motorA pin 1 to HIGH (forward direction)
                GPIO.output(self.Motor_A_Pin2, GPIO.LOW)      # Set motor pin 1 to LOW (forward direction)
                self.pwm_A.start(100)     # Start PWM with 100% duty cycle
                self.pwm_A.ChangeDutyCycle(speed)     # Set PWM duty cycle to control speed
            elif direction == self.Dir_backward:      # If direction is backward
                GPIO.output(self.Motor_A_Pin1, GPIO.LOW)      # Set motorA pin 1 to LOW
                GPIO.output(self.Motor_A_Pin2, GPIO.HIGH)     # Set motor pin 2 to HIGH (backward direction)
                self.pwm_A.start(0)     # Start PWM with 0% duty cycle (stopped)
                self.pwm_A.ChangeDutyCycle(speed)     # Set PWM duty cycle to control speed

    def move(self, speed, direction, turn, radius=0.6, second=2.0):
        #Controls the main movement of the robot.
        
        if direction == 'backward':     #Movement direction: 'forward', 'backward', or 'no'.
            if turn == 'right':     #Turn direction: 'left', 'right', or 'no'.
                # Turn right while moving backward
                self.motor_left(0, self.left_backward, int(speed*radius))
                self.motor_right(1, self.right_forward, speed)
                time.sleep(second)     #duration of movement (default: 2.0 seconds).
            elif turn == 'left':     #Turn direction: 'left', 'right', or 'no'.
                # Turn left while moving backward
                self.motor_left(1, self.left_forward, speed)
                self.motor_right(0, self.right_backward, int(speed*radius))
                time.sleep(second)     #duration of movement (default: 2.0 seconds).
            else:
                # Move backward with no turn
                self.motor_left(1, self.left_forward, speed)
                self.motor_right(1, self.right_forward, speed)
                time.sleep(second)     #duration of movement (default: 2.0 seconds).
        elif direction == 'forward':     #Movement direction: 'forward', 'backward', or 'no'.
            if turn == 'right':     #Turn direction: 'left', 'right', or 'no'.
                # Turn right while moving forward
                self.motor_left(0, self.left_forward, int(speed*radius))
                self.motor_right(1, self.right_backward, speed)
                time.sleep(second)     #duration of movement (default: 2.0 seconds).
            elif turn == 'left':     #Turn direction: 'left', 'right', or 'no'.
                # Turn left while moving forward
                self.motor_left(1, self.left_backward, speed)
                self.motor_right(0, self.right_forward, int(speed*radius))
                time.sleep(second)     #duration of movement (default: 2.0 seconds).
            else:
                # Move forward with no turn
                self.motor_left(1, self.left_backward, speed)
                self.motor_right(1, self.right_backward, speed)
                time.sleep(second)     #duration of movement (default: 2.0 seconds).
        elif direction == 'no':     #Movement direction: 'forward', 'backward', or 'no'.
            if turn == 'right':     #Turn direction: 'left', 'right', or 'no'.
                # Turn right in place
                self.motor_left(1, self.left_backward, speed)
                self.motor_right(1, self.right_forward, speed)
                time.sleep(second)     #duration of movement (default: 2.0 seconds).
            elif turn == 'left':     #Turn direction: 'left', 'right', or 'no'.
                # Turn left in place
                self.motor_left(1, self.left_forward, speed)
                self.motor_right(1, self.right_backward, speed)
                time.sleep(second)     #duration of movement (default: 2.0 seconds).
            else:
                # Stop the motors
                self.motorStop()
        else:
            pass

    def destroy(self):
        #Stops motors and cleans up GPIO.
        
        self.motorStop()
        GPIO.cleanup()
