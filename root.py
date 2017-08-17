# from __future__ import division
from time import sleep
from threading import Thread
import json 
import webbrowser

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

def _sjf(process, size):
	index = 0
	time_in = 0 
	turnaround = 0

	process.sort(key= lambda p: p['tempo_chegada'])
	first = process[0]
	range_process = process[1:]
	range_process.sort(key= lambda p: p['tempo_execucao'])
	range_process.insert(0, first)
	
	t = None

	for p in range_process:
		time_in = p['tempo_execucao'] + time_in
		turnaround += time_in + - p['tempo_chegada']
		sleep(p['tempo_chegada'])
		t = Processo(index, p['tempo_chegada'], p['tempo_execucao'])
		t.setName(index)
		t.start()
		index += 1

	t.join()

	print '\n\nTurnaround: ' + str(turnaround/float(size))

def _round__robin(process, size, quantum, sobrecarga):
	index = 0
	time_in = 0 
	turnaround = 0
	time_split = 0

	processos.sort(key= lambda p: p['tempo_chegada'])
	print processos

	t = None

	for p in processos:
		time_split_div = p['tempo_execucao'] / quantum
		time_split_mod = p['tempo_execucao'] % quantum

		if time_split_div == 0:
			time_in = p['tempo_execucao'] + time_in 
		else :
			if time_split_mod == 0:
				time_in = p['tempo_execucao'] + time_in + (time_split_div * sobrecarga) -1
			else:
				time_in = p['tempo_execucao'] + time_in + (time_split_div * sobrecarga) 

		turnaround += time_in - p['tempo_chegada']
		sleep(p['tempo_chegada'])
		t = Processo(index, p['tempo_chegada'], p['tempo_execucao'])
		t.setName(index)
		t.start()
		index += 1

	t.join()

	print '\n\nTurnaround: ' + str(turnaround/size)

def _prioridade(process, size):
	index = 0
	time_in = 0 
	turnaround = 0

	process.sort(key= lambda p: p['tempo_chegada'])
	first = process[0]
	range_process = process[1:]
	range_process.sort(key= lambda p: p['tempo_prioridade'])
	range_process.insert(0, first)

	t = None

	for p in range_process:
		time_in = p['tempo_execucao'] + time_in
		turnaround += time_in + - p['tempo_chegada']
		sleep(p['tempo_chegada'])
		t = Processo(index, p['tempo_chegada'], p['tempo_execucao'])
		t.setName(index)
		t.start()
		index += 1

	t.join()

	print '\n\nTurnaround: ' + str(turnaround/float(size))

def get_lower_priority(process):

	if not process:
		return False

	small = float("inf") 
	
	for p in process:
		if p['tempo_prioridade'] < small :
			small = p['tempo_prioridade']
			chosen = p

	return chosen

def remove_process(process):

	for p in process:
		if p['tempo_execucao'] <=0 :
			process.remove(p)
	return process
def initialize_list_result(process):
	result = []
	for p in process:
		result.append({'id': p['id'], 'time_exc': p['tempo_chegada'], 'time_in': 0})
	return result

def add_to_process(process, time_in, result):	
	for p in result:
		if process["id"] == p["id"]:
			p['time_in'] =  time_in
			break
	return result

def _edf(process, size, quantum, sobrecarga):

	index = 0
	time_in = 0 
	turnaround = 0

	process.sort(key= lambda p: p['tempo_chegada'])
	first = process[0]
	range_process = process[1:]
	range_process.sort(key= lambda p: p['tempo_prioridade'])
	range_process.insert(0, first)
	p = first
	result = initialize_list_result(range_process) 

	while True:
		if p['tempo_execucao'] > quantum:
			time_in = quantum + time_in + sobrecarga 
		else:
			time_in = p['tempo_execucao'] + time_in

		sleep(p['tempo_chegada'])
		t = Processo(index, p['tempo_chegada'], time_in)
		t.setName(index)
		t.start()
		index += 1
		
		p['tempo_execucao'] = p['tempo_execucao'] - quantum
		result = add_to_process(p, time_in, result)
		range_process = remove_process(range_process) 
		p = get_lower_priority(range_process)
		if not p:
			break
	t.join()
	for p in result:
		turnaround += p['time_in'] - p['time_exc']

	print '\n\nTurnaround: ' + str(turnaround/size)
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
			print processos
			# fifo(processos)
			break

		if opcao_algoritmo == 2: #SJF
			processos = list()
			for i in range(0, quantidade_processos):
				print '\nProcesso %d:' % i
				tempo_chegada  = int(input('Tempo de chegada: '))
				tempo_execucao = int(input('Tempo de execucao: '))
				processos.append({'tempo_chegada': tempo_chegada, 'tempo_execucao':tempo_execucao})
			_sjf(processos, quantidade_processos)
			break

		if opcao_algoritmo == 3: #Round Robin
			processos = list()
			for i in range(0, quantidade_processos):
				print '\nProcesso %d:' % i
				tempo_chegada  = int(input('Tempo de chegada: '))
				tempo_execucao = int(input('Tempo de execucao: '))
				processos.append({'tempo_chegada': tempo_chegada, 'tempo_execucao':tempo_execucao})
			quantum = int(input('Qual o valor do Quantum?'))
			sobrecarga = int(input('Qual o valor da Sobrecarga?'))

			_round__robin(processos, quantidade_processos, quantum, sobrecarga)
			break
		if opcao_algoritmo == 4: #Prioridade
			processos = list()
			for i in range(0, quantidade_processos):
				print '\nProcesso %d:' % i
				tempo_chegada  = int(input('Tempo de chegada: '))
				tempo_execucao = int(input('Tempo de execucao: '))
				tempo_prioridade = int(input('Prioridade: '))
				processos.append({'tempo_chegada': tempo_chegada, 'tempo_execucao':tempo_execucao, 'tempo_prioridade': tempo_prioridade})
			_prioridade(processos, quantidade_processos)
			break

		if opcao_algoritmo == 5: #EDF
			processos = list()
			id = 0
			for i in range(0, quantidade_processos):
				print '\nProcesso %d:' % i
				tempo_chegada  = int(input('Tempo de chegada: '))
				tempo_execucao = int(input('Tempo de execucao: '))
				tempo_prioridade = int(input('Prioridade: '))
				processos.append({'id': id,'tempo_chegada': tempo_chegada, 'tempo_execucao':tempo_execucao, 'tempo_prioridade': tempo_prioridade})
				id = id + 1
			quantum = int(input('Qual o valor do Quantum?'))
			sobrecarga = int(input('Qual o valor da Sobrecarga?'))
			_edf(processos, quantidade_processos,quantum, sobrecarga)
			break

		if opcao_algoritmo == 6:
			arquivo = open('resultados.json', 'w')
			process = [{'tempo_execucao': 4, 'tempo_chegada': 0}, {'tempo_execucao': 2, 'tempo_chegada': 2}, {'tempo_execucao': 1, 'tempo_chegada': 4}, {'tempo_execucao': 3, 'tempo_chegada': 6}]
			time_in = 4
			saida = {'labels': ["FIFO"],'datasets': [{'data': [_sjf(process, time_in)]}]}
			json.dump(saida, arquivo, indent=4)
			webbrowser.open_new_tab("templates/grafico.html")
			break
		
		else:
			print "Comando Invalido!"