import subprocess
import sys

try:
    import cirq
    import cirq_google
except ImportError:
    print("Installing cirq and cirq_google...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "cirq-google"])
    print("Installed cirq and cirq_google.")
    import cirq
    import cirq_google

try:
    import qsimcirq
except ImportError:
    print("Installing qsimcirq...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "qsimcirq"])
    print("Installed qsimcirq.")
    import qsimcirq

import matplotlib.pyplot as plt
import time

####################################################
processor_id = "rainbow"

# Construct a simulator with a noise model based on the specified processor
cal = cirq_google.engine.load_median_device_calibration(processor_id)
noise_props = cirq_google.noise_properties_from_calibration(cal)
noise_model = cirq_google.NoiseModelFromGoogleNoiseProperties(noise_props)
sim = qsimcirq.QSimSimulator(noise=noise_model)

# Create a device from the public device description
device = cirq_google.engine.create_device_from_processor_id(processor_id)
# Build the simulated local processor from the simulator and device
sim_processor = cirq_google.engine.SimulatedLocalProcessor(
    processor_id=processor_id, sampler=sim, device=device, calibrations={cal.timestamp // 1000: cal}
)
# Package the processor to use an Engine interface
sim_engine = cirq_google.engine.SimulatedLocalEngine([sim_processor])
print(
    "Your quantum virtual machine",
    processor_id,
    "is ready, here is the qubit grid:",
    "\n========================\n",
)
print(sim_engine.get_processor(processor_id).get_device())

######## Create a circuit, transform it (to make it executable on Google quantum hardware) ########
########                   and choose qubits on the processor                              ########


""" The circuit needs to be device ready, which means that:
       1. It comprised of operations from the device's gate set.
       2. It is applied to qubits that exist on the device.
       3. It respects the connectivity of qubits on the device. """

# Define an abstract line of qubits
number_of_qubits = 17
qubits = cirq.LineQubit.range(number_of_qubits)

# Create a GHZ (Greenberger–Horne–Zeilinger) circuit on this qubit line
ghz_circuit = cirq.Circuit(cirq.H(qubits[0]), *[cirq.CNOT(qubits[i - 1], qubits[i]) for i in range(1, number_of_qubits)],
    cirq.measure(*qubits, key='out'),
)
print(ghz_circuit)

# Before executing a circuit on (virtual) quantum hardware, the operations in the circuit need to be translated to use the types of gates the device supports
translated_ghz_circuit = cirq.optimize_for_target_gateset(
    ghz_circuit, context=cirq.TransformerContext(deep=True), gateset=cirq.SqrtIswapTargetGateset()
)
print(translated_ghz_circuit)

# Choose qubits on the virtual device - look at the device map and choose a set of qubits that fit your circuit (eg a line or a block).
# The Rainbow and Weber devices have different topologies - some qubit maps may be possible on only one of these devices.
# We need to find a consecutive line of qubits.

device_qubit_chain = [
    cirq.GridQubit(3, 2),
    cirq.GridQubit(4, 2),
    cirq.GridQubit(4, 1),
    cirq.GridQubit(5, 1),
    cirq.GridQubit(5, 2),
    cirq.GridQubit(5, 3),
    cirq.GridQubit(5, 4),
    cirq.GridQubit(6, 4),
    cirq.GridQubit(6, 3),
    cirq.GridQubit(6, 2),
    cirq.GridQubit(7, 2),
    cirq.GridQubit(7, 3),
    cirq.GridQubit(7, 4),
    cirq.GridQubit(7, 5),
    cirq.GridQubit(8, 5),
    cirq.GridQubit(8, 4),
    cirq.GridQubit(9, 4),
]

# Map the transformed circuit to the qubits we chose on the device
qubit_map = dict(zip(qubits, device_qubit_chain))
# Then replace qubits in the circuit according to that map
device_ready_ghz_circuit = translated_ghz_circuit.transform_qubits(lambda q: qubit_map[q])
print(device_ready_ghz_circuit)

######## Execute device-ready circuit on the Quantum Virtual Machine ########
circuit = device_ready_ghz_circuit

repetitions = 3000
start = time.time()
results = sim_engine.get_sampler(processor_id).run(circuit, repetitions=repetitions)
elapsed = time.time() - start

print('Circuit successfully executed on quantum virtual machine', processor_id)
print(f'QVM runtime: {elapsed:.04g}s ({repetitions} repetitions)')

# Visualize output
ax = cirq.plot_state_histogram(results.histogram(key='out'))
ax.get_xaxis().set_ticks([])
plt.gcf().set_size_inches(10, 4)
plt.show()