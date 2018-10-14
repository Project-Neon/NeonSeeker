#!/usr/bin/env python3
import time
from ev3dev2.sensor import *
from ev3dev.ev3 import *
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.motor import OUTPUT_A,OUTPUT_B,MoveTank,SpeedPercent
rodas=MoveTank(OUTPUT_A,OUTPUT_B)
sensor1=ColorSensor(INPUT_1)
quads = []
orientacao = 0
memoria_cor= {}
ida=0
cor_atual=""
tentativa=0
sensor1.mode = sensor1.MODE_COL_COLOR #modo detecção de  cor padrao
#função para retorno, a partir do tempo em que o robo detecta a cor do quad novo
#neste caso branco, ele se utiliza deste tempo e volta para a quad de onde saiu
def virar(graus):
        global orientacao
        if graus<0:
            rodas.on_for_seconds(-50,50,abs(graus)*(0.5/90))
        else:
            rodas.on_for_seconds(50,-50,abs(graus)*(0.5/90))
        orientacao += graus
        if (orientacao>=360):
            orientacao -= 360
        if (orientacao<0):
            orientacao += 360
def anda_frente():
    global cor_atual
    start_time=time.time()
    while(1):
        if(sensor1.color_name=='Brown'):
            rodas.on(-20,-20)
        elif(sensor1.color_name=='White'):
            rodas.on_for_seconds(-20,-20,0.5)
            rodas.off()
            cor_atual="White"
            return time.time()-start_time
        elif(sensor1.color_name=='Black'):
            rodas.off()
            cor_atual="Black"
            return time.time()-start_time

def retorno(t):
    while(sensor1.color_name!="White"):
        rodas.on(20,20)
    rodas.off()
def Procurar():
       global tentativa
       if(tentativa==0):
           virar(90)
           rodas.on_for_seconds(-20,-20,0.5)
           tentativa=1
       elif(tentativa==1):
           virar(-90)
           rodas.on_for_seconds(-20,-20,0.5)
           tentativa=2
       elif(tentativa==2):
           virar(-90)
           rodas.on_for_seconds(-20,-20,0.5)
if __name__=="__main__":
    while (1):
        if(sensor1.color_name=="Brown"):
            tempo = anda_frente()
        if (sensor1.color_name=='Black'):
            retorno(tempo+0.5)
        if (sensor1.color_name=='White' and cor_atual!="Branco"):
            Procurar()
        if(sensor1.color_name=="White"and cor_atual=="Branco"):
            if(tentativa!=0): tentativa =0
            Procurar()
