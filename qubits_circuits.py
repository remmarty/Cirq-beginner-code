import cirq

# Create and name a qubit
qubit = cirq.NamedQubit("myqubit")

# Create a circuit object
circuit = cirq.Circuit()

# Add one quantum gate so that circuit will actually do something
circuit.append(cirq.X(qubit))  # Apply Pauli's X gate to our qubit

# Print the circuit to see the result in the console
print("Circuit with named qubit and X gate:")
print(circuit)

# Create a list of qubits
qubits = [cirq.GridQubit(0, i) for i in range(3)]

# Create new circuit object
new_circuit = cirq.Circuit()

# Add multiple quantum gates
new_circuit.append([cirq.Y(qubits[0]), cirq.Z(qubits[1]), cirq.H(qubits[2])])

# Print the new circuit to see the introduced changes
print("\nNew circuit with grid qubits and multiple gates:")
print(new_circuit)
