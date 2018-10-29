#!/usr/bin/env python3
from ev3dev2.button import Button
from ev3dev2.sound import Sound
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sensor import *
from time import sleep
import pickle
btn = Button()
cores = {
    'Red': (),
    'Green': (),
    'Yellow': (),
    'White': (),
    'Black': (),
}
Sensor_direita = ColorSensor(INPUT_1)
Sensor_esquerda = ColorSensor(INPUT_2)
Sensor_direita.mode= Sensor_direita.MODE_RGB_RAW
Sensor_esquerda.mode = Sensor_esquerda.MODE_RGB_RAW

def media(leitura1,leitura2):#FAZ A MÈDIA DAS LEITURAS DOS AMBOS SENSORES, NÂO USAR NO ALINHAMENTO
    media=[]
    for x in range(3):
        media.append((leitura1[x]+leitura2[x])/2)
    return tuple(media)

for cor in cores.keys():
    print("Coloque na cor:",cor)
    while not btn.any():pass
    #Sound.speak('A cor ',cor,' foi adicionada com sucesso')
    cores[cor]=media(Sensor_direita.rgb,Sensor_esquerda.rgb)
    sleep(2)
print('Todas as cores registradas\nSalvando arquivo Cores.p...\nSaindo',end='\r')
pickle.dump(cores,open('Cores.p','wb'))
