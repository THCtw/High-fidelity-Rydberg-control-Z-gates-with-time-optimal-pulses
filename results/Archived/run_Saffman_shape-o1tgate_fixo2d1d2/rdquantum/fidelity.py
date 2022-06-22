import re
from qutip import *
import numpy as np

class fidelity:
    def __init__(self, GateOp):
        self.GateOp = GateOp

    def get_fidelity(self, Pulses, rho_init, rho_targets):
        results = self.GateOp(Pulses, rho_init, rho_targets)
        bell1 = results.expect[0][-1]
        bell2 = results.expect[1][-1]
        bell3 = results.expect[2][-1]
        F = 1/2 * (bell1 + bell2) + np.absolute(bell3)
        return  F
