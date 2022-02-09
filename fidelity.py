from qutip import *

class fidelity:
    def __init__(self, GateOp, rho_init, rho_targets):
        self.GateOp = GateOp
        self.rho_init = rho_init
        self.rho_targets = rho_targets

    def get_fidelity(self, args):
        results = self.GateOp(args, self.rho_init, self.rho_targets)
        return  results.expect[0][-1]