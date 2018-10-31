#!/usr/bin/env python3
from ev3dev.ev3 import *
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, MoveTank, SpeedPercent
from ev3dev2.button import Button

rodas=MoveTank(OUTPUT_A,OUTPUT_B)
botao=Button()
para=1.00
print('Pronto')
while(1):
        while not botao.any():pass
        print("Tentei rodar por: ",para," segundos")
        rodas.on_for_seconds(-20,-20,1.45)
        para+=0.1
        rodas.on_for_seconds(-50,50,0.42)
