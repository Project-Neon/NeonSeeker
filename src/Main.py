from ev3dev2.sensor import *
from ev3dev.ev3 import *
import ev3dev2.motor as ev3m
import ev3dev2.sensor.lego as sensor
rodas=ev3m.MoveTank(ev3m.OUTPUT_A,ev3m.OUTPUT_B)
sensor1=sensor.ColorSensor(INPUT_1)
def andar_frente:
    #run_forever until sees a color different than white
    while sensor1.color==6 or sensor1.color==0:
        rodas.on(60,60)

def virar(graus):

    if graus == 90:
        rodas.on(50,-50,1)
    if graus == -90 or graus== 270:
        rodas.om(-50,50,1)

if __name__=="__main__":
    virar(90)
    andar_frente()    
