import cirq
import numpy as np

NUM_QUBITS = 3

# Define a custom (single-qubit) gate
class CustomGate(cirq.Gate):
    def __init__(self):
        super().__init__()

    def _num_qubits_(self):
        return 1
    
    def _unitary_(self):
        return np.array([
            [1, 0],
            [0, 1]
        ]) / np.sqrt(3)
    
    def _circuit_diagram_info_(self, args):
        return "Example"

my_gate = CustomGate()

# Create a list of LineQubits
qubits = [cirq.LineQubit(i) for i in range(NUM_QUBITS)]

# Create a circuit
circuit = cirq.Circuit()
circuit.append([cirq.H(qubits[0]), my_gate(qubits[1]), cirq.CZ(qubits[1], qubits[2])])
print(circuit)