#!/usr/bin/env python3
from ev3dev2.sensor import *
from ev3dev.ev3 import *
from time import sleep
from ev3dev2.motor import OUTPUT_A,OUTPUT_B,MoveTank,SpeedPercent
sensor1.mode = sensor1.MODE_COL_COLOR
class Anda:
        def __init__():
                rodas=MoveTank(OUTPUT_A,OUTPUT_B)
                print("HEAVY ENGINE READY!!")

        def virar(graus):#fun    o de virada relativa a posi  ao
                if graus<0:
                    rodas.on_for_seconds(-50,50,abs(graus)*(0.5/90))
                elif(graus==0): pass
                else:
                    rodas.on_for_seconds(50,-50,abs(graus)*(0.5/90))

        def stop():
                rodas.on(0,0)
        def frente():
                rodas.on(-20,-20)






