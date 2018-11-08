#!/usr/bin/env python3
#FUNÇÂO DE CALIBRAÇÂO
#COLOCAR AS CORES DA PISTA
#SE A PISTA NAO TIVER YELLLOW TIRE O Yellow
#SE NECESSARIO CALIBRAR UM COR PARA  ROBO NAO CAIR
#CRIE ESSA COR COM QUALQUER NOME E CALIBRE NORMALMENTE
#NO PROGRAMA PRINCIPAL CHAMAR ESSA COR PELO NOME DADO AQUI
import ev3dev2.fonts as fonts
from ev3dev2.button import Button
from time import sleep
from ev3dev2.sensor import INPUT_4, INPUT_2
from ev3dev.ev3 import *
from ev3dev2.sensor.lego import ColorSensor
import pickle
import os
os.system('setfont Lat15-TerminusBold32x16')
btn = Button()
cores = {
    'Red': (),
    'Green': (),
  #  'Yellow': (),
    'White': (),
    'Black': (),
    'Blue':(),
    'DarkBlue':(),
    'LightGreen':(),
}
Sensor_direita = ColorSensor(INPUT_4)
Sensor_esquerda = ColorSensor(INPUT_2)
Sensor_direita.mode= Sensor_direita.MODE_RGB_RAW
Sensor_esquerda.mode = Sensor_esquerda.MODE_RGB_RAW
def mostre(frase):
    print(frase,end = '                                           \r')

def media(leitura1,leitura2):#FAZ A MÈDIA DAS LEITURAS DOS AMBOS SENSORES, NÂO USAR NO ALINHAMENTO
    media=[]
    for x in range(3):
        media.append((leitura1[x]+leitura2[x])/2)
    return tuple(media)

for cor in cores.keys():
    frase = "Coloque na cor: {}".format(cor)
    mostre(frase)
    print("Coloque na cor:",cor)
    Sound.speak(cor)
    while not btn.any():pass
    cores[cor]=media(Sensor_direita.rgb,Sensor_esquerda.rgb)
    sleep(1)
mostre('Todas as cores registradas')
mostre('Salvando arquivo Cores.p...')
pickle.dump(cores,open('Cores.p','wb'))
mostre('Saindo')
