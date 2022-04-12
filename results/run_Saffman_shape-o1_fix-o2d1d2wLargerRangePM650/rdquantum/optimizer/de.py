from multiprocessing.connection import wait
from IPython.display import clear_output
from rdquantum.fidelity import fidelity
import numpy as np

from qutip import *

class de:
    def __init__(self, fidelity, rho_init, rho_targets, mu=0.5, xi=0.9):
        self.fidelity = fidelity        # Fidelity object
        self.rho_init = rho_init        # Initial state
        self.rho_targets = rho_targets  # Target state           
        self.mu = mu                    # Mutation factor
        self.xi = xi                    # Crossover rate
        
        self.Np = 0                     # Population size
        self.K = 0                      # Number of control parameters
        self.populations = []
        self.valuerange = {}

        # Initialize data
        self.data_fidelity = []
        self.data_pulses = []
        self.op_fidelity = 0
        self.op_pulse = []

    def createPopulations(self, Pulses, PulsesRange, c=15):
        # Initiallize random Np populations for optimization
        self.K = 0                       # Number of control parameters
        self.valuerange = PulsesRange    # The limit of parameters' value
        for key in Pulses:
            self.K += len(Pulses[key])
        # print("Number of control parameters: %s" %self.K)
        self.Np = c * self.K        # Population size
        # print("Population size: %s" %self.Np)

        for i in range(self.Np):
            population = {}
            for key in Pulses:
                n = len(Pulses[key])
                population[key] = np.array(np.random.uniform(self.valuerange[key][0], self.valuerange[key][1], n))
            self.populations.append(population)

    def sample(self, n):
        # Randomly sample n populations for one differential evolution iteration
        choosed = []
        np.random.seed()
        for i in range(n):
            s = int(self.Np * np.random.uniform(0,1))
            while s in choosed:
                s = int(self.Np * np.random.uniform(0,1))
            choosed.append(s)

        return np.array(choosed)
    
    def iteration(self, arg):
        Mi = {}     # Trail vector
        Ci = {}     # Target vector
        # 1) Mutation
        # Mutated population should in the required limit (PulseRange).
        validmutation = False
        sample_trail = 0
        while validmutation != True:
            sample_trail +=1
            di = self.sample(4)             # Sampled population member
            Di = self.populations[di[0]]    # Original vector
            Di1 = self.populations[di[1]]
            Di2 = self.populations[di[2]]
            Di3 = self.populations[di[3]]
            for key in Di:
                Mi[key] = np.array(Di1[key]) + self.mu*(np.array(Di2[key]) - np.array(Di3[key]))
                # Check the validation of mutation
                invalid = [temp for temp in Mi[key]
                if temp < self.valuerange[key][0] or temp > self.valuerange[key][1]]
                if len(invalid) != 0:
                    validmutation = False
                    break
                else:
                    validmutation = True

        # 2) Corssover
        for key in Mi:
            Ci[key] = []
            for i in range(len(Mi[key])):
                r = np.random.uniform(0,1)
                if r < self.xi:
                    Ci[key].append(Mi[key][i])
                else:
                    Ci[key].append(Di[key][i])

        # 3) Selection
        fci = self.fidelity.get_fidelity(Ci, self.rho_init, self.rho_targets)
        fdi = self.fidelity.get_fidelity(Di, self.rho_init, self.rho_targets)
        print()
        if fci > fdi:
            replace = True
            print("Fidelity (Ci, Di) = %s %s, replace population %s" %(fci, fdi, di[0]), end='\r')
            return replace, di[0], Ci, fci
            
        else:
            replace = False
            print("Fidelity (Ci, Di) = %s %s, population %s unchanged" %(fci, fdi, di[0]), end='\r')
            return replace, di[0], Di, fdi

    def start(self, itr = 1000, batch = 10):
        # itr: iteration times
        # Check if self.populations is empty
        if len(self.populations) == 0:
            print("Please create populations, de.createPopulations(Pulses, PulsesRange).")
        else:
            # Differential evolution
            Mi = {}     # Trail vector
            Ci = {}     # Target vector
            for i in range(itr):
                print("Number of control parameters: %s" %self.K)
                print("Populations size: %s" %len(self.populations))
                print("Start differential evolution...")
                print("Iterations: %s" %itr)
                print("Optimized fidelity: %s" %self.op_fidelity)
                print("==============================")
                print('# %s batch iteration.' %(i+1))
                replace, id, pulse, fpulse = parfor(self.iteration, range(batch))

                for i in range(len(replace)):
                    if replace[i] == True:
                        self.populations[id[i]] = pulse[i]
                        self.data_fidelity.append(fpulse[i])
                        self.data_pulses.append(pulse[i])
                        
                    else:
                        self.data_fidelity.append(fpulse[i])
                        self.data_pulses.append(pulse[i])

                if self.data_fidelity[-1] > self.op_fidelity:
                    self.op_fidelity = self.data_fidelity[-1]
                    self.op_pulse = self.data_pulses[-1]
                
                print("Optimized Fidelity: %s" %self.op_fidelity)
                print('==============================')
                clear_output(wait=True)
        
            np.savez("out.npz", fidelity=self.data_fidelity, pulses=self.data_pulses)