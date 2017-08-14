from time import sleep
from threading import Thread


class Processo(Thread):
	def __init__(self, id, tempo_chegada, tempo_execucao):
		Thread.__init__(self)
		self.id = id
		self.tempo_chegada = tempo_chegada
		self.tempo_execucao = tempo_execucao
 
	def run(self):
		print '\nProcesso %d: Chegando em %d' % (self.id, self.tempo_chegada)
		sleep(self.tempo_execucao)
		# print 'Processo %d: Iniciando execucao em %d' % (self.id, self.tempo_chegada)
		print '\nProcesso %d: Finalizou execucao em %d' % (self.id, self.tempo_execucao)



def fifo(processos):
	turnaround = 0
	processos.sort(key= lambda p: p['tempo_chegada'])
	index = 0
	print 'Comecando execucao!\n'

	t = None
	for p in processos:
		turnaround += p['tempo_execucao'] - p['tempo_chegada']
		sleep(p['tempo_chegada'])
		t = Processo(index, p['tempo_chegada'], p['tempo_execucao'])
		t.setName(index)
		t.start()
		index += 1
	t.join()
	
	print '\n\nTurnaround: %d' % turnaround
	# Gerar grafico


if __name__ == "__main__":
	
	opcao_algoritmo = input("""
	Informe qual o algoritmo desejado:
		1 - FIFO
		2 - SJF
		3 - Round Robin
		4 - Prioridades
		5 - EDF
	""")

	quantidade_processos = int(input('Qual a quantidade de processos?'))

	print 'Informe os dados dos processos:'
	while 0 < opcao_algoritmo  < 6:
		if opcao_algoritmo == 1: #FIFO
			processos = list()
			for i in range(0, quantidade_processos):
				print '\nProcesso %d:' % i
				tempo_chegada  = int(input('Tempo de chegada: '))
				tempo_execucao = int(input('Tempo de execucao: '))
				processos.append({'tempo_chegada': tempo_chegada, 'tempo_execucao':tempo_execucao})

			fifo(processos)
			break
