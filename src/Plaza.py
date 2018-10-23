from threading import Thread
def verificar_plaza():
    mudanca=0
    cor_momento=sensor1.color_name
    goiaba=Thread(target=rodas.on_for_seconds,args=(-20,-20,2,))
    goiaba.start()
    while(goiaba.is_alive()):
        if (cor_momento!=sensor1.color_name):
            mudanca+=1
            cor_momento=sensor1.color_name
    if(mudanca>=3):
        print("È O PLAZA")
    else: print("NÃO É O PLAZA")

    
