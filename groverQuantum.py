import numpy as np
import time
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

def criar_oraculo(num_qubits, elemento_alvo_binario):
    oraculo_qc = QuantumCircuit(num_qubits)
    
    for i, bit in enumerate(reversed(elemento_alvo_binario)):
        if bit == '0':
            oraculo_qc.x(i)
    
    oraculo_qc.h(num_qubits-1)
    oraculo_qc.mcx(list(range(num_qubits-1)), num_qubits-1)
    oraculo_qc.h(num_qubits-1)

    for i, bit in enumerate(reversed(elemento_alvo_binario)):
        if bit == '0':
            oraculo_qc.x(i)
            
    oraculo_gate = oraculo_qc.to_gate()
    oraculo_gate.name = "Oráculo"
    return oraculo_gate

def criar_difusor(num_qubits):
    qc = QuantumCircuit(num_qubits)
    qc.h(range(num_qubits))
    qc.x(range(num_qubits))
    qc.h(num_qubits-1)
    qc.mcx(list(range(num_qubits-1)), num_qubits-1)
    qc.h(num_qubits-1)
    qc.x(range(num_qubits))
    qc.h(range(num_qubits))
    difusor_gate = qc.to_gate()
    difusor_gate.name = "Difusor"
    return difusor_gate

num_qubits = 6
tamanho_do_problema = 2**num_qubits
print(f"O problema tem um espaço de busca de N = {tamanho_do_problema} itens ({num_qubits} qubits).")

item_procurado = tamanho_do_problema - 1
elemento_alvo_binario = format(item_procurado, f'0{num_qubits}b')
print(f"O elemento alvo a ser encontrado é: {item_procurado} (binário: {elemento_alvo_binario})\n")

qc = QuantumCircuit(num_qubits, num_qubits)
num_iteracoes = int(np.floor(np.pi / 4 * np.sqrt(tamanho_do_problema)))
print(f"Número ótimo de consultas (iterações de Grover): {num_iteracoes}")

qc.h(range(num_qubits))
qc.barrier()

oraculo = criar_oraculo(num_qubits, elemento_alvo_binario)
difusor = criar_difusor(num_qubits)
for _ in range(num_iteracoes):
    qc.append(oraculo, range(num_qubits))
    qc.append(difusor, range(num_qubits))
    qc.barrier()

qc.measure(range(num_qubits), range(num_qubits))

print("\nIniciando a busca com o algoritmo quântico (simulador)...")
start_time = time.perf_counter()

simulador = Aer.get_backend('qasm_simulator')
circuito_transpilado = transpile(qc, simulador)
resultado_sim = simulador.run(circuito_transpilado, shots=1024).result()
contagens = resultado_sim.get_counts()

end_time = time.perf_counter()

print(f"Simulação concluída!")
print(f"Tempo de execução: {end_time - start_time:.6f} segundos")

resultado_mais_provavel_binario = max(contagens, key=contagens.get)
resultado_mais_provavel_decimal = int(resultado_mais_provavel_binario, 2)

print(f"\nO resultado mais provável medido foi '{resultado_mais_provavel_binario}', que corresponde ao número {resultado_mais_provavel_decimal}.")

plot_histogram(contagens, figsize=(10, 6))
plt.show()