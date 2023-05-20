import usb.core
import usb.util
import RPi.GPIO as GPIO

# USB HMI device information
vendor_id = 0x1234  # Replace with the actual vendor ID of your USB HMI device
product_id = 0x5678  # Replace with the actual product ID of your USB HMI device

# GPIO pins for PWM output
x_pin = 18  # Replace with the actual GPIO pin number for X-axis PWM output
y_pin = 19  # Replace with the actual GPIO pin number for Y-axis PWM output

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(x_pin, GPIO.OUT)
GPIO.setup(y_pin, GPIO.OUT)
x_pwm = GPIO.PWM(x_pin, 100)  # PWM frequency of 100 Hz for X-axis
y_pwm = GPIO.PWM(y_pin, 100)  # PWM frequency of 100 Hz for Y-axis

# Find the USB HMI device
device = usb.core.find(idVendor=vendor_id, idProduct=product_id)

if device is None:
    raise ValueError("USB HMI device not found.")

# Set up USB device for mouse input
usb.util.claim_interface(device, 0)

try:
    while True:
        # Read USB HMI mouse data
        data = device.read(0x81, 8)  # Endpoint address and data size may vary

        # Extract X and Y axis data
        x_axis = data[1]
        y_axis = data[2]

        # Map mouse data to PWM duty cycle (0-100%)
        x_duty = (x_axis / 255) * 100
        y_duty = (y_axis / 255) * 100

        # Update PWM signals
        x_pwm.ChangeDutyCycle(x_duty)
        y_pwm.ChangeDutyCycle(y_duty)

except KeyboardInterrupt:
    pass

finally:
    # Release USB interface and clean up GPIO
    usb.util.release_interface(device, 0)
    usb.util.dispose_resources(device)
    x_pwm.stop()
    y_pwm.stop()
    GPIO.cleanup()
