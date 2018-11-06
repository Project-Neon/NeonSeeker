#!/usr/bin/env python3
print("Importando motores...", end='                      \r')
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, MoveTank, SpeedPercent
print("Importando sensores...", end='                      \r')
from ev3dev2.sensor.lego import ColorSensor,UltrasonicSensor
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3
import time
import Mochila
print("ATIVADO!!", end='                      \r')
rodas=MoveTank(OUTPUT_A,OUTPUT_B)
Sensor_direita = ColorSensor(INPUT_2)
Sensor_infra = UltrasonicSensor(INPUT_3)
Sensor_infra.mode=Sensor_infra.MODE_US_DIST_CM
Sensor_direita.mode = Sensor_direita.MODE_COL_COLOR
mochila=0
def virar(graus):#função de virada relativa a posiçao
        if graus<0:
            rodas.on_for_rotations(-40,40,abs(graus)*(0.566/90))
        elif(graus==0): pass
        else:
            rodas.on_for_rotations(40,-40,abs(graus)*(0.566/90))#FROM HELL
Mochila.Mochila_sobe()
while(1):
    while Sensor_direita.color_name == 'White':
        print(Sensor_infra.distance_centimeters)
        rodas.on(-15,-15)
        if Sensor_infra.distance_centimeters<30 and mochila==0 :
            dist = Sensor_infra.distance_centimeters
            time.sleep(0.5)
            rodas.off()
            Mochila.Mochila_desce()
            virar(90)
#regular para o robo parar com seu centro de giro alinhado com o boneco detectado
            time.sleep(1)
            rodas.on_for_seconds(-20,-20,dist*0.05)#regular o valor de forma ao robo pegar o boneco
            Mochila.Mochila_pega()
            time.sleep(1)
            mochila=1
            rodas.on_for_seconds(20,20,dist*0.05)
            virar(-90)
            rodas.off()
    if Sensor_direita.color_name=="Black":
        rodas.off()
        if(mochila==1):
            Mochila.Mochila_solta()
            time.sleep(3.3)
            rodas.on_for_seconds(20,20,2)
            Mochila.Mochila_sobe()
            mochila=0
