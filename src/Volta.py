
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, MoveTank, SpeedPercent
from ev3dev2.sensor.lego import ColorSensor, UltrasonicSensor
from ev3dev2.sensor import INPUT_1,INPUT_2, INPUT_3
import time
Sensor_sonic = UltrasonicSensor(INPUT_3)
Sensor_sonic.mode = Sensor_sonic.MODE_US_DIST_CM
Sensor_direita = ColorSensor(INPUT_1)
Sensor_esquerda = ColorSensor(INPUT_2)
Sensor_direita.mode = Sensor_direita.MODE_COL_COLOR
Sensor_esquerda.mode = Sensor_esquerda.MODE_COL_COLOR
rodas = MoveTank(OUTPUT_A, OUTPUT_B)
mochila = 0
memoria_cor = {
'Red':0,
'Yellow':-90,
'Green':90
}
class quad:  # objeto que guarda informações do ponto de referencia encontrado
    def __init__(self, cor):
        self.cor = cor


def virar(graus):  # função de virada relativa a posiçao
        if graus < 0:
            rodas.on_for_seconds(-50, 50, abs(graus)*(0.40/90))
        elif(graus == 0):
            pass
        else:
            rodas.on_for_seconds(50, -50, abs(graus)*(0.40/90))
def sair_da_cor_atual():  # TROCAR PELO ALINHAMENTO
    while Sensor_esquerda.color_name != 'White':
        rodas.on(-20, -20)
    rodas.off()
def procurar_passageiro():
    global mochila
    while Sensor_esquerda.color_name == 'White':
        rodas.on(-15, -15)
        if Sensor_sonic.distance_centimeters < 25 and mochila == 0:
            # regular para o robo parar com seu centro de giro alinhado com o boneco detectado
            time.sleep(0.3)
            rodas.off()
            dist = Sensor_sonic.distance_centimeters
            virar(90)
            # regular o valor de forma ao robo pegar o boneco
            rodas.on_for_seconds(-20, -20, dist*0.048)
            time.sleep(1)
            mochila = 1
            rodas.on_for_seconds(20, 20, dist*0.048)
            virar(-90)
            rodas.off()
quads = [quad('Red'), quad('Yellow'), quad('Green'), quad('Green'), quad('Yellow')]
def volta():
    global quads, mochila
    i = len(quads)-1
    while(i > 0 and mochila == 0):
        virar(memoria_cor[quads[i].cor]*-1)
        sair_da_cor_atual()
        procurar_passageiro()
        time.sleep(2.17)
        if(mochila == 1):
            virar(180)
            while(Sensor_esquerda.color_name != 'White'):
                rodas.on(-20, -20)
            rodas.off()
            break
        i -= 1
        #alinhar
        #if sensor detectar algo retorna start_time e execute a função de pegar o boneco
    if(i == 0):
        virar(180)
    rodas.off()
