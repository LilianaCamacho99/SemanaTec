from .led import *
'''
For comprehensive insights into this module, please refer to the following link:
https://www.adeept.com/learn/detail-50.html. Additionally, it is recommended 
to extract the contents of the zip file provided on the webpage. 
For further guidance, please consult Lesson 8. Moreover, you can find relevant 
information within the module documentation enclosed within the adeeptpicarpro package.
'''



import time  # Importing the time module for time-related functions
import RPi.GPIO as GPIO  # Importing the RPi.GPIO module for controlling Raspberry Pi GPIO pins
from rpi_ws281x import *  # Importing functions from the NeoPixel LED controller
import threading  # Importing the threading module for threading support

class RobotLight(threading.Thread):  # Defines a custom thread class for controlling robot lights
    def __init__(self, *args, **kwargs):  # Initializes the RobotLight object
        super()._init_(*args, **kwargs)  # Initializes the thread
        self.LED_COUNT      = 16     # Number of LEDs
        self.LED_PIN        = 12     # GPIO pin connected to the LEDs
        self.LED_FREQ_HZ    = 800000     # LED signal frequency in hertz
        self.LED_DMA        = 10    # DMA channel to use for generating signal
        self.LED_BRIGHTNESS = 255     # LED brightness (0 to 255)
        self.LED_INVERT     = False     # True to invert the signal
        self.LED_CHANNEL    = 0     # GPIO channel

        self.colorBreathR = 0  # Red component for breathing effect
        self.colorBreathG = 0  # Green component for breathing effect
        self.colorBreathB = 0  # Blue component for breathing effect
        self.breathSteps = 10  # Steps for breathing effect

        self.lightMode = 'none'        #'none' 'police' 'breath'

        GPIO.setwarnings(False)  # Disables GPIO warnings
        GPIO.setmode(GPIO.BCM)  # Sets the pin numbering mode
        GPIO.setup(5, GPIO.OUT)  # Configures pin 5 as output
        GPIO.setup(6, GPIO.OUT)  # Configures pin 6 as output
        GPIO.setup(13, GPIO.OUT)  # Configures pin 13 as output
    
        # Creates a NeoPixel object with appropriate configuration
        self.strip = Adafruit_NeoPixel(self.LED_COUNT, self.LED_PIN, self.LED_FREQ_HZ, self.LED_DMA, self.LED_INVERT, self.LED_BRIGHTNESS, self.LED_CHANNEL)
        self.strip.begin()  # Initializes the library

        self.__flag = threading.Event()  # Initializes an event to pause the thread
        self.__flag.clear()  # Clears the event

    # Define functions to animate LEDs in various ways
    def setColor(self, R, G, B):  # Displays a color across all LEDs.
        color = Color(int(R),int(G),int(B))  # Converts RGB values to a color

        for i in range(self.strip.numPixels()):  # Iterates over all LEDs
            self.strip.setPixelColor(i, color)  # Sets the color for the LED
            self.strip.show()  # Updates the LED display

    def setSomeColor(self, R, G, B, ID):  # Sets a color for specified LEDs
        color = Color(int(R),int(G),int(B))  # Converts RGB values to a color

        for i in ID:  # Iterates over specified LEDs
            self.strip.setPixelColor(i, color)  # Sets the color for the LED
            self.strip.show()  # Updates the LED display

    def pause(self):  # Pauses lighting effects
        self.lightMode = 'none'  # Sets the light mode to none
        self.setColor(0,0,0)  # Turns off all LEDs
        self.__flag.clear()  # Clears the event flag

    def resume(self):  # Resumes lighting effects
        self.__flag.set()  # Sets the event flag

    def police(self):  # Activates police light mode
        self.lightMode = 'police'  # Sets the light mode to police
        self.resume()  # Resumes the lighting effects

    def policeProcessing(self):  # Implements police light effect
        while self.lightMode == 'police':  # Runs the loop while in police light mode

            for i in range(0,3):  # Iterates over a range
                self.setSomeColor(0,0,255,[0,1,2])  # Sets blue color for specific LEDs
                time.sleep(0.05)  # Pauses for a short time
                self.setSomeColor(0,0,0,[0,1,2])  # Turns off the LEDs
                time.sleep(0.05)  # Pauses for a short time
                
            if self.lightMode != 'police':  # Checks if the mode changed
                break  # Exits the loop

            time.sleep(1)  # Pauses for a longer time

            for i in range(0,3):  # Iterates over a range
                self.setSomeColor(255,0,0,[0,1,2])  # Sets red color for specific LEDs
                time.sleep(0.05)  # Pauses for a short time
                self.setSomeColor(0,0,0,[0,1,2])  # Turns off the LEDs
                time.sleep(0.05)  # Pauses for a short time

            time.sleep(1)  # Pauses for a longer time

    def breath(self, R_input, G_input, B_input):  # Activates breathing effect with a specific color
        self.lightMode = 'breath'  # Sets the light mode to breath
        self.colorBreathR = R_input  # Sets the red component for breathing
        self.colorBreathG = G_input  # Sets the green component for breathing
        self.colorBreathB = B_input  # Sets the blue component for breathing
        self.resume()  # Resumes the lighting effects

    def breathProcessing(self):  # Implements breathing effect
        while self.lightMode == 'breath':  # Runs the loop while in breath mode

            for i in range(0,self.breathSteps):  # Iterates over a range
                if self.lightMode != 'breath':  # Checks if the mode changed
                    break  # Exits the loop

                self.setColor(self.colorBreathR*i/self.breathSteps, self.colorBreathG*i/self.breathSteps, self.colorBreathB*i/self.breathSteps)  # Sets the color for breathing
                time.sleep(0.03)  # Pauses for a short time

            for i in range(0,self.breathSteps):  # Iterates over a range
                if self.lightMode != 'breath':  # Checks if the mode changed
                    break  # Exits the loop

                self.setColor(self.colorBreathR-(self.colorBreathR*i/self.breathSteps), self.colorBreathG-(self.colorBreathG*i/self.breathSteps), self.colorBreathB-(self.colorBreathB*i/self.breathSteps))  # Sets the color for breathing
                time.sleep(0.03)  # Pauses for a short time

    def frontLight(self, switch):  # Controls the front lights
        if switch == 'on':  # Checks if the lights should be turned on
            GPIO.output(6, GPIO.HIGH)  # Turns on GPIO pin 6
            GPIO.output(5, GPIO.HIGH)  # Turns on GPIO pin 5

        elif switch == 'off':  # Checks if the lights should be turned off
            GPIO.output(6,GPIO.LOW)  # Turns off GPIO pin 6
            GPIO.output(5, GPIO.LOW)  # Turns off GPIO pin 5
            
    def switch(self, port, status):  # Controls a switch on specified port
        if port == 1:  # Checks if the port is 1
            if status == 1:  # Checks if the status is 1 (on)
                GPIO.output(5, GPIO.HIGH)  # Turns on GPIO pin 5
                
            elif status == 0:  # Checks if the status is 0 (off)
                GPIO.output(5,GPIO.LOW)  # Turns off GPIO pin 5

            else:  # If status is neither 1 nor 0
                pass  # Does nothing

        elif port == 2:  # Checks if the port is 2
            if status == 1:  # Checks if the status is 1 (on)
                GPIO.output(6, GPIO.HIGH)  # Turns on GPIO pin 6

            elif status == 0:  # Checks if the status is 0 (off)
                GPIO.output(6,GPIO.LOW)  # Turns off GPIO pin 6

            else:  # If status is neither 1 nor 0
                pass  # Does nothing

        elif port == 3:  # Checks if the port is 3
            if status == 1:  # Checks if the status is 1 (on)
                GPIO.output(13, GPIO.HIGH)  # Turns on GPIO pin 13

            elif status == 0:  # Checks if the status is 0 (off)
                GPIO.output(13,GPIO.LOW)  # Turns off GPIO pin 13

            else:  # If status is neither 1 nor 0
                pass  # Does nothing

        else:  # If the port is neither 1, 2, nor 3
            print('Wrong Command: Example--switch(3, 1)->to switch on port3')  # Prints a message

    def set_all_switch_off(self):  # Switches off all ports
        self.switch(1,0)  # Turns off port 1
        self.switch(2,0)  # Turns off port 2
        self.switch(3,0)  # Turns off port 3

    def headLight(self, switch):  # Controls the headlight
        if switch == 'on':  # Checks if the headlight should be turned on
            GPIO.output(5, GPIO.HIGH)  # Turns on GPIO pin 5

        elif switch == 'off':  # Checks if the headlight should be turned off
            GPIO.output(5,GPIO.LOW)  # Turns off GPIO pin 5
            
    def lightChange(self):  # Manages the change of light modes
        if self.lightMode == 'none': 
            self.pause()  # Pauses lighting effects

        elif self.lightMode == 'police':  # Checks if police mode is active
            self.policeProcessing()  # Executes police light effect
            
        elif self.lightMode == 'breath':  # Checks if breath mode is active
            self.breathProcessing()  # Executes breathing light effect

    def run(self):  # Runs the thread
        while 1:  # Runs indefinitely
            self.__flag.wait()  # Waits for the flag
            self.lightChange()  # Manages the change of light modes
