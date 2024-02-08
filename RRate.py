import time

taps = 0
rrate = None
start = None
end = None
time_interval = None
interval_set = []
min_taps = 3
threshold = 13

while taps <= 12:
    wow = input("")
    taps += 1;
    if start is None:
        start = time.perf_counter()
    else:
        end = time.perf_counter()
        time_interval = end - start
        interval_set.append(time_interval)        
        start = time.perf_counter()
        print(time_interval)
    if len(interval_set) == min_taps:
        interval_set.sort()
        deviation = []
        for x in interval_set:
            deviation.append(abs(x - interval_set[1]) / interval_set[1] * 100)
        print("deviation", max(deviation))
        if (max(deviation) < threshold):
            rrate = 60 / interval_set[1]
            print("SUCCESS", rrate)
            break
        interval_set.pop(0)