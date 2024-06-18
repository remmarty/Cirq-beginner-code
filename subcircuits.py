import cirq

# Define the number of qubits
NUM_QUBITS = 4

# Create a list of grid qubits
qubits = [cirq.GridQubit(0, i) for i in range(NUM_QUBITS)]

# Create a circuit object
circuit = cirq.Circuit()

# Append some gates to the circuit
circuit.append([cirq.X(qubits[0]), cirq.H(qubits[1])])

# Define a subcircuit operation
subcircuit = cirq.FrozenCircuit([cirq.Y(qubits[1]), cirq.H(qubits[2])])
subcircuit_op = cirq.CircuitOperation(subcircuit)

# Append the repeated subcircuit operation to the main circuit
circuit.append(subcircuit_op.repeat(2))

# Print the final circuit
print(circuit)