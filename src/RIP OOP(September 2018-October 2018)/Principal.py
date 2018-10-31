#!/usr/bin/env python3
from ev3dev2.sensor import *
from ev3dev.ev3 import *
from time import sleep
from ev3dev2.motor import OUTPUT_A,OUTPUT_B,MoveTank,SpeedPercent

import Anda as go
import mapa as ma

rodas=MoveTank(OUTPUT_A,OUTPUT_B)
Sensor1 = ColorSensor(INPUT_1)
Sensor1.mode = Sensor_esquerda.MODE_RGB_RAW


Car = go.Anda()
Circuito = ma.Mapa()
class principal:
        def main():
                cor_atual = sensor1.value()
                if(cor_atual <131 and cor_atual>120):
                        Car.frente()
                if(cor_atual <14 and cor_atual > 0):
                        Car.virar(180)
                elif(): # vemos uma cor diferente de Preto ou branco
                        Circuito.procura(cor_atual)
        if __name__== "__main__":
                main()



