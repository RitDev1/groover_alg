import random
import time

def busca_classica_linear(banco_de_dados, elemento_alvo):
    numero_de_consultas = 0
    for indice, elemento in enumerate(banco_de_dados):
        numero_de_consultas += 1
        if elemento == elemento_alvo:
            return (indice, numero_de_consultas)

    return (-1, numero_de_consultas)

tamanho_do_problema = 10_000_000
print(f"Criando um banco de dados não estruturado com {tamanho_do_problema:,} itens.")
banco_de_dados_exemplo = list(range(tamanho_do_problema))
random.shuffle(banco_de_dados_exemplo)

indice_alvo = tamanho_do_problema - 1
item_procurado = banco_de_dados_exemplo[indice_alvo]
print(f"O elemento alvo a ser encontrado é: {item_procurado}\n")

print("Iniciando a busca com o algoritmo clássico...")
start_time = time.perf_counter()
resultado, consultas_realizadas = busca_classica_linear(banco_de_dados_exemplo, item_procurado)
end_time = time.perf_counter()

if resultado != -1:
    print(f"O elemento {item_procurado} foi encontrado no índice {resultado}.")
else:
    print(f"O elemento {item_procurado} não foi encontrado no banco de dados.")

# Agora o número de consultas e o tempo serão significativos
print(f"Número de verificações (consultas) realizadas: {consultas_realizadas:,}")
print(f"Tempo de execução: {end_time - start_time:.6f} segundos")