#!/usr/bin/env python3
import ev3dev2.fonts as fonts
from ev3dev2.button import Button
from time import sleep
from ev3dev2.sensor import INPUT_1, INPUT_2
from ev3dev2.sensor.lego import ColorSensor
import pickle
import os
os.system('setfont Lat15-TerminusBold32x16')
btn = Button()
cores = {
    'Red': (),
    'Green': (),
    'Yellow': (),
    'White': (),
    'Black': (),
    'Blue':(),
}
Sensor_direita = ColorSensor(INPUT_1)
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
