"""The quantum virtual machine is a virtual Google quantum processor that you can run circuits on
by using the virtual engine interface. Behind this interface, it uses simulation with noise data to
mimic Google quantum hardware processors with high accuracy"""

import subprocess
import sys

# Install `cirq_google` and `qsimcirq`
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

# Choose a processor to virtualize ("rainbow" or "weber")
processor_id = "weber"

# Load the median device noise calibration for your selected processor.
cal = cirq_google.engine.load_median_device_calibration(processor_id)
# Create the noise properties object.
noise_props = cirq_google.noise_properties_from_calibration(cal)
# Create a noise model from the noise properties.
noise_model = cirq_google.NoiseModelFromGoogleNoiseProperties(noise_props)
# Prepare a qsim simulator using the noise model.
sim = qsimcirq.QSimSimulator(noise=noise_model)

# Package the simulator and device in an Engine.
# The device object
device = cirq_google.engine.create_device_from_processor_id(processor_id)
# The simulated processor object
sim_processor = cirq_google.engine.SimulatedLocalProcessor(processor_id=processor_id, sampler=sim, device=device,
                                                            calibrations={cal.timestamp // 1000: cal})
# The virtual engine
sim_engine = cirq_google.engine.SimulatedLocalEngine([sim_processor])
print(
    "Your quantum virtual machine",
    processor_id,
    "is ready, here is the qubit grid:",
    "\n========================\n",
)
print(sim_engine.get_processor(processor_id).get_device())

# Run a circuit on QVM
q0 = cirq.GridQubit(4,4)
q1 = cirq.GridQubit(4,5)
circuit = cirq.Circuit([cirq.X(q0), cirq.SQRT_ISWAP(q0, q1), cirq.measure([q0, q1], key="measure")])

results = sim_engine.get_sampler(processor_id).run(circuit, repetitions=1000)
print(results.histogram(key="measure"))
