import time
import datetime
from gpiozero import PWMLED

led = PWMLED(10)
led.on()
time.sleep(3)
led.off()
while True:
	pass
