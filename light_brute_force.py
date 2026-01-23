import json
import numpy as np
import copy
from test_zne import make_experiment_list, batch_execute, make_executor
from noise_model_backends import get_noise_backend
from circuits import get_experiment

NOISE_MODEL = "depolarizing"
CIRCUIT = "mirror_circuits"

search_space = {
    "noise_scaling_factors": [[1, 1.25, 1.5],[1, 2, 3],[2, 4, 6],],
    "noise_scaling_method": ["global", "local_all", "local_random"],
    "extrapolation": ["polynomial", "linear"],
}

param_order = ["noise_scaling_factors", "noise_scaling_method", "extrapolation"]

circ, verify_func, ideal_result = get_experiment(CIRCUIT)
backend = get_noise_backend(NOISE_MODEL)
exe = make_executor(backend, verify_func, shots=4096)

# Starting configuration: first value of each parameter
current_config = {
    "noise_scaling_factors": search_space["noise_scaling_factors"][0],
    "noise_scaling_method": search_space["noise_scaling_method"][0],
    "extrapolation": search_space["extrapolation"][0]
}

iter = 0
max_iter=10
converged = False
max_reached=False

while not converged and not max_reached:
    iter += 1
    
    previous_config = current_config.copy()
    
    # Optimize locally each parameter
    for param_name in ["noise_scaling_factors", "noise_scaling_method", "extrapolation"]:
        
        # Set up an experiment with all parameters fixed except one
        batch_dict = {
            "noise_scaling_factors": [current_config["noise_scaling_factors"]],
            "noise_scaling_method": [current_config["noise_scaling_method"]],
            "extrapolation": [current_config["extrapolation"]]
        }

        batch_dict[param_name] = search_space[param_name]
        
        # Run this batch of experiments and find the best configuration
        results = batch_execute(batch_dict, circ, exe)
        errors = np.abs(np.array(results) - ideal_result)
        best_idx = np.argmin(errors)
        best_value_for_param = search_space[param_name][best_idx]
        best_result_value = results[best_idx]

        # Update current configuration
        current_config[param_name] = best_value_for_param
        

    # Check if the configuration has changed
    start_str = json.dumps(previous_config, sort_keys=True)
    end_str = json.dumps(current_config, sort_keys=True)
    if start_str == end_str:
        converged = True
    # If it has change, restart the loop
    # Limit on iterations
    if iter==max_iter:
        max_reached=True

if max_reached:
    print("Max number of iterations reached")
else:
    final_error = abs(best_result_value - ideal_result)
    print("BEST CONFIGURATION:")
    print(json.dumps(current_config, indent=4))
    print(f"Ideal result:      {ideal_result}")
    print(f"Best result:   {best_result_value}")
    print(f"Absolute error:   {final_error}")
