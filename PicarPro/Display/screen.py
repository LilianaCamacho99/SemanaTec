
from .screen import *
'''
For comprehensive insights into this module, please refer to the following link:
https://www.adeept.com/learn/detail-50.html. Additionally, it is recommended 
to extract the contents of the zip file provided on the webpage. 
For further guidance, please consult Lesson 10. Moreover, you can find relevant 
information within the module documentation enclosed within the adeeptpicarpro package.
'''

from luma.core.interface.serial import i2c     # Importing the I2C serial interface
from luma.core.render import canvas     # Importing the canvas for rendering
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106     # Importing OLED device drivers
import threading     # Importing the threading module for multi-threading support

class OLED_ctrl(threading.Thread):
    def __init__(self, t1='', t2='', t3='', t4='', t5='', *args, **kwargs):
        super(OLED_ctrl, self)._init_(*args, **kwargs)     # Calling the constructor of the superclass
        self.__flag = threading.Event()     # Used for pausing the thread
        self.__flag.set()       # Set to True
        self.__running = threading.Event()     # Used for stopping the thread
        self.__running.set()      # Set to True
        self.texts = [t1, t2, t3, t4, t5]     # Initializing text strings for OLED display

        try:
            serial = i2c(port=1, address=0x3C)     # Initializing the I2C serial interface
            self.device = ssd1306(serial, rotate=0)     # Initializing the OLED device with SSD1306 driver
        except:
            print('Screen disconnected')

    def run(self):
        while self.__running.isSet():      # Looping while the thread is running
            self.__flag.wait()      # Returns immediately if True, blocks until internal flag is True if False
            with canvas(self.device) as draw:
                for i, text in enumerate(self.texts):      # Iterating through text strings
                    draw.text((0, i * 10), text, fill="white")      # Rendering text on OLED screen
            self.pause()      # Pausing the thread after rendering

    def pause(self):
        #Pauses the OLED controller thread.
        self.__flag.clear()     # Set to False, blocks the thread

    def resume(self):
        #Resumes the OLED controller thread.
        self.__flag.set()     # Set to True, unblocks the thread

    def stop(self):
        #Stops the OLED controller thread.
        self.__flag.set()       # Resume the thread if it's paused
        self.__running.clear()      # Set to False  

    def update_texts(self, t1='', t2='', t3='', t4='', t5=''):
        #Updates the text strings displayed on the OLED screen.
        self.texts = [t1, t2, t3, t4, t5]
        self.resume()      # Resuming the thread to display updated texts
