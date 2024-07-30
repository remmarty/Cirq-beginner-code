import cirq
import sympy

q0 = cirq.LineQubit(0)
theta = sympy.Symbol("theta")

# Create a parameterized circuit
circuit = cirq.Circuit([cirq.H(q0),  cirq.Z(q0)**theta, cirq.measure(q0)])
# or
circuit2 = cirq.Circuit([cirq.H(q0),  cirq.ZPowGate(exponent=theta)(q0), cirq.measure(q0)])

print(f"circuit:\n{circuit}")
print(f"circui2:\n{circuit2}")

# Check whether circuits are indeed parameterized
print(cirq.is_parameterized(circuit))
print(cirq.is_parameterized(circuit2))

# First example of using sweep in simulation
sim = cirq.Simulator()
results = sim.run_sweep(circuit, repetitions=10, params=[{"theta": 0.5}, {"theta": 0.25}])
for result in results:
    print(f"param: {result.params}, result: {result}")

# Second example - sweep over equally spaced values from 0 to 2.5
params = cirq.Linspace(key="theta", start=0, stop=2.5, length=10)
for param in params:
    print(param)

results = sim.run_sweep(circuit, repetitions=5, params=params)
for result in results:
    print(f"param: {result.params}, result: {result}")

# if you need to explicitly and individually specify each parameter resolution then:
params = cirq.Points(key="theta", points=[0, 1, 2])
for param in params:
    print(param)
results = sim.run_sweep(circuit, repetitions=5, params=params)
for result in results:
    print(f"param: {result.params}, result: {result}")


# Sweep from two constituent sweeps
sweep1 = cirq.Linspace("theta", 0, 1, 5)
sweep2 = cirq.Points("gamma", [0, 3])
# By taking the product of these two sweeps, you can sweep over all possible
# combinations of the parameters.
for param in sweep1 * sweep2:
    print(param)