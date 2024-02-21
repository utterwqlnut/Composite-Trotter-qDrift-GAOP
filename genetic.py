import random
import numpy as np
from qiskit.quantum_info import SparsePauliOp
from util import fast_norm

class Individual:
    def __init__(self, h, N_b, t, e, mutate_prob, chromosome):
        self.mutate_prob = mutate_prob
        self.chromosome = chromosome
        self.h = h
        self.N_b=N_b
        self.t = t
        self.e = e
        self.h_a_coeffs, self.h_a_ops, self.h_b_coeffs, self.h_b_ops, self.h_a, self.h_b = self.partition_w_chromosome(h,chromosome)

    @classmethod
    def partition_w_chromosome(self,h,chromosome):
        # Partition hamiltonian into channel a for trotter and channel b for qdrift based on chromosome

        h_a_coeffs = []
        h_b_coeffs = []
        h_a_ops = []
        h_b_ops = []
        h_a_list = []
        h_b_list = []

        for i,val in enumerate(chromosome):
            if val==1:
                h_a_coeffs.append(h.coeffs[i])
                h_a_ops.append(h.paulis[i])
                h_a_list.append((h.paulis[i].to_label(),h.coeffs[i]))
            else:
                h_b_coeffs.append(h.coeffs[i])
                h_b_ops.append(h.paulis[i])
                h_b_list.append((h.paulis[i].to_label(),h.coeffs[i]))

        h_a = SparsePauliOp.from_list(h_a_list) if len(h_a_list)>0 else None 
        h_b = SparsePauliOp.from_list(h_b_list) if len(h_b_list)>0 else None

        return h_a_coeffs,h_a_ops, h_b_coeffs,h_b_ops, h_a, h_b
    
    @classmethod
    def get_mutate_gene(self):
        return random.randint(0,1)
    
    @classmethod 
    def create_gnome(self, len):
        return [self.get_mutate_gene() for _ in range(len)]
    
    def mate(self, other):
        child_chromosomes = []

        for gene1, gene2 in zip(self.chromosome, other.chromosome):
            prob = random.random()

            if prob<(1-self.mutate_prob)/2:
                child_chromosomes.append(gene1)
            elif prob<1-self.mutate_prob:
                child_chromosomes.append(gene2)
            else:
                child_chromosomes.append(self.get_mutate_gene())

        return Individual(self.h,self.N_b,self.t,self.e,self.mutate_prob,child_chromosomes)
    
    def fitness(self):
        # Calculate the upper bound for number of gates required

        term1 = (len(self.h_a_coeffs)+self.N_b)
        term2 = self.t**2/self.e
        term3 = 0
        term4 = 0
        term5 = 0

        for i,a_i in enumerate(self.h_a_coeffs):
            for j,a_j in enumerate(self.h_a_coeffs):
                if j<=i:
                    continue
                term3+=abs(a_i*a_j*fast_norm(self.h_a_ops[i],self.h_a_ops[j]))

        for i,a_i in enumerate(self.h_a_coeffs):
            for j,b_j in enumerate(self.h_b_coeffs):
                term4+=abs(a_i*b_j*fast_norm(self.h_a_ops[i],self.h_b_ops[j]))
        
        term4*=0.5
        
        term5 = 2*sum([abs(a) for a in self.h_b_coeffs])**2/self.N_b

        self.cost = term1*np.ceil(np.real(term2*(term3+term4+term5))) 

        return self.cost
        
    
def run_genetic_algo(population_size, num_generations, elite_prop, hamiltonian, N_b, t, e, mutate_prob):
    # Perform the genetic algorithm search for near-optimal partitioning
    
    population = []
    least_cost=1e30
    ans_h_a = None
    ans_h_b = None

    for _ in range(population_size):
        population.append(Individual(h=hamiltonian,N_b=N_b, t=t, e=e, mutate_prob=mutate_prob, chromosome=Individual.create_gnome(len(hamiltonian.paulis))))

    for i in range(num_generations):
        population = sorted(population, key = lambda x:x.fitness())
        new_generation = []
        s = int(population_size*elite_prop)
        new_generation.extend(population[:s])

        for _ in range(population_size-s):
            parent1 = random.choice(population[:int(0.5*population_size)])
            parent2 = random.choice(population[:int(0.5*population_size)])

            child = parent1.mate(parent2)
            new_generation.append(child)

        print(f"Generation {i+1} Lowest Number of Gates: {population[0].cost}")
        
        if population[0].cost<least_cost:
            least_cost=population[0].cost
            ans_h_a = population[0].h_a
            ans_h_b = population[0].h_b

        population = new_generation

    print(f"Lowest Number of Gates: {least_cost}")

    return least_cost, ans_h_a, ans_h_b

