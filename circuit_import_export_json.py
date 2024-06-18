import cirq
import json

# Define the number of qubits
NUM_QUBITS = 4

# Create a list of line qubits
qubits = cirq.LineQubit.range(NUM_QUBITS)

# Define a function to create a subcircuit
def my_circuit():
    yield cirq.X(qubits[0])
    yield cirq.H(qubits[1])
    yield cirq.CZ(qubits[2], qubits[3])

# Create the main circuit and append the subcircuit
circuit = cirq.Circuit()
circuit.append(my_circuit())

# Serialize the circuit to JSON
json_string = cirq.to_json(circuit)

# Write the JSON string to a file
with open("circuit.json", "w") as w:
    w.write(json_string)

# Read the JSON string from the file and deserialize it back to a circuit
with open("circuit.json", "r") as r:
    new_circuit = cirq.read_json(r)

# Print the deserialized circuit
print(new_circuit)
