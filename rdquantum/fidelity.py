from qutip import *

class fidelity:
    def __init__(self, GateOp):
        self.GateOp = GateOp

    def get_fidelity(self, Pulses, rho_init, rho_targets):
        results = self.GateOp(Pulses, rho_init, rho_targets)
        return  results.expect[0][-1]