import time
def volta():
    global quads
    i=len(quads)-1
    while(achado!=1):
        virar(memoria_cor[quads[i].cor]*-1)
        start_time=time.time()
        #alinhar
        while start_time != quads[i-1].tempo:
            rodas.on(-20,-20)
            #if sensor detectar algo retorna start_time e execute a função de pegar o boneco
        rodas.off()