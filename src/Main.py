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
# Substituir White por verde e em locais em que aparecem verde trocar pelas possibilades de cor da pista
def retorno(t):#função para o retorno
    global tentativa,start_time
    print ('viu preto')
    
    rodas.on_for_seconds(20,20,t)#volta até o ultimo ponto de referencia
    tentativa+=1#indica que foi feita uma tentativa que falhou
    cor=sensor1.color_name
    procurar_proximo()#vira conforme as orientações que são possiveis
    start_time = time.time()#reseta o timer
    sair_da_cor_atual(cor)#anda um pouco a frente para nao o robo não reconhecer o mesmo ponto de referencia como um novo ponto

def sair_da_cor_atual(cor):#TROCAR PELO ALINHAMENTO
    while sensor1.color_name==cor:
        rodas.on(-20,-20)
    rodas.off()

def andar_frente():#Corrigir todos os tempos presentes aqui a fim de utilizar com o robo e pista finais
    global cor_atual,start_time,quads
    #Vai para frente até ver Black, retorna o tempo percorrido
    while 1:    
        if diferente_de("White","Black") and start_time==0:
                cor_atual=sensor1.color_name
                print(cor_atual)
                if not quads[0]: time.sleep(2.5)
                procurar_proximo()#vira se ver branco, começa o timer e continua a andar para frente
                start_time = time.time()
                sair_da_cor_atual(cor_atual)
                #alinhar (lembrar de descontar o tempo de alinhamento na variavel start_time)
        elif sensor1.color_name=='White':
            #while não ver o boneco
            rodas.on(-20,-20)
        elif diferente_de("White", "Black") and start_time != 0:
            rodas.on_for_seconds(-20,-20,2.5)#trocar por função de indentificação do plaza
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
        #orientacao += graus
        #if (orientacao>=360):
           # orientacao -= 360
        #if (orientacao<0):
            #orientacao += 360

def procurar_proximo():#função de virar conforme o aprendido, ou a falta dele
    global tentativa,cor_atual,orientacao
    if (cor_atual not in  memoria_cor.keys()):
        if (90 not in memoria_cor.values() and tentativa == 0):
            print ('tentativa0')
            virar(90)
            orientacao = 90
        if(90 in memoria_cor.values()):
            tentativa=1;
        if (0 not in memoria_cor.values() and tentativa == 1):
            virar(-90)
            print ('tentativa1')
            orientacao = 0
        if(0 in memoria_cor.values() and 90 not in memoria_cor.values() and tentativa==1):
            tentativa=2;
            virar(-90)
        if (-90 not in memoria_cor.values() and tentativa == 2):
            print ('tentativa2')
            virar(-90)
            orientacao = -90
    else:
        virar(memoria_cor[cor_atual])

def diferente_de(*cor):
    if sensor1.color_name not in cor:
        return 1
    else: return 0

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
        # se ver um novo ponto de referencia atualiza a memoria de tal cor, coloca na lista informações relativas ao descoberto e ao ultimo ligado a ele
        if (diferente_de("White", "Black")):
            tentativa=0#reseta a variavel tentativas o que indica que é um novo quadrado
            memoria_cor[cor_atual]=orientacao
            quads.append(quad(cor_atual,tempo,orientacao))
            orientacao=0
            start_time=0#reseta o timer
            print('achou novo')
