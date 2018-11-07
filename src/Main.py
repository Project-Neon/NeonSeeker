#!/usr/bin/env python3
print("Inicializando...", end='                      \r')
import time
# from ev3dev.ev3 import *
print("ev3dev.ev3", end='                      \r')
from ev3dev2.motor import OUTPUT_A, OUTPUT_B,OUTPUT_C, MoveTank, SpeedPercent, LargeMotor
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
Mochila=LargeMotor(OUTPUT_C)
quads = []
orientacao = 0
# memoria_cor= {}
memoria_cor = {}
plaza=False
cor_atual=""
tentativa=0
c=""
mochila=False
velocidade=20
cores = pickle.load(open("Cores.p", "rb"))
Sensor_direita = ColorSensor(INPUT_2)
Sensor_esquerda = ColorSensor(INPUT_4)
Sensor_direita.mode = Sensor_direita.MODE_RGB_RAW
Sensor_esquerda.mode = Sensor_esquerda.MODE_RGB_RAW
Sensor_sonic = UltrasonicSensor(INPUT_3)
Sensor_sonic.mode=Sensor_sonic.MODE_US_DIST_CM
print("Declarando tudo!", end='                      \r')
#FUNÇÔES DE LOCOMOÇÂO
def retorno():#função para o retorno
    global tentativa,c,cor_atual,velocidade
    while c!=cor_atual:
        rodas.on(SpeedPercent(velocidade),SpeedPercent(velocidade))
        if c!= 'White': Confirmar_cor(c)
    #tempo para a parada no meio do quadrado
    rodas.on_for_seconds(SpeedPercent(velocidade), SpeedPercent(velocidade), 8/SpeedPercent(velocidade))
    #8 é o fator de tempo para ele voltar até o meio do quadrado, Se aumentar ele volta mais para tras
    rodas.off()
    tentativa+=1#indica que foi feita uma tentativa que falhou
    procurar_proximo()#vira conforme as orientações que são possiveis
    alinha(0.02,230,30)#anda um pouco a frente para nao o robo não reconhecer o mesmo ponto de referencia como um novo ponto

def alinha(Kp,target,margem):
    global d
    erroE=1
    erroD=1
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
        outputD = erroD* (Kp+0.01)
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

def andar_frente():#Corrigir todos os tempos presentes aqui a fim de utilizar com o robo e pista finais
    global cor_atual,tentativa,quads,c,plaza,memoria_cor
    #Vai para frente até ver Black, retorna o tempo percorrido
    while 1:
        if(c=="Black"):
            rodas.off()
            retorno()
            return
        elif c!="White" and c!="Black":
            if(Confirmar_cor(c)):
                verificar_plaza()
                if(len(quads)>0 and plaza==False):memoria_cor[cor_atual]=orientacao
                if(plaza==False):quads.append(c)
                cor_atual=c
                print('ACHEI: ',cor_atual)
                tentativa=0
                rodas.off()
                procurar_proximo()
                alinha(0.02,230,30)
                return
        while c=='White':
            #Anda pelo branco em procura do boneco se a mochila nao esta carregada(mochila==0).Senão apenas anda para frente no branco
            procurar_passageiro()

def virar(graus):#função de virada relativa a posiçao
#0.666 é o fator de tempo da virada, alterar para virar 90 graus corretamente e caso mude a velocidade de virada, mude-o de acordo
        if graus<0:
            rodas.on_for_rotations(-40,40,abs(graus)*(0.666/90))
        elif(graus==0): pass
        else:
            rodas.on_for_rotations(40,-40,abs(graus)*(0.666/90))#FROM HELL

def procurar_proximo():#função de virar conforme o aprendido, ou a falta dele
    global tentativa,cor_atual,orientacao
    if (cor_atual not in  memoria_cor.keys()):
        if (tentativa == 0):
            virar(90)
            orientacao = 90
        if (tentativa == 1):
            virar(-90)
            orientacao = 0
        if (tentativa == 2):
            virar(-90)
            orientacao = -90
    else:virar(memoria_cor[cor_atual])
#Essa função deve conseguir servir para 4 casos(Oque aparecer na lista é o que ele deve tentar pois não conhece):
#1:Direita->Frente->Esquerda(Não conhece nada)
#2:Direita->Esquerda(conhece frente/0)
#3:Frente->Esquerda(conhece direita/90)
#4:Esquerda(conhece direita/90 e frente/0)

#FIM DAS FUNÇÔES DE LOCOMOÇÂO

#FUNÇÕES DE COR
def media(leitura1, leitura2):  # FAZ A MÈDIA DAS LEITURAS DOS AMBOS SENSORES
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
    global c,d
    while(1):
        c=cor_mais_proxima(Sensor_direita.rgb)
        d=Sensor_direita.rgb

def Confirmar_cor(cor_vista):
    global c
    time.sleep(0.1)
    if(c==cor_vista):return True
    else:return False
#FIM DAS FUNÇÕES DE COR

#FUNÇÕES DO PLAZA
def verificar_plaza():
    global c, mochila, quad, cor_atual, plaza,velocidade
    if(1):
        if c!='Black':
            mudanca = 0
            cor_momento = c
            goiaba = Thread(target=rodas.on_for_seconds, args=(-15, -15, 32.22/15,))#32.22 =fator de tempo para o mesmo ir até o meio do quadrado COLORIDO
#Caso altere a velocidade de 15(Caso nao esteja conseguindo subir a rampa), diminua esse fator de acordo
            goiaba.start()
            while(goiaba.is_alive()):
                print("Checando plaza: ",mudanca)
                if (cor_momento != c):
                    mudanca += 1
                    cor_momento = c
            if(mudanca >= 2):
                print("PLAZA")
                pickle.dump(quads,open('memoria.p','wb'))#Armazena os quadrados vistos para debugs futuros
                plaza=True #Plaza encontrado
                quads.append(quad(cor_atual))#coloca o ultimo quadrado antes do plaza no array
                tempo=time.time()
                while(c!='Black'):
                    rodas.on(-(SpeedPercent(velocidade)*1.35), -(SpeedPercent(velocidade)*1.35))
                    if(diferente_de('Black','White')):
                        if(Confirmar_cor(c)):
                            rodas.off()
                            return
                if(plaza==True):
                    rodas.off()
                    time.sleep(49.5/SpeedPercent(velocidade))#esse tempo serve para ele voltar alem das faixas do plaza, não é necessario alterar
                    par=mochila
                    solte()#deixa o BONECO
                    mochila=False
                    rodas.on_for_seconds((SpeedPercent(velocidade)*1.35), (SpeedPercent(velocidade)*1.35), time.time()-tempo)
                    while(c=="White"):rodas.on(SpeedPercent(velocidade),SpeedPercent(velocidade))
                    rodas.on_for_seconds(SpeedPercent(velocidade), SpeedPercent(velocidade), 8/SpeedPercent(velocidade))
                    #8 deve ser o mesmo fator de tempo do retorno
                    rodas.off()
                    if par==True:Mochila_sobe()
                    virar(180)
                    Volta()
            else:pass
            goiaba.join()
        rodas.off()

def Volta():
    global quads,mochila,start_time,c,velocidade
    i=len(quads)-2#Indice para o robo ir somente até o ultimo quadrado
    while(i>0 and mochila==False):#Se quiser que o robo vá até o ultimo: Tire a condição da mochila
        if c!='White':
            print(memoria_cor[c])
            virar((memoria_cor[c])*(-1))
            alinha(0.02,230,30)
        procurar_passageiro()
        time.sleep(35.22/SpeedPercent(velocidade))#Mesmo fator de tempo do verificar_plaza(ENTRADA DE COLORIDO)
        rodas.off()
        if(mochila==True ):
            virar(90)
            virar(90)
            alinha(0.02,230,30)
            while(c!='White'):rodas.on(-SpeedPercent(velocidade),-SpeedPercent(velocidade))
            rodas.off()
            break
        i-=1
            #if sensor detectar algo retorna start_time e execute a função de pegar o boneco
    if(i==0):
        virar(90)
        virar(90)
        while(c!='White'):rodas.on(-SpeedPercent(velocidade),-SpeedPercent(velocidade))
    rodas.off()
    procurar_passageiro()
    verificar_plaza()
#FIM DAS FUNÇÕES DO PLAZA

#FUNÇÕES DA MOCHILA(EQUIPAMENTO DE CAPTURAR BONECO)
def procurar_passageiro():
    global mochila,c,velocidade
    while c == 'White':
        rodas.on(-SpeedPercent(velocidade), -SpeedPercent(velocidade))
        if Sensor_sonic.distance_centimeters<30 and mochila==0 :
            rodas.off()
            pega()

def Mochila_desce():
    Mochila.on_for_rotations(SpeedPercent(20), 0.53) ## negativo sobe
def Mochila_solta():
    Mochila.on_for_rotations(SpeedPercent(20),0.25)
def Mochila_pega():
    Mochila.on_for_rotations(SpeedPercent(-20), 0.25)
def Mochila_sobe():
    Mochila.on_for_rotations(SpeedPercent(-20), 0.53)

def solte():
    global mochila
    rodas.off()
    if(mochila==True):
        Mochila_solta()

def pega():
    global mochila
    dist = Sensor_sonic.distance_centimeters
    time.sleep(0.5)
    rodas.off()
    Mochila_desce()
    virar(90)
    time.sleep(1)
    rodas.on_for_seconds(-20,-20,dist*0.05)#regular o valor de forma ao robo pegar o boneco
    Mochila_pega()
    time.sleep(1)
    mochila=True
    rodas.on_for_seconds(20,20,dist*0.05)
    virar(-90)
    rodas.off()

#FIM DAS FUNÇÕES DE MOCHILA

#FUNÇÕES DE INFORMAÇÃO
class quad:#objeto que guarda informações do ponto de referencia encontrado
    def __init__(self,cor):
        self.cor = cor
        # self.tempo = tempo
        # self.orientacao=orientacao
#FIM DAS FUNÇÕES DE INFORMAÇÃO

print("Vamos comecar!", end='                      \r')
if __name__=="__main__":
    start_time=0
    plaza = False
    ver_cor = Thread(target=cor_th)
    ver_cor.daemon=True
    ver_cor.start()
    time.sleep(0.5)
    Mochila_sobe()
    while (1):
        andar_frente()
        # if (tuts=0):#se ver Preto retorna até o ponto de referencia de onde saiu
        #     retorno()
        # # se ver um novo ponto de referencia atualiza a memoria de tal cor, coloca na lista informações relativas ao descoberto e ao ultimo ligado a ele
        # if (tuts=1):
        #     print ('Achei: ',c)
        #     tentativa=0#reseta a variavel tentativas o que indica que é um novo quadrado
        #     if(plaza==False and len(quads)>0):
        #         memoria_cor[cor_atual]=orientacao
        #         quads.append(quad(cor_atual))
