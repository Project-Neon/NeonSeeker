class volta(quad):
	anti_direcao
	def __init__ (self,cor,direcao)
		super().__init__(cor)
		if(direcao == 1): #1 está relacionado com a esquerda
			self.anti_direcao = -1
		elif(direcao == -1): #1 está relacionado com a direita
			self.anti_direcao = 1
		elif(direcao == 0): #1 está relacionado com a frente
			self.anti_direcao = 0
