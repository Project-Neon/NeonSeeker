#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
from time import sleep
m = LargeMotor(OUTPUT_A)


a=0.6
while (True):
        print("desce")
        m.on_for_rotations(SpeedPercent(20), a) ## negativo sobe
        sleep(a)
        print("Dorme")
        m.off()
        sleep(2)
        print("sobe")
        m.on_for_rotations(SpeedPercent(-20), a)
        sleep(a)
        print("Dorme")
        m.off()
        sleep(2)






