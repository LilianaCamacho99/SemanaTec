'''
For comprehensive insights into this module, please refer to the following link:
https://www.adeept.com/learn/detail-50.html. Additionally, it is recommended 
to extract the contents of the zip file provided on the webpage. 
For further guidance, please consult Lesson 5. Moreover, you can find relevant 
information within the module documentation enclosed within the adeeptpicarpro package.
'''

from __future__ import division # Importing division from Python 3 for compatibility
import time # Importing the time module for time-related functions
import RPi.GPIO as GPIO # Importing the GPIO library for Raspberry Pi
import Adafruit_PCA9685 # Importing Adafruit PCA9685 module for PWM control
import threading # Importing threading module for multi-threading support

pwm = Adafruit_PCA9685.PCA9685() # Creating an instance of Adafruit PCA9685 module
pwm.set_pwm_freq(50) # Setting the PWM frequency to 50Hz

# Initializing initial PWM values for 16 servos
init_pwm0 = 351
init_pwm1 = 300
init_pwm2 = 300
init_pwm3 = 289

init_pwm4 = 300
init_pwm5 = 300
init_pwm6 = 300
init_pwm7 = 300

init_pwm8 = 300
init_pwm9 = 300
init_pwm10 = 300
init_pwm11 = 300

init_pwm12 = 300
init_pwm13 = 300
init_pwm14 = 300
init_pwm15 = 300

class ServoCtrl(threading.Thread):
# Defining a class for servo control, inheriting from threading.Thread

	def __init__(self, *args, **kwargs):
		# Constructor method for initializing servo control parameters
		self.sc_direction = [1,1,1,1, 1,1,1,1, 1,1,1,1, 1,1,1,1]     # Direction for each servo
		self.initPos = [init_pwm0,init_pwm1,init_pwm2,init_pwm3,
						init_pwm4,init_pwm5,init_pwm6,init_pwm7,
						init_pwm8,init_pwm9,init_pwm10,init_pwm11,
						init_pwm12,init_pwm13,init_pwm14,init_pwm15]     # Initial positions for servos
		self.goalPos = [300,300,300,300, 300,300,300,300 ,300,300,300,300 ,300,300,300,300]     # Target positions for servos
		self.nowPos  = [300,300,300,300, 300,300,300,300 ,300,300,300,300 ,300,300,300,300]     # Current positions for servos
		self.bufferPos  = [300.0,300.0,300.0,300.0, 300.0,300.0,300.0,300.0 ,300.0,300.0,300.0,300.0 ,300.0,300.0,300.0,300.0]
		self.lastPos = [300,300,300,300, 300,300,300,300 ,300,300,300,300 ,300,300,300,300]     # Last positions for servos
		self.ingGoal = [300,300,300,300, 300,300,300,300 ,300,300,300,300 ,300,300,300,300]     # Intended goal positions for each servo motor
		self.maxPos  = [520,520,520,520, 520,520,520,520 ,520,520,520,520 ,520,520,520,520]     # Maximum positions for servos
		self.minPos  = [100,100,100,100, 100,100,100,100 ,100,100,100,100 ,100,100,100,100]     # Minimum positions for servos
		self.scSpeed = [0,0,0,0, 0,0,0,0 ,0,0,0,0 ,0,0,0,0]     # Speed for each servo

		"""
		This is the maximum PWM value that can be sent to the servos, indicating the furthest position they can reach.
		"""
		self.ctrlRangeMax = 560 
		"""
		Thiss is the minimum PWM value that can be sent to the servos, indicating the closest position they can reach.
		"""
		self.ctrlRangeMin = 100  
		self.angleRange = 180     # Angle range
		'''
		scMode: 'init' 'auto' 'certain' 'quick' 'wiggle'
		'''
		self.scMode = 'auto'
		"""
		Duration over which the servo will complete its movement from one position to another. 
		"""
		self.scTime = 2.0  
		"""
		number of steps for servo movement. A higher number of steps typically results in smoother 
		and more precise movement.
		"""  
		self.scSteps = 30
		"""
		the time interval between each step of the servo movement. In this case, a delay of 0.037 seconds is introduced
		between each step of the servo movement.
		"""     
		self.scDelay = 0.037
		"""
		It specifies the duration of each step of the servo movement. In this case, each step of the servo 
		movement is expected to take 0.037 seconds to complete.
		"""
		self.scMoveTime = 0.0372

		self.goalUpdate = 0     # Flag to indicate goal position update 
		self.wiggleID = 0     # ID of servo for wiggling
		self.wiggleDirection = 1     # Direction of wiggling

		super(ServoCtrl, self).__init__(*args, **kwargs)     # Calling the constructor of the parent class (threading.Thread)
		self.__flag = threading.Event()      # Creating a flag for thread synchronization
		self.__flag.clear()     # Clearing the flag


	def pause(self):
		# This method pauses the servo movement.
		print('......................pause..........................')
		self.__flag.clear()


	def resume(self):
		# This method resumes the servo movement.
		print('resume')
		self.__flag.set()


	def moveInit(self):
		#This method initializes the servos to their initial positions.
		self.scMode = 'init'     #It sets the servo control mode to 'init'.
		for i in range(0,16):     #It iterates over all servos and sets them to their initial positions using PWM signals
			pwm.set_pwm(i,0,self.initPos[i])
			self.lastPos[i] = self.initPos[i]
			self.nowPos[i] = self.initPos[i]
			self.bufferPos[i] = float(self.initPos[i])
			self.goalPos[i] = self.initPos[i]
		self.pause()    #It pauses the servo movement.


	def initConfig(self, ID, initInput, moveTo):
		#This method configures the initial position for a specific servo.
		if initInput > self.minPos[ID] and initInput < self.maxPos[ID]: #It checks if the provided initial position is within the valid range for the servo.
			self.initPos[ID] = initInput #It checks if the provided initial position is within the valid range for the servo.
			
			if moveTo:     #Optionally, it moves the servo to the new initial position if moveTo is set to True.
				pwm.set_pwm(ID,0,self.initPos[ID]) 
		else:
			print('initPos Value Error.')


	def moveServoInit(self, ID):
		#This method initializes specified servos to their initial positions.
		self.scMode = 'init'     #It sets the servo control mode to 'init'.
		for i in range(0,len(ID)):     #It iterates over the list of servo IDs provided and moves each servo to its initial position.
			pwm.set_pwm(ID[i], 0, self.initPos[ID[i]])
			self.lastPos[ID[i]] = self.initPos[ID[i]]
			self.nowPos[ID[i]] = self.initPos[ID[i]]
			self.bufferPos[ID[i]] = float(self.initPos[ID[i]])
			self.goalPos[ID[i]] = self.initPos[ID[i]]
			
		self.pause()     #It pauses the servo movement.


	def posUpdate(self):  
		#This method updates the positions of servos.
		self.goalUpdate = 1     #It sets a flag to indicate that servo positions are being updated.
		for i in range(0,16):     #It updates the lastPos attribute with the current positions of servos.
			self.lastPos[i] = self.nowPos[i]
		self.goalUpdate = 0     #It clears the flag after updating.


	def speedUpdate(self, IDinput, speedInput):
		#This method updates the speed of specified servos.
		for i in range(0,len(IDinput)):
			"""
			It updates the speed of servos specified in IDinput with the corresponding speeds provided in speedInput.
			"""
			self.scSpeed[IDinput[i]] = speedInput[i]


	def moveAuto(self):
		# Smoothly moves servos in steps towards target positions.
		# Useful for continuous, smooth motion.
		for i in range(0,16):
			self.ingGoal[i] = self.goalPos[i]

		for i in range(0, self.scSteps):     #Loop through the specified number of steps for smooth movement.
			for dc in range(0,16):     #Iterate over each servo to update its position
				if not self.goalUpdate:
					# Calculate the current position of the servo based on the step.
					self.nowPos[dc] = int(round((self.lastPos[dc] + (((self.goalPos[dc] - self.lastPos[dc])/self.scSteps)*(i+1))),0))
					pwm.set_pwm(dc, 0, self.nowPos[dc]) # Set the PWM signal to move the servo to the current position.

				if self.ingGoal != self.goalPos:  # Check if the goal positions have changed during movement.
					self.posUpdate() #Updates the positions of servos.
					time.sleep(self.scTime/self.scSteps) # Wait for a short interval to allow for smooth movement.
					return 1
				
			time.sleep((self.scTime/self.scSteps - self.scMoveTime))
		# Update servo positions after completing all steps.
		self.posUpdate()
		self.pause()     #It pauses the movement after reaching the goal positions.
		return 0


	def moveCert(self):
		# Adjusts servo positions continuously based on speed and delay instead of dividing movement into steps.
		# Useful for precise, controlled movement to target positions.
		for i in range(0,16):
			self.ingGoal[i] = self.goalPos[i]
			self.bufferPos[i] = self.lastPos[i]     # Initialize ingGoal and bufferPos with current and last positions respectively.
		# Loop until current positions match the goal positions.
		while self.nowPos != self.goalPos:
			
			# Adjust servo positions based on the speed and delay.
			for i in range(0,16):
				if self.lastPos[i] < self.goalPos[i]:
					self.bufferPos[i] += self.pwmGenOut(self.scSpeed[i])/(1/self.scDelay)
					newNow = int(round(self.bufferPos[i], 0))
					
					# Ensure the position does not exceed the goal.
					if newNow > self.goalPos[i]:
						newNow = self.goalPos[i]
					self.nowPos[i] = newNow
					
				elif self.lastPos[i] > self.goalPos[i]:
					self.bufferPos[i] -= self.pwmGenOut(self.scSpeed[i])/(1/self.scDelay)
					newNow = int(round(self.bufferPos[i], 0))

					# Ensure the position does not exceed the goal.
					if newNow < self.goalPos[i]:newNow = self.goalPos[i]
					self.nowPos[i] = newNow

				if not self.goalUpdate:     # Update servo position if goal positions have not been updated during movement.
					pwm.set_pwm(i, 0, self.nowPos[i])

				if self.ingGoal != self.goalPos:
					self.posUpdate()
					return 1
				
			self.posUpdate()
			time.sleep(self.scDelay-self.scMoveTime)

		else:
			self.pause()
			return 0


	def pwmGenOut(self, angleInput):
		# Calculate PWM output based on the input angle.
		return int(round(((self.ctrlRangeMax-self.ctrlRangeMin)/self.angleRange*angleInput),0))


	def setAutoTime(self, autoSpeedSet):
		# Set the time interval for automatic movement.
		self.scTime = autoSpeedSet


	def setDelay(self, delaySet):
		# Set the delay for servo movement.
		self.scDelay = delaySet


	def autoSpeed(self, ID, angleInput):
		# Set servo positions automatically based on the input angle and direction.
		self.scMode = 'auto'
		self.goalUpdate = 1     # Flag indicating that goal positions are being updated
		
		for i in range(0,len(ID)):     
			newGoal = self.initPos[ID[i]] + self.pwmGenOut(angleInput[i])*self.sc_direction[ID[i]]
			# Ensure the goal does not exceed the maximum or minimum positions.
			if newGoal>self.maxPos[ID[i]]:
				newGoal=self.maxPos[ID[i]]
				
			elif newGoal<self.minPos[ID[i]]:
				newGoal=self.minPos[ID[i]]
				
			self.goalPos[ID[i]] = newGoal
			
		self.goalUpdate = 0     # Reset the flag
		self.resume()     # Resume movemennt


	def certSpeed(self, ID, angleInput, speedSet):
		# Set servo positions at a certain speed based on the input angle and direction.
		self.scMode = 'certain'
		self.goalUpdate = 1     # Flag indicating that goal positions are being updated
		
		for i in range(0,len(ID)):
			# Ensure the goal does not exceed the maximum or minimum positions.
			newGoal = self.initPos[ID[i]] + self.pwmGenOut(angleInput[i])*self.sc_direction[ID[i]]
			if newGoal>self.maxPos[ID[i]]:
				newGoal=self.maxPos[ID[i]]
				
			elif newGoal<self.minPos[ID[i]]:
				newGoal=self.minPos[ID[i]]
				
			self.goalPos[ID[i]] = newGoal
			
		self.speedUpdate(ID, speedSet)      # Update servo speeds
		self.goalUpdate = 0     # Reset the flag
		self.resume()      # Resume movement


	def moveWiggle(self):
		# Move a servo in a "wiggle" pattern.
		# Adjusts the servo position to create a back-and-forth movement, resembling a wiggle.
		self.bufferPos[self.wiggleID] += self.wiggleDirection*self.sc_direction[self.wiggleID]*self.pwmGenOut(self.scSpeed[self.wiggleID])/(1/self.scDelay)
		newNow = int(round(self.bufferPos[self.wiggleID], 0))
		# Ensure the position stays within the maximum and minimum limits.
		if self.bufferPos[self.wiggleID] > self.maxPos[self.wiggleID]:
			self.bufferPos[self.wiggleID] = self.maxPos[self.wiggleID]
		elif self.bufferPos[self.wiggleID] < self.minPos[self.wiggleID]:
			self.bufferPos[self.wiggleID] = self.minPos[self.wiggleID]
		self.nowPos[self.wiggleID] = newNow
		self.lastPos[self.wiggleID] = newNow
		
		# Set the PWM signal to move the servo if the position is within the limits.
		if self.bufferPos[self.wiggleID] < self.maxPos[self.wiggleID] and self.bufferPos[self.wiggleID] > self.minPos[self.wiggleID]:
			pwm.set_pwm(self.wiggleID, 0, self.nowPos[self.wiggleID])
		else:
			self.stopWiggle()  # Stop the wiggle movement if the position exceeds the limits.
		time.sleep(self.scDelay-self.scMoveTime)  # Wait for the specified delay before the next movement.
	
	def stopWiggle(self):
		# Stop the "wiggle" movement.
		self.pause()     # Update position
		self.posUpdate()     # Update position


	def singleServo(self, ID, direcInput, speedSet):
		# Move a single servo at a specified speed and direction.
		self.wiggleID = ID
		self.wiggleDirection = direcInput
		self.scSpeed[ID] = speedSet
		self.scMode = 'wiggle'
		self.posUpdate()      # Update position
		self.resume()     # Resume movement


	def moveAngle(self, ID, angleInput):
		# Move a servo to a specific angle
		self.nowPos[ID] = int(self.initPos[ID] + self.sc_direction[ID]*self.pwmGenOut(angleInput))
		# Ensure the position does not exceed the maximum or minimum positions.
		if self.nowPos[ID] > self.maxPos[ID]:
			self.nowPos[ID] = self.maxPos[ID]
			
		elif self.nowPos[ID] < self.minPos[ID]:
			self.nowPos[ID] = self.minPos[ID]
			
		self.lastPos[ID] = self.nowPos[ID]
		pwm.set_pwm(ID, 0, self.nowPos[ID])

	def scMove(self):
		# Move the servos based on the selected mode.
		if self.scMode == 'init':
			self.moveInit()
			
		elif self.scMode == 'auto':
			self.moveAuto()
			
		elif self.scMode == 'certain':
			self.moveCert()
			
		elif self.scMode == 'wiggle':
			self.moveWiggle()

	def setPWM(self, ID, PWM_input):
		# Set the PWM value for a servo.
		self.lastPos[ID] = PWM_input
		self.nowPos[ID] = PWM_input
		self.bufferPos[ID] = float(PWM_input)
		self.goalPos[ID] = PWM_input
		pwm.set_pwm(ID, 0, PWM_input)
		self.pause()     # Set the PWM value for a servo.# Set the PWM value for a servo.


	def run(self):
		# Continuously run the servo controller.
		while 1:
			self.__flag.wait()     # Wait for the flag to be set
			self.scMove()      # Move the servos
			pass
