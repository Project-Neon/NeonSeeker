from threading import Thread
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, MoveTank, SpeedPercent
import Get_cor
rodas = MoveTank(OUTPUT_A, OUTPUT_B)

def verificar_plaza():
    mudanca=0
    cor_momento = Get_cor.cor_mais_proxima(Get_cor.media(Get_cor.Sensor_direita.rgb, Get_cor.Sensor_esquerda.rgb))
    goiaba=Thread(target=rodas.on_for_seconds,args=(-30,-30,1.45,))
    goiaba.start()
    while(goiaba.is_alive()):
        if (cor_momento!=Get_cor.cor_mais_proxima(Get_cor.media(Get_cor.Sensor_direita.rgb,Get_cor.Sensor_esquerda.rgb))):
            mudanca+=1
            cor_momento=Get_cor.cor_mais_proxima(Get_cor.media(Get_cor.Sensor_direita.rgb, Get_cor.Sensor_esquerda.rgb))
    if(mudanca>=3):
        print("PLAZA")
    else: print(" NAO PLAZA")
