## Learn QEM Config

This repo experiments with zero-noise extrapolation (ZNE) workflows using [mitiq](https://mitiq.readthedocs.io/en/stable/) and qiskit.

### Quick Start

- Install [`uv`](https://docs.astral.sh/uv/)
- Install all the project dependencies with `uv sync`
- You should be able to run the `sweep_config.ipynb` file all the way through without errors.

### Goals

1. Include new error models such as readout, amplitude damping, or thermal relaxation to compare how ZNE recipes behave across noise sources.
2. Add different circuits and observables beyond the current GHZ setup so we can probe the mitigation routines on diverse workloads.
3. Build routines that adaptively explore ZNE parameters to discover the best configuration per backend. Begin with scripted sweeps, then incorporate feedback-driven tuning, and finally automate backend-specific parameter selection.
4. Use optimization routines on other QEM techniques.
