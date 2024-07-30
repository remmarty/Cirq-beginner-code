import cirq
import matplotlib.pyplot as plt

# Using state histograms to visualize the output of running a quantum circuit
q = cirq.LineQubit.range(5)
circuit = cirq.Circuit([cirq.H.on_each(*q), cirq.measure(*q, key='measure_all')])
print(circuit)

result = cirq.Simulator().run(circuit, repetitions=10)
histogram = cirq.plot_state_histogram(result, plt.subplot())
plt.show()

# Sparse plots to plot only non-zero entries in the histogram
sparse_histogram = result.histogram(key='measure_all')
_ = cirq.plot_state_histogram(sparse_histogram, plt.subplot())
plt.show()

# Modifying plot properties
def binary_labels(num_qubits):
    return [bin(x)[2:].zfill(num_qubits) for x in range(2 ** num_qubits)]

q = cirq.LineQubit.range(3)
circuit = cirq.Circuit([cirq.H.on_each(*q), cirq.measure(*q)])
result = cirq.Simulator().run(circuit, repetitions=100)
_ = cirq.plot_state_histogram(result, plt.subplot(), title = 'Custom Plot Title', xlabel = 'Custom X-Axis Label', ylabel = 'Custom Y-Axis Label', tick_label=binary_labels(3))
plt.show()