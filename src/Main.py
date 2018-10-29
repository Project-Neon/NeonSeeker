#!/usr/bin/env python3
print("Inicializando...", end='                      \r')
import time
# from ev3dev.ev3 import *
print("ev3dev.ev3", end='                      \r')
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, MoveTank, SpeedPercent
print("motores importados", end='                      \r')
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sensor import INPUT_1, INPUT_2
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
memoria_cor= {}
cor_atual=""
tentativa=0
start_time=0
c=""
cores = pickle.load(open("Cores.p", "rb"))
Sensor_direita = ColorSensor(INPUT_2)
Sensor_esquerda = ColorSensor(INPUT_1)
Sensor_direita.mode = Sensor_direita.MODE_RGB_RAW
Sensor_esquerda.mode = Sensor_esquerda.MODE_RGB_RAW
print("Declarando tudo!", end='                      \r')
#FUNÇÔES DE LOCOMOÇÂO
def retorno(t):#função para o retorno
    global tentativa,start_time,c
    #print ('viu preto')
    rodas.on_for_seconds(20,20,t)#volta até o ultimo ponto de referencia
    tentativa+=1#indica que foi feita uma tentativa que falhou
    cor=c
    procurar_proximo()#vira conforme as orientações que são possiveis
    start_time = time.time()#reseta o timer
    sair_da_cor_atual()#anda um pouco a frente para nao o robo não reconhecer o mesmo ponto de referencia como um novo ponto

def sair_da_cor_atual():#TROCAR PELO ALINHAMENTO
    global c
    while c!='White':
        rodas.on(-20,-20)
    rodas.off()

def andar_frente():#Corrigir todos os tempos presentes aqui a fim de utilizar com o robo e pista finais
    global cor_atual,start_time,quads,c
    #Vai para frente até ver Black, retorna o tempo percorrido
    while 1:
        if(c=="Black"):
            rodas.off()
            return (time.time()-start_time)#ACERTAR ESTE CALCULO PARA A CONTAGEM COMEÇAR DO MEIO DO QUADRADO COLORIDO
        elif c!="White" and c!="Black" and start_time != 0:
            if(Confirmar_cor(c)):
                # rodas.on_for_seconds(-20,-20,2.5)
                # print ("Achou alguma cor: ",c)
                verificar_plaza()#trocar por função de indentificação do plaza
                rodas.off()
                return (time.time()-start_time)#se achar branco/cor de indicação retorna o tempo entre os pontos e para de andar
        elif c!="White" and c!="Black" and start_time==0:
                cor_atual=c
                #print(cor_atual)
                time.sleep(1.42)
                procurar_proximo()#vira se ver branco, começa o timer e continua a andar para frente
                start_time = time.time()
                sair_da_cor_atual()
                #alinhar (lembrar de descontar o tempo de alinhamento na variavel start_time)
        while c=='White':
            #while não ver o boneco
            rodas.on(-20,-20)
def virar(graus):#função de virada relativa a posiçao
        global orientacao
        if graus<0:
            rodas.on_for_seconds(-50,50,abs(graus)*(0.40/90))
        elif(graus==0): pass
        else:
            rodas.on_for_seconds(50,-50,abs(graus)*(0.40/90))

def procurar_proximo():#função de virar conforme o aprendido, ou a falta dele
    global tentativa,cor_atual,orientacao
    if (cor_atual not in  memoria_cor.keys()):
        if (90 not in memoria_cor.values() and tentativa == 0):
            #print ('tentativa0')
            virar(90)
            orientacao = 90
        if(90 in memoria_cor.values()):
            tentativa=1
        if (0 not in memoria_cor.values() and tentativa == 1):
            virar(-90)
            #print ('tentativa1')
            orientacao = 0
        if(0 in memoria_cor.values() and 90 not in memoria_cor.values() and tentativa==1):
            tentativa=2
            virar(-90)
        if (-90 not in memoria_cor.values() and tentativa == 2):
            #print ('tentativa2')
            virar(-90)
            orientacao = -90
    else:
        virar(memoria_cor[cor_atual])

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

def diferente_de(*cor):
    global c
    if c not in cor:
        return 1
    else: return 0

def cor_th():
    global c
    while(1):
        c=cor_mais_proxima(Sensor_direita.rgb)

def Confirmar_cor(cor_vista):
    global c
    time.sleep(0.08)
    if(c==cor_vista):return True
    else:return False
#FIM DAS FUNÇÕES DE COR

#FUNÇÕES DO PLAZA
def verificar_plaza():
    global c
    if c!='Black':
        mudanca = 0
        cor_momento = c
        goiaba = Thread(target=rodas.on_for_seconds, args=(-20, -20, 1.45,))
        goiaba.start()
        while(goiaba.is_alive()):
            if (cor_momento != c):
                mudanca += 1
                cor_momento = c
        if(mudanca >= 3):pass
            # print("PLAZA")
        else:pass
            # print(" NAO PLAZA")
        goiaba.join()
    rodas.off()
#FIM DAS FUNÇÕES DO PLAZA

#FUNÇÕES DA MOCHILA(EQUIPAMENTO DE CAPTURAR BONECO)

#FIM DAS FUNÇÕES DE MOCHILA

#FUNÇÕES DE INFORMAÇÃO
class quad:#objeto que guarda informações do ponto de referencia encontrado
    def __init__(self,cor,tempo,orientacao):
        self.cor = cor
        self.tempo = tempo
        self.orientacao=orientacao
#FIM DAS FUNÇÕES DE INFORMAÇÃO

print("Vamos comecar!", end='                      \r')
if __name__=="__main__":
    start_time=0
    # _thread.start_new_thread(cor_th)
    ver_cor = Thread(target=cor_th)
    ver_cor.daemon=True
    ver_cor.start()
    time.sleep(0.5)
    while (1):
        tempo = andar_frente()
        if (c=='Black'):#se ver Preto retorna até o ponto de referencia de onde saiu
            retorno(tempo)
        # se ver um novo ponto de referencia atualiza a memoria de tal cor, coloca na lista informações relativas ao descoberto e ao ultimo ligado a ele
        if (diferente_de("White", "Black")):
            tentativa=0#reseta a variavel tentativas o que indica que é um novo quadrado
            memoria_cor[cor_atual]=orientacao
            quads.append(quad(cor_atual,tempo,orientacao))
            orientacao=0
            start_time=0#reseta o timer
            ##print('achou novo')
