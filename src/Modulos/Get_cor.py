import pickle
from ev3dev2.sensor.lego import ColorSensor
from math import sqrt
from ev3dev2.sensor import *

cores=pickle.load(open("Cores.p","rb"))
Sensor_direita = ColorSensor(INPUT_1)
Sensor_esquerda = ColorSensor(INPUT_2)
Sensor_direita.mode = Sensor_direita.MODE_RGB_RAW
Sensor_esquerda.mode = Sensor_esquerda.MODE_RGB_RAW

def media(leitura1,leitura2):#FAZ A MÈDIA DAS LEITURAS DOS AMBOS SENSORES, NÂO USAR NO ALINHAMENTO
    media=[]
    for x in range(3):
        media.append((leitura1[x]+leitura2[x])/2)
    return tuple(media)

def cor_mais_proxima(leitura):
    global cores
    min = 1000
    for valor in cores.values():
        dist = sqrt(((leitura[0]-valor[0])**2) + ((leitura[1]-valor[1])**2)+((leitura[2]-valor[2])**2))#DISTANCIA EUCLIDIANA DO VALOR DA LEITURA DO SENSOR QUE FOI USADO COMO ENTRADA COM OS VALORES DAS CORES CALIBRADAS PREVIAMENTE
        if(dist<min):#verifica se é menor que o ultimo verificado
             min = dist
             for key,value in cores.items():#pega o nome da cor que gerou a menor distancia
                 if value == valor: cor = key

    return cor#RETORNA A COR COM O VALOR MAIS PROXIMO DA LEITURA
# while(1):
#     cor=cor_mais_proxima(media(Sensor_direita.rgb,Sensor_esquerda.rgb))
#     print(cor,end='         \r')
