from __future__ import division
from time import sleep
from threading import Thread
import json 
import webbrowser
import os


class Processo(Thread):

	def __init__(self, id, tempo_chegada, tempo_execucao):
		Thread.__init__(self)
		self.id = id
		self.tempo_chegada = tempo_chegada
		self.tempo_execucao = tempo_execucao
		

		self.tempo_inicio_execucao = 0
		self.tempo_fim_execucao = 0
 
	def run(self):
		print '\nProcesso %d: Chegando em %d' % (self.id, self.tempo_chegada)
		sleep(self.tempo_execucao)
		print '\nProcesso %d: Finalizou execucao em %d' % (self.id, self.tempo_execucao)


def gerar_grafico(execucoes):
	with open("execucoes.json", 'w') as fp:
		json.dump(execucoes, fp, indent=4)
	
	webbrowser.open_new_tab("file://" + os.getcwd()+"/grafico.html")



def fifo(processos):
	time_in = 0 
	turnaround = 0
	size = len(processos)
	
	processos.sort(key= lambda p: p['tempo_chegada'])
	print 'Comecando execucao!\n'

	t = None
	json_execucoes = []

	clock_inicio_execucao = 0
	p_anterior = None
	for p in processos:
		time_in = p['tempo_execucao'] + time_in
		turnaround += (time_in - p['tempo_chegada'])
		sleep(p['tempo_chegada'])

		if p_anterior == None:
			clock_inicio_execucao = p['tempo_chegada']
		else:
			clock_inicio_execucao += p_anterior['tempo_execucao']

		json_execucoes.append({
			'id': p['id'],
			'tempo_chegada': p['tempo_chegada'], 
			'tempo_inicio_execucao': clock_inicio_execucao,
			'tempo_fim_execucao': time_in
		})

		t = Processo(p['id'], p['tempo_chegada'], time_in)
		t.setName(p['id'])
		t.start()
		p_anterior = p
	t.join()
	
	print '\n\nTurnaround: ' + str(turnaround / size )
	# Gerar grafico
	# print json_execucoes
	# print json.dumps(json_execucoes)
	gerar_grafico(json_execucoes)



def _sjf(process, size):
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
		turnaround += time_in - p['tempo_chegada']
		sleep(p['tempo_chegada'])
		t = Processo(p['id'], p['tempo_chegada'], p['tempo_execucao'])
		t.setName(p['id'])
		t.start()

	t.join()

	print '\n\nTurnaround: ' + str(turnaround/float(size))


def _round__robin(process, size, quantum, sobrecarga):
	time_in = 0 
	turnaround = 0
	time_split = 0

	processos.sort(key= lambda p: p['tempo_chegada'])
	print processos

	t = None

	for p in processos:
		time_split_div = p['tempo_execucao'] // quantum
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
		t = Processo(p['id'], p['tempo_chegada'], p['tempo_execucao'])
		t.setName(p['id'])
		t.start()

	t.join()

	print '\n\nTurnaround: ' + str(turnaround/size)


def _prioridade(process, size):
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
		t = Processo(p['id'], p['tempo_chegada'], p['tempo_execucao'])
		t.setName(p['id'])
		t.start()

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
		t = Processo(p['id'], p['tempo_chegada'], time_in)
		t.setName(p['id'])
		t.start()
		
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

		#FIFO
		if opcao_algoritmo == 1:
			processos = list()
			for i in range(0, quantidade_processos):
				print '\nProcesso %d:' % i
				p = {
					'id': i,
					'tempo_chegada':  int(input('Tempo de chegada: ')),
					'tempo_execucao': int(input('Tempo de execucao: '))
				}				
				processos.append(p)

			fifo(processos)
			break


		#SJF
		if opcao_algoritmo == 2:
			processos = list()
			for i in range(0, quantidade_processos):
				print '\nProcesso %d:' % i
				p = {
					'id': i,
					'tempo_chegada':  int(input('Tempo de chegada: ')),
					'tempo_execucao': int(input('Tempo de execucao: '))
				}
				processos.append(p)
			_sjf(processos, quantidade_processos)
			break


		#Round Robin
		if opcao_algoritmo == 3:
			processos = list()
			for i in range(0, quantidade_processos):
				print '\nProcesso %d:' % i
				p = {
					'id': i,
					'tempo_chegada':  int(input('Tempo de chegada: ')),
					'tempo_execucao': int(input('Tempo de execucao: '))
				}
				processos.append(p)
			quantum = int(input('Qual o valor do Quantum?'))
			sobrecarga = int(input('Qual o valor da Sobrecarga?'))

			_round__robin(processos, quantidade_processos, quantum, sobrecarga)
			break


		#Prioridade
		if opcao_algoritmo == 4:
			processos = list()
			for i in range(0, quantidade_processos):
				print '\nProcesso %d:' % i
				p = {
					'id': i,
					'tempo_chegada':    int(input('Tempo de chegada: ')),
					'tempo_execucao':   int(input('Tempo de execucao: ')),
					'tempo_prioridade': int(input('Prioridade: '))
				}
				processos.append(p)
			_prioridade(processos, quantidade_processos)
			break


		#EDF
		if opcao_algoritmo == 5:
			processos = list()
			for i in range(0, quantidade_processos):
				print '\nProcesso %d:' % i
				
				p = {
					'id': i,
					'tempo_chegada':    int(input('Tempo de chegada: ')),
					'tempo_execucao':   int(input('Tempo de execucao: ')),
					'tempo_prioridade': int(input('Prioridade: '))
				}
				processos.append(p)

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
			
			webbrowser.open_new_tab("file://" + os.getcwd()+"/templates/grafico.html")
			break
		
		else:
			print "Comando Invalido!"