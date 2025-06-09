
# Qiskit core
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import QFT
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

# IBM Quantum
from qiskit_ibm_runtime import (
    QiskitRuntimeService,
    SamplerV2 as Sampler,
    Options,
    Session,
    Estimator
)
from qiskit_ibm_runtime.fake_provider import FakeKyiv

# Auxiliares
import numpy as np
import random
import math
from fractions import Fraction

# Visualização
import matplotlib.pyplot as plt
from qiskit.visualization import plot_histogram

# Parâmetros
n = 4
oracle_target = '1110'

# 1. Inicialização
grover_circuit = QuantumCircuit(n, n)
grover_circuit.h(range(n))
grover_circuit.barrier()

# 2. Oráculo
def aplicar_oraculo(qc, target: str):
    for i, bit in enumerate(reversed(target)):
        if bit == '0':
            qc.x(i)
    qc.h(n-1)
    qc.mcx(list(range(n-1)), n-1)
    qc.h(n-1)
    for i, bit in enumerate(reversed(target)):
        if bit == '0':
            qc.x(i)


# 3. Difusor (amplificação)
def diffusion_operator(qc):
    qc.h(range(n))
    qc.x(range(n))
    qc.h(n-1)
    qc.mcx(list(range(n-1)), n-1)
    qc.h(n-1)
    qc.x(range(n))
    qc.h(range(n))

# Número de iterações de Grover
num_iterations = math.floor((math.pi / 4) * math.sqrt(2**n))

for _ in range(num_iterations):
    aplicar_oraculo(grover_circuit, oracle_target)
    diffusion_operator(grover_circuit)
    grover_circuit.barrier()


# 4. Medição
grover_circuit.measure(range(n), range(n))

# Autenticação e seleção de backend IBM
service = QiskitRuntimeService(
    channel="ibm_quantum",
    token="TOKEN_AQUI"
)
backend = service.least_busy(operational=True, simulator=False)
print("Backend selecionado:", backend)

# Transpilação
transpiled_circuit = transpile(grover_circuit, backend)

# Submissão do job
sampler = Sampler(backend)
job = sampler.run([transpiled_circuit])
result = job.result()[0]

# Exibição de resultados inline
counts = result.data.c.get_counts()

transpiled_circuit.draw()

# Gere a figura e deixe o Jupyter exibi-la automaticamente
fig = plot_histogram(counts)
fig

