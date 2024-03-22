from picarpro.display import screen  # Imports the screen module from picarpro.display package
import time  # Imports the time module

screen = screen.OLED_ctrl(t1='GEWBOT.COM', t2='IP:CONNECTING', t3='<ARM> OR <PT> MODE', t4='MPU6050 DETECTING', t5='FUNCTION OFF')  # Instantiates an OLED control object with specified texts
screen.start()  # Starts the OLED control thread
time.sleep(5)  # Pauses for 5 seconds
screen.update_texts(t1='Changing', t2='Texts')  # Updates the displayed texts
time.sleep(5)  # Pauses for 5 seconds
screen.stop()  # Stops the OLED control thread
