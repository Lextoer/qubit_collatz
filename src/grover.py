from qiskit import QuantumCircuit
from src.collatz_oracle import collatz_oracle
from qiskit import QuantumCircuit

def create_grover_circuit(num_qubits):
    circuit = QuantumCircuit(num_qubits)

    # Hadamard kapıları ile süperpozisyon oluşturuyoruz
    for qubit in range(num_qubits):
        circuit.h(qubit)

    return circuit

def grover_iteration(circuit, qubits):
    # Oracle çağrısı
    collatz_oracle(circuit, qubits)

    # Difüzyon Operatörü
    circuit.h(qubits)
    circuit.x(qubits)
    circuit.mct(qubits[:-1], qubits[-1])
    circuit.x(qubits)
    circuit.h(qubits)

def create_grover_circuit(num_qubits):
    circuit = QuantumCircuit(num_qubits)

    # Hadamard Kapıları ile süperpozisyon oluşturuyoruz
    circuit.h(range(num_qubits))

    # Birden fazla iterasyon ile hassasiyeti artırıyoruz
    for _ in range(6):  # İterasyon sayısını artırıyoruz
     grover_iteration(circuit, list(range(num_qubits)))

    # Ölçüm ekliyoruz
    circuit.measure_all()

    return circuit
