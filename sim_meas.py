import cirq

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

# TODO noisy simulation
# TODO running on GPU
