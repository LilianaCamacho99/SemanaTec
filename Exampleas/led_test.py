from picarpro.lights import led
import time

RL = led.RobotLight() # Instantiates the RobotLight object
RL.start()  # Starts the thread
RL.frontLight('on')  # Turns on the front light
time.sleep(3)  # Pauses for 3 seconds
RL.frontLight('off')  # Turns off the front light
RL.strip.begin()  # Initializes the LED strip
RL.police()  # Activates police light mode
RL.lightChange()  # Manages the change of light modes
RL.pause()  # Pauses the lighting effects
