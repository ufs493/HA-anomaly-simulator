# HA-Anomaly-Simulator

A proof-of-concept Python package for generating synthetic time-series data from a simple hybrid automaton. This tool is designed to create structured datasets for developing and testing physics-informed anomaly detection algorithms in Cyber-Physical Systems (CPS).

## Concept

This simulator implements a classic two-tank system as a hybrid automaton with two discrete modes:
- `NORMAL`: Standard operation.
- `VALVE_STUCK`: An anomalous mode where a valve is stuck closed.

The package demonstrates a key methodology for CPS resilience research: using formal models (hybrid automata) to create realistic training data for data-driven AI models.

## Features

- **Hybrid Automaton Model:** Defines continuous dynamics and discrete modes.
- **Data Simulation:** Generates time-series data of system states under normal and anomalous conditions.
- **Dataset Generation:** Creates labeled datasets suitable for training machine learning models.
- **Example Analysis:** Includes a Jupyter notebook demonstrating data generation and a basic anomaly detection example.
