import re
from qutip import *
import numpy as np

class fidelity:
    def __init__(self, GateOp):
        self.GateOp = GateOp

    def get_fidelity(self, Pulses, rho_init, rho_targets):
        F = self.GateOp(Pulses, rho_init, rho_targets)
        return  F
