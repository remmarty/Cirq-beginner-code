import cirq
import qsimcirq

NUM_QUBITS = 3
NUM_REP = 10

def my_circuit():
    yield cirq.X(qubits[0])
    yield cirq.H(qubits[1])
    yield cirq.X(qubits[2])
    yield cirq.measure(*qubits)  # Measure all qubits at the end of the circuit

qubits = [cirq.LineQubit(i) for i in range(NUM_QUBITS)]
circuit = cirq.Circuit(my_circuit())
print(circuit)

simulator = cirq.Simulator()
simulation = simulator.run(circuit, repetitions=NUM_REP)

# Extract measurement results
measurements = simulation.measurements
print(measurements)

""" Noisy simulation """
# The single-qubit bit-flip channel
bit_flip = cirq.bit_flip(p=0.2)
noisy_circuit = cirq.Circuit()

# Apply the channel to each qubit in a circuit
for moment in circuit:
    noisy_circuit.append(moment)
    # Check if the moment contains measurement operations
    if any(isinstance(op.gate, cirq.MeasurementGate) for op in moment):
        # Apply bit-flip noise to each qubit before the measurements
        noisy_circuit.insert(len(noisy_circuit) - 1, bit_flip.on_each(*qubits))
print(noisy_circuit)

noisy_simulation = simulator.run(noisy_circuit, repetitions=NUM_REP)
measurements = noisy_simulation.measurements
print(measurements)

""" Using mixture protocol """
for prob, kraus in cirq.mixture(bit_flip):
    print(f"With probability {prob}, apply\n", kraus, end="\n\n")

""" Adding custom (noisy) channel """
class MyChannel(cirq.Gate):
    def _num_qubits_(self) -> int:
        return 1
    
    # Probability
    def __init__(self, p: float) -> None:
        self._p = p

    def _mixture_(self):
        # List of probabilities, there is '1.0 - p' probabilty of doing nothing (apply I)
        #  and a 'p' probabiity of applying the X gate
        ps = [1.0 - self._p, self._p]
        ops = [cirq.unitary(cirq.I), cirq.unitary(cirq.X)]
        return tuple(zip(ps, ops))

    def _has_mixture_(self) -> bool:
        return True
    
    def _circuit_diagram_info_(self, args) -> str:
        return f"MyChannel({self._p})"