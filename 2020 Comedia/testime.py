from time import sleep, time

safety_timer = time()
sleep(5)
elapsed_time = time() - safety_timer
print(int(elapsed_time))