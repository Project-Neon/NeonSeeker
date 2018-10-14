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
def retorno(t):
    global tentativa,ida
    ida=0
    rodas.on_for_seconds(20,20,t)
    tentativa+=1
    procurar_proximo()
def andar_frente():
    global ida;
    g=0
    ida=1
    start_time=0
    #run_forever until sees a color different than white,returns traveled time
    # start_time=0
    #time.sleep(1)
    while 1:
        global ultima_cor,cor_atual
        if  (sensor1.color_name=='White'or sensor1.color_name=='Brown') and start_time ==0:
            rodas.on(-20,-20)
            if sensor1.color_name=='White' and start_time==0:
                time.sleep(1)
                cor_atual=sensor1.color_name
                procurar_proximo()
                start_time = time.time()
                # print ("executou")
        elif sensor1.color_name=='Brown' and start_time!=0:
            rodas.on(-20,-20)
        elif sensor1.color_name=='White' and start_time!=0 and g ==1:
            # print ('exec')
            return (time.time()-start_time)
            rodas.off()
        elif sensor1.color_name=='White' and start_time!=0 and g == 0:
            rodas.on(-20,-20)
            if (sensor1.color_name!=cor_atual): g =1
        elif(sensor1.color_name=="Black"):
            elapsed_time=(time.time()-start_time)
            #ACERTAR ESTE CALCULO PARA A CONTAGEM COMEÇAR DO MEIO DO QUADRADO COLORIDO
            rodas.off()
            # print (start_time)
            return elapsed_time

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

def procurar_proximo():
    global tentativa
    if (sensor1.color_name not in  memoria_cor):
        if (90 not in memoria_cor.values() and tentativa == 0):
            virar(90)
        if (0 not in memoria_cor.values() and tentativa == 1):
            virar(-90)
        if (270 not in memoria_cor.values() and tentativa == 2):
            virar(-90)
    else:
        virar(memoria_cor[sensor1.color_name])

class quad:
    def __init__(self,cor,tempo,orientacao):
        self.cor = cor
        self.tempo = tempo
        self.orientacao=orientacao

if __name__=="__main__":
    while (1):
        tempo = andar_frente()
        if (sensor1.color_name=='Black' or sensor1.color_name=="No color"):
            retorno(tempo)
        if (sensor1.color_name=='White' and ida==1):
            tentativa=0
            memoria_cor[cor_atual]=orientacao
            quads.append(quad(cor_atual,tempo,orientacao))
