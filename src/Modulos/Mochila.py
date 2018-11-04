from ev3dev2.motor import LargeMotor, OUTPUT_C
Garra=LargeMotor(OUTPUT_C)

rotacoes=0.6

def Mochila_desca():
    Garra.on_for_rotation(20,0.6)
    Garra.off()

def Mochila_pegue():
    Garra.on_for_rotations(-20,0.6)
    Garra.off()