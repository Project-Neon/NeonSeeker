#!/usr/bin/env python3
from ev3dev2.sensor import *
from ev3dev.ev3 import *
from time import sleep
class Anda:
	def __init__():
		mA = LargeMotor(OUTPUT_A)
		mB = LargeMotor(OUTPUT_B)
		print("HEAVY ENGINE READY!!")
	def stop():
		mA.run_forever(speed_sp=0)
		mB.run_forever(speed_sp=0)		
	def vira90(): ## Descobrir qual lado é 90
		mA.run_forever(speed_sp=-500)
		mB.run_forever(speed_sp=500)
		## Descobrir Quanto tempo ele tem que ser mantido
		sleep(1)
	def vira-90(): ## Descobrir qual lado é -90
		mA.run_forever(speed_sp=500)
		mB.run_forever(speed_sp=-500)
		## Descobrir Quanto tempo ele tem que ser mantido
		sleep(1)
		#stop()
	def vira180(): ## Descobrir qual lado é -90
		mA.run_forever(speed_sp=500)
		mB.run_forever(speed_sp=-500)
		## Descobrir Quanto tempo ele tem que ser mantido
		sleep(2)
		stop()
	def frente():
		mA.run_forever(speed_sp=900)
		mB.run_forever(speed_sp=900)
	##def alinhamento()
		## Descobrir como faz o alinhamento
		
