from qiskit.quantum_info import SparsePauliOp
from qiskit.synthesis import QDrift, SuzukiTrotter
from qiskit.circuit.library import PauliEvolutionGate
from util import calc_reps_composite

class Composite:
    def __init__(self, h_trotter, h_qdrift, t, N_b, error):
        self.evoa = PauliEvolutionGate(h_trotter,time=t)
        self.evob = PauliEvolutionGate(h_qdrift,time=t)
        self.t = t
        self.N_b = N_b
        self.h_trotter = h_trotter
        self.h_qdrift = h_qdrift
        self.error = error
    
    def synthesize(self, need_reps):
        if need_reps:
            self.trotter_circ = SuzukiTrotter(reps=calc_reps_composite(self.error, self.h_trotter, self.h_qdrift, self.t, self.N_b)).synthesize(self.evoa)
            self.qdrift_circ = QDrift(reps=self.N_b).synthesize(self.evob)
        else:
            self.trotter_circ = SuzukiTrotter(reps=1).synthesize(self.evoa)
            self.trotter_reps = calc_reps_composite(self.error, self.h_trotter, self.h_qdrift, self.t, self.N_b)
            self.qdrift_circ = QDrift(reps=1).synthesize(self.evob) 
            self.qdrift_reps = self.N_b

    def count_gates(self, multiply_reps):
        if not multiply_reps:
            self.trotter_total = sum(dict(self.trotter_circ.count_ops()).values())
            self.qdrift_total = sum(dict(self.qdrift_circ.count_ops()).values()) 
        else:
            self.trotter_total = sum(dict(self.trotter_circ.count_ops()).values())*self.trotter_reps
            self.qdrift_total = sum(dict(self.qdrift_circ.count_ops()).values())*self.qdrift_reps

        return self.trotter_total+self.qdrift_total
    