def fifo(processos):
	turnaround = 0
	for p in processos:
		turnaround += p['tempo_execucao'] - p['tempo_chegada']
	print '\nTurnaround: %d' % turnaround
	# Gerar grafico
	

if __name__ == "__main__":
	while True:
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
				count = 0;
				for i in range(0, quantidade_processos):
					print '\nProcesso %d:' % i
					tempo_chegada  = int(input('Tempo de chegada: '))
					tempo_execucao = int(input('Tempo de execucao: '))
					processos.append({'tempo_chegada': tempo_chegada, 'tempo_execucao':tempo_execucao})

				fifo(processos)