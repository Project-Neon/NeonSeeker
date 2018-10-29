#!/usr/bin/env python3
import ev3dev2.fonts as fonts
from ev3dev2.button import Button
from time import sleep
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sensor import INPUT_1, INPUT_2
from ev3dev2.display import Display
import pickle
display=Display()
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
def imprime(frase):
    display.clear()
    display.draw.text((10, 10),frase, font=fonts.load('charBI24'))

def media(leitura1,leitura2):#FAZ A MÈDIA DAS LEITURAS DOS AMBOS SENSORES, NÂO USAR NO ALINHAMENTO
    media=[]
    for x in range(3):
        media.append((leitura1[x]+leitura2[x])/2)
    return tuple(media)

for cor in cores.keys():
    frase = "Coloque na cor: {}".format(cor)
    imprime(frase)
    print("Coloque na cor:",cor)
    while not btn.any():pass
    cores[cor]=media(Sensor_direita.rgb,Sensor_esquerda.rgb)
    sleep(2)
imprime('Todas as cores registradas')
imprime('Salvando arquivo Cores.p...')
pickle.dump(cores,open('Cores.p','wb'))
imprime('Saindo')
