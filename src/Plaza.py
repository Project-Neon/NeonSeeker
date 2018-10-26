from threading import Thread
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, MoveTank, SpeedPercent
import Get_cor
rodas = MoveTank(OUTPUT_A, OUTPUT_B)

def verificar_plaza():
    mudanca=0
    cor_momento = Get_cor.cor_mais_proxima(Get_cor.media(Get_cor.Sensor_direita, Get_cor.Sensor_esquerda))
    goiaba=Thread(target=rodas.on_for_seconds,args=(-20,-20,2,))
    goiaba.start()
    while(goiaba.is_alive()):
        if (cor_momento!=Get_cor.cor_mais_proxima(Get_cor.media(Get_cor.Sensor_direita,Get_cor.Sensor_esquerda))):
            mudanca+=1
            cor_momento=Get_cor.cor_mais_proxima(Get_cor.media(Get_cor.Sensor_direita, Get_cor.Sensor_esquerda))
    if(mudanca>=3):
        print("È O PLAZA")
    else: print("NÃO É O PLAZA")

    
