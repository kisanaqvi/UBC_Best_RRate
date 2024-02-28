from machine import Pin
import time

# GPIO is the internal built-in LED
onboard_led = Pin(25, Pin.OUT)
onboard_led.high()
time.sleep(1)
onboard_led.low()
# input on the lower left of the Pico using a built-in pull-down resistor to keep the value from floating
button = Pin(11, Pin.IN, Pin.PULL_DOWN)
led_blue = Pin(8, Pin.OUT)
led_green = Pin(12, Pin.OUT)
led_white = Pin(15, Pin.OUT)
led_yellow = Pin(14, Pin.OUT)
rrate = None
start = None
end = None
time_interval = None
interval_set = []
min_taps = 3
threshold = 13
taps=0
on = False

#external execution loop
#device is always listening for inputs
while 1:
    
    # wait to turn on device until long press recieved
    while on != True:
        #if an input recieved, check that it is longer than 1.5 secs (a long press)
        if button.value():
            beginning = time.ticks_ms()
            while button.value():
                time.sleep(1/10)
            ending = time.ticks_ms()
            total = ending - beginning
            print("total",total)
            # if press is greater than 1.5 seconds, turn on device (turn bool on to true) and proceed to rrate tracking
            if(total > 1000):
                on = True
                led_white.high()
                time.sleep(1) # wait 1/10th of a second
                led_white.low()
                time.sleep(1)
        total = 0
                
    
    # while device is on, it is always waiting to start a new rrate measurement
    while taps <= 12:
        #wait for a tap
            if button.value():
                #if its a long press, turn off the device
                beginning = time.ticks_ms()
                while button.value():
                    time.sleep(1/10)
                ending = time.ticks_ms()
                total = ending - beginning
                #if press is greater than 1.5 seconds, turn off device
                if(total > 1000):
                    on = False
                    break
                total = 0

                #if its a short press, begin rrate tracking
                led_blue.high()
                time.sleep(1) # wait 1/10th of a second
                led_blue.low()
                time.sleep(1)
                taps += 1
                if start is None:
                    start = time.ticks_ms()
                else:
                    end = time.ticks_ms()
                    time_interval = end - start
                    interval_set.append(time_interval)        
                    start = time.ticks_ms()
                    print(time_interval)
                if len(interval_set) == min_taps:
                    interval_set.sort()
                    deviation = []
                    for x in interval_set:
                        deviation.append(abs(x - interval_set[1]) / interval_set[1] * 100)
                    print("deviation", max(deviation))
                    if (max(deviation) < threshold):
                        rrate = 60000 / interval_set[1]
                        if rrate < 2:
                            print("baby is not breathing")
                        elif rrate > 140:
                            print("baby is hyperventilating")
                        else:
                            print("SUCCESS", rrate)
                            led_green.high()
                            time.sleep(1)
                            led_green.low()
                            time.sleep(1)
                    else:
                        print("Inconsistent")
                        led_yellow.high()
                        time.sleep(1)
                        led_yellow.low()
                        time.sleep(1)
                    
                    #reset values for a new rrate measurement
                    interval_set.clear()
                    deviation.clear()
                    taps = 0
                    rrate = None
                    start = None
                    end = None
                    time_interval = None
                    
                
        #will now wait for a tap to begin execution again