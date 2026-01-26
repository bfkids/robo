import time
import board
import pwmio
import digitalio

# --- SETUP SENSOR (3.3V) ---
trig = digitalio.DigitalInOut(board.GP14)
trig.direction = digitalio.Direction.OUTPUT
echo = digitalio.DigitalInOut(board.GP15)
echo.direction = digitalio.Direction.INPUT
echo.pull = None 

# --- SETUP LED ---
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# --- SETUP SCHALTER ---
start_button = digitalio.DigitalInOut(board.GP1)
start_button.direction = digitalio.Direction.INPUT
start_button.pull = digitalio.Pull.UP

# --- PWM WERTE ---
s = 4915  # Stopp
v = 6000  # Vorwärts rechts
r = 3830  # Vorwärts links (angepasst an v=6000)
k = 4260  # Kurve

# --- MOTOREN SETUP ---
pwm_links = pwmio.PWMOut(board.GP22, frequency=50, duty_cycle=s)
pwm_rechts = pwmio.PWMOut(board.GP28, frequency=50, duty_cycle=s)

# --- FUNKTIONEN SENSOR ---

def distanz():
    trig.value = False
    time.sleep(0.01) # Kurze Beruhigungspause vor Messung
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

def blink(anzahl):
    for i in range(anzahl):
        led.value = True
        time.sleep(0.1)
        led.value = False
        time.sleep(0.1)

# --- FUNKTIONEN BEWEGUNG ---

def stop(): 
    pwm_links.duty_cycle = s 
    pwm_rechts.duty_cycle = s
    time.sleep(0.3)

def vor(): 
    pwm_links.duty_cycle = r
    pwm_rechts.duty_cycle = v

def kurve(): 
    # Dreht auf der Stelle
    pwm_links.duty_cycle = k
    pwm_rechts.duty_cycle = k
    time.sleep(0.3) 
    stop()


# --- HAUPTPROGRAMM ---
stop() # Initialer Stopp

while True:
    # Schalter ist EIN
    if not start_button.value:
        d = distanz()
        
        if d < 20: # Wenn Hindernis näher als 20cm
            stop()
            blink(3) 
            kurve()
            stop()
            
        else:
            vor()
    else:
        # Schalter ist AUS
        stop()
        led.value = False
    

