
"""
Defines a simple two-tank system as a hybrid automaton.
"""

import numpy as np

class TwoTankSystem:
    """
    A hybrid automaton for a two-tank system with continuous dynamics and discrete modes.
    Modes:
        'NORMAL':   Both valves operating correctly.
        'VALVE_STUCK':  Valve 1 is stuck closed. This is our anomalous mode.
    """
    def __init__(self, A1=1.0, A2=1.0, valve_setting=0.5):
        self.A1 = A1  # Cross-sectional area of tank 1
        self.A2 = A2  # Cross-sectional area of tank 2
        self.valve_setting = valve_setting  # Normal valve opening
        self.mode = 'NORMAL'

    def continuous_dynamics(self, state, t):
        """
        Defines the continuous dynamics (ODEs) for the system.
        state = [h1, h2] (heights of tank 1 and tank 2)
        """
        h1, h2 = state
        dh1_dt = dh2_dt = 0.0

        if self.mode == 'NORMAL':
            # Water flows from a source into tank 1, and from tank 1 to tank 2
            inflow = 2.0  # Constant inflow
            flow12 = self.valve_setting * (h1 - h2)  # Flow from tank1 to tank2
            dh1_dt = (inflow - flow12) / self.A1
            dh2_dt = (flow12) / self.A2

        elif self.mode == 'VALVE_STUCK':
            # Valve is stuck, no flow from tank1 to tank2
            inflow = 2.0
            flow12 = 0.0  # Stuck valve means no flow
            dh1_dt = (inflow - flow12) / self.A1
            dh2_dt = (flow12) / self.A2
            # Tank 1 will fill up, tank 2 will empty

        return np.array([dh1_dt, dh2_dt])

    def set_mode(self, new_mode):
        """Switches the discrete mode of the automaton."""
        if new_mode in ['NORMAL', 'VALVE_STUCK']:
            self.mode = new_mode
        else:
            raise ValueError("Invalid mode. Choose 'NORMAL' or 'VALVE_STUCK'.")
