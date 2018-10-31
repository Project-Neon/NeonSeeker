print("Importando motores...", end='                      \r')
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, MoveTank, SpeedPercent
print("Importando sensores...", end='                      \r')
from ev3dev2.sensor.lego import ColorSensor,UltrasonicSensor
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3
import time
print("ATIVADO!!", end='                      \r')
rodas=MoveTank(OUTPUT_A,OUTPUT_B)
Sensor_direita = ColorSensor(INPUT_2)
Sensor_infra = UltrasonicSensor(INPUT_3)
Sensor_infra.mode=Sensor_infra.MODE_US_DIST_CM
Sensor_direita.mode = Sensor_direita.MODE_COL_COLOR
while(1):
    while Sensor_direita.color_name == 'White':
        while Sensor_infra.distance_centimeters>30:
            rodas.on(-20,-20)
        if Sensor_infra.distance_centimeters<30:
            print("ACHEI!!:",Sensor_infra.distance_centimeters)
            time.sleep(0.2)
            rodas.off()
