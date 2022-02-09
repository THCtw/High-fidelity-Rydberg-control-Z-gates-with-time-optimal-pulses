from random import sample
from fidelity import fidelity
import numpy as np

class de:
    def __init__(self, fidelity, K, Llim, Ulim, c=15, mu=0.5, xi=0.9):
        self.fidelity = fidelity    # Fidelity object
        self.K = K                  # Number of control parameters
        self.Np = c * K             # Population size
        self.Llim = Llim            # Lower limit of control parameters
        self.Ulim = Ulim            # Upper limit of control parameters
        self.samples = []           
        self.mu = mu                # Mutation factor
        self.xi = xi                # Crossover rate
        
        self.data_fidelity = []
        self.data_pulses = [[]]
        self.op_fidelity = 0
        self.op_pulse = []

    def sample_init(self):
        # Initaillize random samples for optimization
        self.samples = np.random.uniform(self.Llim, self.Ulim, [self.Np, self.K])

    def sample(self, n):
        # Randomly choose n samples for one differential evolution iteration
        choosed = []
        for i in range(n):
            s = int(self.Np * np.random.uniform(0,1))
            while s in choosed:
                s = int(self.Np * np.random.uniform(0,1))
            choosed.append(s)

        return np.array(choosed)
    
    def start(self, itr = 10000):
        # itr: iteration times
        self.sample_init()
        Data_Fidelity = self.data_fidelity
        Data_Pulses = self.data_pulses
        Op_Fidelity = self.op_fidelity
        Op_Pulse = self.op_pulse

        for i in range(itr):
            print('# %s.' %i)
            print("Optimized Fidelity: %s" %Op_Fidelity)
            # 1) Mutation
            di = self.sample(4)   # Sampled population member
            Di = self.samples[di[0]]            # Original vector
            Di1 = self.samples[di[1]]
            Di2 = self.samples[di[2]]
            Di3 = self.samples[di[3]]
            Mi = Di1 + self.mu*(Di2 - Di3)      # Trail vector

            # 2) Corssover
            Ci = []     # Target vector
            for i in range(len(Mi)):
                r = np.random.uniform(0,1) 
                if r < self.xi:
                    Ci.append(Mi[i])
                else:
                    Ci.append(Di[i])

            # 3) Selection
            fci = self.fidelity.get_fidelity(Ci)
            fdi = self.fidelity.get_fidelity(Di)
            print("Fidelity (Ci, Di) = %s %s"%(fci, fdi))
            if fci > fdi:
                self.samples[di[0]] = Ci
                print("Replace vector %s" %(di[0]))
                Data_Fidelity.append(fci)
                Data_Pulses.append(Ci)
            else:
                print("Vector %s unchanged" %(di[0]))
                Data_Fidelity.append(fdi)
                Data_Pulses.append(Di)
            
            if Data_Fidelity[-1] > Op_Fidelity:
                Op_Fidelity = Data_Fidelity[-1]
                Op_Pulse = Data_Pulses[-1]