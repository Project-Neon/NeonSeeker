from ev3dev2.sensor import *
from ev3dev.ev3 import *
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.motor import OUTPUT_A,OUTPUT_B,MoveTank
rodas=MoveTank(OUTPUT_A,OUTPUT_B)
sensor1=ColorSensor(INPUT_1)
sensor1.mode = sensor1.MODE_COL_COLOR #modo detecção de  cor padrao
def andar_frente:
    #run_forever until sees a color different than white
    while sensor1.color==6 or sensor1.color==0:
        rodas.on(60,60)

def virar(graus):

    if graus == 90:
        rodas.on(SpeedPercent(50),SpeedPercent(-50),1)
    if graus == -90:
        rodas.on(SpeedPercent(-50),SpeedPercent(50),1)
    if graus = 180:
        rodas,on(SpeedPercent(50),SpeedPercent(-50),2)
    else:
        pass

if __name__=="__main__":
    virar(90)
    sleep(5)
    andar_frente()
