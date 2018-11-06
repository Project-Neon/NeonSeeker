#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor,OUTPUT_C, SpeedPercent
Mochila = LargeMotor(OUTPUT_C)
def Mochila_desce():
    Mochila.on_for_rotations(SpeedPercent(20), 0.53) ## negativo sobe
def Mochila_solta():
    Mochila.on_for_rotations(SpeedPercent(20),0.15)
def Mochila_pega():
    Mochila.on_for_rotations(SpeedPercent(-20), 0.15)
def Mochila_sobe():
    Mochila.on_for_rotations(SpeedPercent(-20), 0.53)
def set_mochila(cond): ## Define se temos um boneco ou não
	self.cond=cond
def get_mochila():     ## Caso True ele entra no plaza    
	return cond        ## Caso False ele não entra no plaza
