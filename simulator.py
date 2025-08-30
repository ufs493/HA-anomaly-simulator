"""
Simulates the hybrid automaton and generates time-series data.
"""
import numpy as np
from scipy.integrate import odeint
from .ha_models import TwoTankSystem

def simulate_system(initial_state, t_end, dt, anomaly_time=None):
    """
    Simulates the two-tank system and generates data.
    Args:
        initial_state: [h1_0, h2_0]
        t_end: End time of simulation
        dt: Time step
        anomaly_time: Time at which to inject a valve_stuck anomaly. If None, runs normally.
    Returns:
        t: Array of time points
        states: Array of system states [h1, h2] at each time point
        modes: Array of operational modes at each time point
    """
    system = TwoTankSystem()
    t = np.arange(0, t_end, dt)
    states = []
    modes = []

    current_state = initial_state

    for time_point in t:
        # Inject anomaly if it's time
        if anomaly_time is not None and time_point >= anomaly_time:
            system.set_mode('VALVE_STUCK')

        # Record current state and mode
        states.append(current_state)
        modes.append(system.mode)

        # Integrate the dynamics forward one time step (using simple Euler for clarity)
        derivative = system.continuous_dynamics(current_state, time_point)
        next_state = current_state + derivative * dt
        current_state = next_state

    return t, np.array(states), np.array(modes)

def generate_dataset(num_normal_samples, num_anomalous_samples, dt=0.1, t_end=50, anomaly_time=25):
    """
    Generates a dataset of normal and anomalous runs.
    Returns:
        X: Combined data array [time, h1, h2]
        y: Labels (0 for normal, 1 for anomalous)
    """
    all_data = []
    all_labels = []

    # Generate normal samples (no anomaly injected)
    for _ in range(num_normal_samples):
        # Randomize initial conditions slightly for variety
        h0 = np.random.uniform(0.5, 1.5)
        h1 = np.random.uniform(0.5, 1.5)
        t, states, modes = simulate_system([h0, h1], t_end, dt, anomaly_time=None)
        data = np.column_stack((t, states))
        all_data.append(data)
        all_labels.append(np.zeros(len(t))) # Label 0 for all time points

    # Generate anomalous samples (anomaly injected at anomaly_time)
    for _ in range(num_anomalous_samples):
        h0 = np.random.uniform(0.5, 1.5)
        h1 = np.random.uniform(0.5, 1.5)
        t, states, modes = simulate_system([h0, h1], t_end, dt, anomaly_time)
        data = np.column_stack((t, states))
        labels = np.where(t >= anomaly_time, 1, 0) # Label 1 after anomaly
        all_data.append(data)
        all_labels.append(labels)

    # Combine all samples
    X = np.vstack(all_data)
    y = np.hstack(all_labels)

    return X, y
