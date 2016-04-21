import os, time

for x in range (0,100):
    os.system("aplay -Dplug:default -r 176400 sethkara.wav")
    time.sleep(1)