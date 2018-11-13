import time
import datetime
from gpiozero import PWMLED

led = PWMLED(6)

led.on()
time.sleep(3)  # the led should be lit
#led.off()  # the led should go off
led.value = 0.5  # the led should be lit at half brightness
while True:
	pass