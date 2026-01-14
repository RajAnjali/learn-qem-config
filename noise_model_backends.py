from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error, phase_damping_error, amplitude_damping_error

def build_depolarizing_backend(prob=0.005):
    noise_model = NoiseModel()

    depolarizing_err1 = depolarizing_error(prob, num_qubits=1)
    depolarizing_err2 = depolarizing_error(prob, num_qubits=2)
    noise_model.add_all_qubit_quantum_error(depolarizing_err1, ["h", "x", "y", "z"])
    noise_model.add_all_qubit_quantum_error(depolarizing_err2, ["cx"])

    return AerSimulator(noise_model=noise_model)

def build_amplitude_damping_backend(param_amp=0.005, excited_state_population=0, canonical_kraus=True):
    noise_model = NoiseModel()

    amplitude_err = amplitude_damping_error(param_amp, excited_state_population, canonical_kraus)
    noise_model.add_all_qubit_quantum_error(amplitude_err, ["h", "x", "y", "z"])
    
    return AerSimulator(noise_model=noise_model)

def build_phase_damping_backend(param_phase=0.005, canonical_kraus=True):
    noise_model = NoiseModel()

    phase_err = phase_damping_error(param_phase, canonical_kraus)
    noise_model.add_all_qubit_quantum_error(phase_err, ["h", "x", "y", "z"])
    
    return AerSimulator(noise_model=noise_model)


