from machine import Pin
import time
# GPIO is the internal built-in LED
led = Pin(15, Pin.OUT)
# input on the lower left of the Pico using a built-in pull-down resistor to keep the value from floating
button = Pin(17, Pin.IN, Pin.PULL_DOWN)
rrate = None
start = None
end = None
time_interval = None
interval_set = []
min_taps = 3
threshold = 13
taps=0

while taps <= 12:
    if button.value(): # if the value changes
        led.toggle()
        time.sleep(1) # wait 1/10th of a second
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
                    exit()
                if rrate > 140:
                    print("baby is hyperventilating")
                    exit()
                print("SUCCESS", rrate)
                exit()
            interval_set.pop(0)
            
print("Inconsistent")

