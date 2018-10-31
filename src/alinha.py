#!/usr/bin/env python3
import time
from ev3dev.ev3 import *
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, MoveTank, SpeedPercent
from ev3dev2.sensor.lego import ColorSensor
rodas=MoveTank(OUTPUT_A,OUTPUT_B) #motor A = direita e motor B = esquer$

Sensor_direita = ColorSensor(INPUT_1)
Sensor_esquerda = ColorSensor(INPUT_2)
Sensor_direita.mode= Sensor_direita.MODE_RGB_RAW
Sensor_esquerda.mode = Sensor_esquerda.MODE_RGB_RAW

def alinha(Kp,target,margem):
        erroE=1
        erroD=1
        while(erroE != 0 or erroD != 0) :

                atualD = Sensor_direita.rgb[0]+Sensor_direita.rgb[1]+Sensor_direita.rgb[2]
                erroD=atualD - target 
                if abs(erroD)<margem:
                        erroD=0
                outputD = erroD* Kp 

                atualE = Sensor_esquerda.rgb[0]+Sensor_esquerda.rgb[1]+Sensor_esquerda.rgb[2]
                erroE=atualE - target
                if abs(erroE)<margem:
                        erroE=0
                outputE = erroE* Kp

                if outputE>40:
                        outputE = 40
                elif outputE<-40:
                        outputE=-40
                
                if outputD>40:
                        outputD = 40

                if erroE == 0 and erroD == 0:
                        rodas.off()
                else:
                        rodas.on(outputE,outputD)
        rodas.off()
        print(erroE)
        print("foi")
        print(erroD)
        time.sleep(3)


while(1):
        alinha(0.02,230,30)

        