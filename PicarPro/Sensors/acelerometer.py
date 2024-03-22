'''
For further information about this module, please consult 
the following link: https://www.adeept.com/learn/tutorial-260.html. 
Additionally, you may refer to the module documentation included in 
the adeeptpicarpro package.
'''

from mpu6050 import mpu6050     # Import the MPU6050 class from the mpu6050 module

class Accelerometer:
    def __init__(self, address=0x68):
        # Initialize the Accelerometer object with the specified I2C address
        self.sensor = mpu6050(address)

    def test(self, num_readings=10):
        # Initialize variables to store the sum of acceleration data
        x_sum = 0
        y_sum = 0
        z_sum = 0

        # Iterate over a specified number of readings
        for _ in range(num_readings):
            # Get the accelerometer data from the sensor
            accelerometer_data = self.sensor.get_accel_data()
            # Accumulate the x, y, and z acceleration values
            x_sum += accelerometer_data['x']
            y_sum += accelerometer_data['y']
            z_sum += accelerometer_data['z']

        # Calculate the average acceleration values
        x_avg = "{:.3f}".format(x_sum / num_readings)
        y_avg = "{:.3f}".format(y_sum / num_readings)
        z_avg = "{:.3f}".format(z_sum / num_readings)

        # Return the averaged gravitational acceleration at X, Y, and Z axes.
        return x_avg, y_avg, z_avg



