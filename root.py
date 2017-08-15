from __future__ import division
from time import sleep
from threading import Thread
# from queue import Queue


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



class Scheduler(object):
	
	def __init__(self):
		self.cpu = None
		self.processes = []

	def add(self, process):
		self.processes.append(process)

	def pop(self):
		return self.process.pop()

	
	def start():
		for p in self.processes:
			p.start()

	def is_busy():
		pass
		
		



def fifo(processos):
	index = 0
	time_in = 0 
	turnaround = 0
	size = len(processos)

	processos.sort(key= lambda p: p['tempo_chegada'])
	print 'Comecando execucao!\n'

	t = None
	for p in processos:
		time_in = p['tempo_execucao'] + time_in
		turnaround += time_in - p['tempo_chegada']
		sleep(p['tempo_chegada'])
		t = Processo(index, p['tempo_chegada'], p['tempo_execucao'])
		t.setName(index)
		t.start()
		index += 1
	t.join()
	
	print '\n\nTurnaround: '+ str(turnaround / size)
	# Gerar grafico


def _sjf(process):
	index = 0
	time_in = 0 
	turnaround = 0
	size = len(process)


	process.sort(key= lambda p: p['tempo_chegada'])
	first = process[0]
	range_process = process[1:]
	range_process.sort(key= lambda p: p['tempo_execucao'])
	range_process.insert(0, first)
	
	t = None

	for p in range_process:
		time_in = p['tempo_execucao'] + time_in
		turnaround += time_in - p['tempo_chegada']
		sleep(p['tempo_chegada'])
		t = Processo(index, p['tempo_chegada'], p['tempo_execucao'])
		t.setName(index)
		t.start()
		index += 1
		
	t.join()

	print '\n\nTurnaround: ' + str(turnaround/size)
def rr(processos, tamanho, quantum, sobrecarga):
	processos.sort(key= lambda p: p['tempo_chegada'])
	index = 0
	turnaround = 0
	fila = processos
	time = 0
	print 'iniciando o RR'
	while (fila):
		time += quantum
		print '------------------------- RR processo %d ----------------------- \n' %(index)
		t = None
		p = fila.pop(0)
		p['tempo_execucao'] -= quantum
		t = Processo(index, p['tempo_chegada'], p['tempo_execucao'])
		t.setName(index)
		t.start()
		index += 1
		sleep(p['tempo_chegada'])
		if (p['tempo_execucao'] > 0):
			fila.append(p)
			print '\n<<<<<<<<<<<< Processo: %d volta para fila >>>>>>>>>>>>>>>' %(index)
		else:
			turnaround += (time - p['tempo_chegada'])
			print '\n<<<<<<<<<<<< Processo: %d sai da fila >>>>>>>>>>>>>>>' %(index)
		if (index == tamanho): index = 0

		t.join()
		print '\n turnaround: %d \n time: %d ' % (turnaround, time)
	print '\n turnaround FINAL %f: ' % (turnaround/tamanho)



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
		
		#FIFO
		if opcao_algoritmo == 1:
			processos = list()
			for i in range(0, quantidade_processos):
				print '\nProcesso %d:' % i
				tempo_chegada  = int(input('Tempo de chegada: '))
				tempo_execucao = int(input('Tempo de execucao: '))
				processos.append({'tempo_chegada': tempo_chegada, 'tempo_execucao':tempo_execucao})
			fifo(processos)
			break

		
		if opcao_algoritmo == 2:
			processos = list()
			for i in range(0, quantidade_processos):
				print '\nProcesso %d:' % i
				tempo_chegada  = int(input('Tempo de chegada: '))
				tempo_execucao = int(input('Tempo de execucao: '))
				processos.append({'tempo_chegada': tempo_chegada, 'tempo_execucao':tempo_execucao})
			_sjf(processos)
			break

		if opcao_algoritmo == 3:
			processos = list()
			sobrecarga = int(input('Sobrecarga: '))
			quantum = int(input('Quantum: '))
			for i in range(0, quantidade_processos):
				print '\nProcesso %d:' % i
				tempo_chegada  = int(input('Tempo de chegada: '))
				tempo_execucao = int(input('Tempo de execucao: '))
				processos.append({'tempo_chegada': tempo_chegada, 'tempo_execucao':tempo_execucao})
			rr(processos, quantidade_processos, quantum, sobrecarga)
			break
