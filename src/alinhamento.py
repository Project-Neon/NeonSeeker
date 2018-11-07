#!/usr/bin/env python3
print("Inicializando...", end='                      \r')
import time
# from ev3dev.ev3 import *
print("ev3dev.ev3", end='                      \r')
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, MoveTank, SpeedPercent
print("motores importados", end='                      \r')
from ev3dev2.sensor.lego import ColorSensor,UltrasonicSensor
from ev3dev2.sensor import INPUT_4, INPUT_2, INPUT_3
print("Sensores importados", end='                      \r')
from threading import Thread
from math import sqrt
import pickle
print("threading, math e pickle importados", end='                      \r')
time.sleep(1)
print("Importacoes concluidas!", end='                      \r')
#DECLARAÇÃO DE VARIAVEIS GLOBAIS
rodas=MoveTank(OUTPUT_A,OUTPUT_B)
quads = []
orientacao = 0
# memoria_cor= {}
memoria_cor = {}
plaza=False
cor_atual=""
tentativa=0
start_time=0
c=""
mochila=0
cores = pickle.load(open("Cores.p", "rb"))
Sensor_direita = ColorSensor(INPUT_2)
Sensor_esquerda = ColorSensor(INPUT_4)
Sensor_direita.mode = Sensor_direita.MODE_RGB_RAW
Sensor_esquerda.mode = Sensor_esquerda.MODE_RGB_RAW
Sensor_sonic = UltrasonicSensor(INPUT_3)
Sensor_sonic.mode=Sensor_sonic.MODE_US_DIST_CM
print("Declarando tudo!", end='                      \r')
#FUNÇÔES DE LOCOMOÇÂO


def alinha(Kp,target,margem):
    print('ALINHANDO')
    global e,d
    erroE=1
    erroD=1
    #rodas.on_for_seconds(-20,-20,0.8)
    if c == 'White':
        while c=='White':
            rodas.on(15,15)
        rodas.off()
    else:
        while c!='White':
            rodas.on(-15,-15)
        rodas.off()
    while(erroE != 0 or erroD != 0) :
        atualD = d[0]+d[1]+d[2]
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
    while c!='White':
        rodas.on(-20,-20)
        time.sleep(0.3)
        rodas.off()


#FIM DAS FUNÇÔES DE LOCOMOÇÂO

#FUNÇÕES DE COR
def media(leitura1, leitura2):  # FAZ A MÈDIA DAS LEITURAS DOS AMBOS SENSORES, NÂO USAR NO ALINHAMENTO
    media = []
    for x in range(3):
        media.append((leitura1[x]+leitura2[x])/2)
    return tuple(media)

def cor_mais_proxima(leitura):
    global cores
    min = 1000
    for valor in cores.values():
        # DISTANCIA EUCLIDIANA DO VALOR DA LEITURA DO SENSOR QUE FOI USADO COMO ENTRADA COM OS VALORES DAS CORES CALIBRADAS PREVIAMENTE
        dist = sqrt(((leitura[0]-valor[0])**2) +
                    ((leitura[1]-valor[1])**2)+((leitura[2]-valor[2])**2))
        if(dist < min):  # verifica se é menor que o ultimo verificado
             min = dist
             for key, value in cores.items():  # pega o nome da cor que gerou a menor distancia
                 if value == valor:
                     cor = key
    return cor


def cor_th():
    global c,e,d
    while(1):
        c=cor_mais_proxima(Sensor_direita.rgb)
        d=Sensor_direita.rgb
        # if(c=='Black' and plaza ==False):rodas.off()

def Confirmar_cor(cor_vista):
    global c
    time.sleep(0.1)
    if(c==cor_vista):return True
    else:return False
#FIM DAS FUNÇÕES DE COR

if __name__=="__main__":
    # _thread.start_new_thread(cor_th)
    ver_cor = Thread(target=cor_th)
    ver_cor.daemon=True
    ver_cor.start()
    time.sleep(0.5)

    while (1):
        alinha(0.02,230,15)
        print("Foi")


