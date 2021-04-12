print(":::LOADED:::")

import digitalio
import usb_hid
from adafruit_hid.keyboard  import Keyboard
from adafruit_hid.gamepad   import Gamepad
from time                   import sleep
import board
            
gamepad         = Gamepad(usb_hid.devices)

delaytime       = 0.0001

latch           = digitalio.DigitalInOut(board.GP4)
clock           = digitalio.DigitalInOut(board.GP5)
data            = digitalio.DigitalInOut(board.GP6)
led             = digitalio.DigitalInOut(board.GP25)

led.direction   = digitalio.Direction.OUTPUT
latch.direction = digitalio.Direction.OUTPUT
clock.direction = digitalio.Direction.OUTPUT
data.direction  = digitalio.Direction.INPUT

data.pull       = digitalio.Pull.UP

latch.value     = False
clock.value     = False
previousState   = False

buttonz         = 0

while True:
    #LATCH
    latch.value = True
    sleep(delaytime)
    latch.value = False
    sleep(delaytime)
    for x in range(0, 8, 1):
        #released
        if data.value:
            if buttonz & (1<<x):
#                print("released ",x)
                gamepad.release_buttons(x+1)
            buttonz &= ~(1<<x)
        #pressed
        else:
            if not (buttonz & (1<<x)):
#                print("pressed ",x)
                gamepad.press_buttons(x+1)
            buttonz |= (1<<x)
        #CLOCK
        clock.value = True
        sleep(delaytime)
        clock.value = False
        sleep(delaytime)
    #SIGNALING
    led.value = True if buttonz else False
