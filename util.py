from scipy.special import lambertw
import numpy as np

def calc_reps_qdrift(error, hamiltonian,t):
    norm = sum([abs(a) for a in hamiltonian.coeffs])
    return np.ceil(2*norm**2*t**2/error).astype(int)

def calc_reps_trotter(error, hamiltonian, t):
    L = len(hamiltonian.coeffs)
    tri = max([abs(a) for a in hamiltonian.coeffs])

    u = L*tri*t
    ans = u/lambertw(2*error/(u)) 
    
    return np.ceil(ans.real).astype(int)

def calc_reps_composite(error, h_a, h_b, t, N_b):
    h_a_coeffs = h_a.coeffs
    h_b_coeffs = h_b.coeffs
    h_a_ops = h_a.paulis
    h_b_ops = h_b.paulis

    term1 = t**2/error
    term2 = 0
    term3 = 0
    term4 = 0

    for i,a_i in enumerate(h_a_coeffs):
        for j,a_j in enumerate(h_a_coeffs):
            if j<=i:
                continue
            term2+=abs(a_i*a_j*fast_norm(h_a_ops[i],h_a_ops[j]))
    for i,a_i in enumerate(h_a_coeffs):
        for j,b_j in enumerate(h_b_coeffs):
            term3+=abs(a_i*b_j*fast_norm(h_a_ops[i],h_b_ops[j]))
    term3*=0.5
    
    term4 = 2*sum([abs(a) for a in h_b_coeffs])**2/N_b
    
    r = int(np.ceil(np.real(term1*(term2+term3+term4))))
    return r

def fast_norm(a, b):
    if a.commutes(b):
        return 0
    else:
        return 2