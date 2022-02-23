from qutip import *

def __init__(self, dim):
    self.dim = dim

def transition (self, init, final):
    init_state = basis(self.dim, init)
    final_state = basis(self.dim, final)
    op = tensor(final_state, init_state.dag())

    return op