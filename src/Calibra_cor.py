from ev3dev2.button import Button
from ev3dev2.sound import Sound
from ev3dev2.sensor.lego import ColorSensor
from Get_cor import media
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

for cor in cores.keys():
    print (f'Coloque Dora no {cor}, e aperte qualquer botão para prosseguir',end="     \r")
    while not btn.any():pass
    Sound.speak('A cor ',cor,' foi adicionada com sucesso')
    cores[cor]=media(Sensor_direita.rgb,Sensor_esquerda.rgb)
print('Todas as cores registradas\nSalvando arquivo Cores.p...\nSaindo',end='\r')
pickle.dump(cores,open('Cores.p','wb'))




