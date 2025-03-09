from qiskit import QuantumCircuit

def collatz_oracle(circuit, qubits):
    """
    Collatz zincirinde belirli bir durumu işaretlemek için oracle fonksiyonu.
    """
    qubits = list(qubits)

    # ✅ Çift sayı kontrolü → Son qubit "0" ise çift
    circuit.x(qubits[-1])
    circuit.mct(qubits[:-1], qubits[-1])
    circuit.x(qubits[-1])

    # ✅ Tek sayı kontrolü → Son qubit "1" ise tek
    circuit.cx(qubits[-1], qubits[0])

    # ✅ İşaretleme işlemi → Faz dönüşü kübit sayısına bağlı olarak ayarlandı
    circuit.h(qubits[-1])
    circuit.x(qubits[-1])
    circuit.mct(qubits[:-1], qubits[-1])
    circuit.x(qubits[-1])
    circuit.h(qubits[-1])

    return circuit
