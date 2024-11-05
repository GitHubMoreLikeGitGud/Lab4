import RPi.GPIO as GPIO
from time import sleep, time
from hal.hal_input_switch import init as init_switch, read_slide_switch
from hal.hal_led import init as init_led, set_output

# Initialize the switch and LED
init_switch()
init_led()

def blink_led(frequency, duration=None):
    """
    Blink the LED at the specified frequency.
    If duration is specified, blink for that duration, then turn off.
    """
    interval = 1 / (2 * frequency)  # Interval for half a period (on and off)
    start_time = time()
    
    while duration is None or (time() - start_time) < duration:
        set_output(24, True)  # Turn on LED
        sleep(interval)
        set_output(24, False)  # Turn off LED
        sleep(interval)

def main():
    try:
        while True:
            switch_position = read_slide_switch()
            
            if switch_position == 0:
                # Left position: Blink at 5 Hz continuously
                blink_led(frequency=5, duration=0.2)  # Blink 5 times per second
            else:
                # Right position: Blink at 10 Hz for 5 seconds, then turn off
                blink_led(frequency=10, duration=5)
                set_output(24, False)  # Ensure LED is turned off after 5 seconds
                
            # Small delay to avoid rapid polling
            sleep(0.1)

    except KeyboardInterrupt:
        # Cleanup GPIO settings on program exit
        GPIO.cleanup()

# Run the main function to execute the program
main()
