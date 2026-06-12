import time
import board
import pwmio
import digitalio

# --- SETUP DISTANCE SENSOR (3.3V) ---
trig = digitalio.DigitalInOut(board.GP14)
trig.direction = digitalio.Direction.OUTPUT
echo = digitalio.DigitalInOut(board.GP15)
echo.direction = digitalio.Direction.INPUT
echo.pull = None 

# --- SETUP LED ---
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# --- SETUP SWITCH ---
start_button = digitalio.DigitalInOut(board.GP1)
start_button.direction = digitalio.Direction.INPUT
start_button.pull = digitalio.Pull.UP

# --- PWM VALUES ---
s = 4915  # Stop
f = 6000  # Forward 
b = 3830  # Backward (adjusted to f=6000)
t = 4260  # Turn

# --- SETUP MOTORS ---
pwm_left = pwmio.PWMOut(board.GP22, frequency=50, duty_cycle=s)
pwm_right = pwmio.PWMOut(board.GP28, frequency=50, duty_cycle=s)

# --- SENSORS ---
def distance():
    trig.value = False
    time.sleep(0.01) # Short settling period before measurement
    trig.value = True
    time.sleep(0.00001)
    trig.value = False

    t_max = time.monotonic() + 0.03
    while not echo.value:
        if time.monotonic() > t_max: return 500
    
    t_0 = time.monotonic()
    while echo.value:
        if time.monotonic() > t_max: return 500
    t_1 = time.monotonic()
    
    return (t_1 - t_0) * 17150

# --- ACTUATORS ---
def blink(count):
    for i in range(count):
        led.value = True
        time.sleep(0.1)
        led.value = False
        time.sleep(0.1)
        
def stop(): 
    pwm_left.duty_cycle = s 
    pwm_right.duty_cycle = s
    time.sleep(0.1)

def forward(): 
    pwm_left.duty_cycle = f
    pwm_right.duty_cycle = b

def turn(): 
    # Turns on the spot
    pwm_left.duty_cycle = t
    pwm_right.duty_cycle = t
    time.sleep(0.3) 
    stop()


# --- MAIN PROGRAM ---
stop() # Initial stop

while True:
    # Switch is ON
    if not start_button.value:
        d = distance()
        
        if d < 10: 
            stop() 
            blink(3)
            turn()
            stop()
            
        else:
            forward()
    else:
        # Switch is OFF
        stop()
        led.value = False

time.sleep(0.05)
