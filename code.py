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

# --- SETUP SCHALTER ---
start_button = digitalio.DigitalInOut(board.GP1)
start_button.direction = digitalio.Direction.INPUT
start_button.pull = digitalio.Pull.UP

# --- PWM WERTE ---
s = 4915  # Stopp
v = 6000  # Vorwärts
r = 3830  # Rückwärts
k = 4260  # Kurve

# --- MOTOREN SETUP ---
pwm_links = pwmio.PWMOut(board.GP22, frequency=50, duty_cycle=s)
pwm_rechts = pwmio.PWMOut(board.GP28, frequency=50, duty_cycle=s)

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

# --- BEWEGUNGS-FUNKTIONEN MIT PAUSEN ---
def stop(): 
    pwm_links.duty_cycle = s 
    pwm_rechts.duty_cycle = s
    time.sleep(0.3)

def vor(): 
    pwm_links.duty_cycle = v
    pwm_rechts.duty_cycle = r

def kurve(): 
    # Dreht auf der Stelle
    pwm_links.duty_cycle = k
    pwm_rechts.duty_cycle = k
    time.sleep(0.3) # Dauer der Drehung
    stop()

# --- HAUPTPROGRAMM ---
stop()

while True:
    # Die Logik aus deinem funktionierenden Dioden-Code
    if not start_button.value:
        d = distanz()
        
        if d < 20: # Wenn Hindernis näher als 15cm
            stop()
            kurve()
            stop()
            
        else:
            vor()
    else:
        # Schalter ist AUS
        pwm_links.duty_cycle = s
        pwm_rechts.duty_cycle = s
    
