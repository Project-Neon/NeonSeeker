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
cor_atual=""
tentativa=0
start_time=0
sensor1.mode = sensor1.MODE_COL_COLOR #modo detecção de  cor padrao
#função para retorno, a partir do tempo em que o robo detecta a cor do quad novo
#neste caso branco, ele se utiliza deste tempo e volta para a quad de onde saiu
# Substituir Brown por White e em locais em que aparecem White trocar pelas possibilades de cor da pista
def retorno(t):#função para o retorno
    global tentativa,,start_time
    rodas.on_for_seconds(20,20,t)#volta até o ultimo ponto de referencia
    tentativa+=1#indica que foi feita uma tentativa que falhou
    procurar_proximo()#vira conforme as orientações que são possiveis
    start_time = time.time()#reseta o timer
    rodas.on_for_seconds(-20,-20,1)#anda um pouco a frente para nao o robo não reconhecer o mesmo ponto de referencia como um novo ponto


def andar_frente():#Corrigir todos os tempos presentes aqui a fim de utilizar com o robo e pista finais
    global ,ultima_cor,cor_atual,start_time
    #Vai para frente até ver Black, retorna o tempo percorrido
    while 1:
        if  (sensor1.color_name=='White'or sensor1.color_name=='Brown') and start_time ==0:
            rodas.on(-20,-20)
            if sensor1.color_name=='White' and start_time==0:
                print ('exec white and start time==0')
                cor_atual=sensor1.color_name
                time.sleep(1.5)
                procurar_proximo()#vira se ver branco, começa o timer e continua a andar para frente
                start_time = time.time()
        elif sensor1.color_name=='Brown' and start_time!=0:
            rodas.on(-20,-20)
        elif sensor1.color_name=='White' and start_time!=0 :
            print ('exec white and start time!=0')
            rodas.on_for_seconds(-20,-20,0.5)
            rodas.off()
            return (time.time()-start_time)#se achar branco/cor de indicação retorna o tempo entre os pontos e para de andar
        elif(sensor1.color_name=="Black"):
            rodas.off()
            return (time.time()-start_time)#ACERTAR ESTE CALCULO PARA A CONTAGEM COMEÇAR DO MEIO DO QUADRADO COLORIDO
def virar(graus):#função de virada relativa a posiçao
        global orientacao
        if graus<0:
            rodas.on_for_seconds(-50,50,abs(graus)*(0.5/90))
        elif(graus==0): pass
        else:
            rodas.on_for_seconds(50,-50,abs(graus)*(0.5/90))
        orientacao += graus
        if (orientacao>=360):
            orientacao -= 360
        if (orientacao<0):
            orientacao += 360

def procurar_proximo():#corrigir para o caso de nao conhecer a cor porém conhecer 90(exemplo)
    global tentativa,cor_atual
    if (cor_atual not in  memoria_cor.keys()):
        if (90 not in memoria_cor.values() and tentativa == 0):
            virar(90)
        if (0 not in memoria_cor.values() and tentativa == 1):
            virar(-90)
        if (270 not in memoria_cor.values() and tentativa == 2):
            virar(-90)
    else:
        virar(memoria_cor[cor_atual])

class quad:#objeto que guarda informações do ponto de referencia encontrado
    def __init__(self,cor,tempo,orientacao):
        self.cor = cor
        self.tempo = tempo
        self.orientacao=orientacao

if __name__=="__main__":
    start_time=0
    while (1):
        tempo = andar_frente()
        if (sensor1.color_name=='Black'):#se ver Preto retorna até o ponto de referencia de onde saiu
            retorno(tempo)
        if (sensor1.color_name=='White'):#se ver um novo ponto de referencia atualiza a memoria de tal cor, coloca na lista informações relativas ao descoberto e ao ultimo ligado a ele
            tentativa=0#reseta a variavel tentativas o que indica que é um novo quadrado
            memoria_cor[cor_atual]=orientacao
            quads.append(quad(cor_atual,tempo,orientacao))
            start_time=0#reseta o timer
