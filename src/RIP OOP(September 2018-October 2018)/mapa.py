
from time import sleep
from ev3dev2.motor import OUTPUT_A,OUTPUT_B,MoveTank,SpeedPercent

import Anda as go
import mapa as ma
rodas=MoveTank(OUTPUT_A,OUTPUT_B)
class mapa: # com regra da mao direita
        memoria_cor = {}
        Car = go.Anda()
        def intervalo(max,min,valor):
                if(valor > min and valor < max):
                        return True
                return False
        def testa(graus):
                rodas.on_for_seconds(-20,-20,1)
                Car.virar(graus)
                rodas.on_for_seconds(-20,-20,1)
                while(intervalo(cor_recebida-5,cor_recebida+5,sensor1.value())  or intevalo(131,120,cor_recebidsensor1.value()) or intevalo(1$
                        if(cor_atual <131 and cor_atual>120):
                                Car.frente()
                        if(cor_atual <14 and cor_atual > 0):
                                Car.virar(180)
                                break
                        else:
                                memoria_cor[cor_recebida] = graus
                                return 0
                                break

        def procura(cor_recebida): # Aqui quer dizer que ele viu uma nova cor
                boolean = 1
                graus = 90
                for i in memoria_cor.keys():
                        if i - 5 < cor_recebida and i + 5 > cor_recebida:
                                boolean = 2
                                break
                if(boolean == 1 and graus not in memoria_cor.values()):
                        boolean = testa(graus)
                graus -=90
                elif(boolean == 1 and graus not in memoria_cor.values()):
                        boolean = testa(graus)
                graus -=90
                elif(boolean == 1 and graus not in memoria_cor.values()):
                        boolean = testa(graus)
        	if(boolean == 2):
                	Car.virar(memoria_cor[cor_recebida])

                return 1
