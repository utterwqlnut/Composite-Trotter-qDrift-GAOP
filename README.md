# Composite-Trotter-qDrift-GAOP 
> In this project I explore the usage of a composite trotter-qdrift quantum simulator with genetic algorithm optimized partitioning

## Introduction
The operator $U(t) = e^{iHt}$ can be used to calculate how a quantum system evolves over time. This is extremely useful for numerous fields such as chemistry and condensed matter. Constructing this operator is not an easy task, and quantum computers are thought to be one effective way of tackling it. The two biggest quantum algorithms for this are Trotter methods and QDrift. Trotter methods being deterministic and QDrift being stochastic, both have their own merits.

In this project we propose a composite trotter-qdrift algorithm which uses a genetic algorithm to search for near optimal partitioning of the hamiltonian. 

## Partitioning
We can define the total channel as $U_H(t) = U_A(t) \circ U_B(t; N,M)$

The cost or total number of gates for this composite channel is defined as
$$C_{cost} \leq (L_A+N_B)\frac{t^2}{\epsilon}\left(\sum_{i<j}a_ia_j||[A_i, A_j]||+\frac{1}{2}\sum_{ij}a_ib_j||[A_i,B_j]||+\frac{2\lambda^2}{N_B}\right)$$

We use this cost function as the fitness function in our genetic algorithm, and create partitions using the chromosomes

## Results
![alt text](https://file%2B.vscode-resource.vscode-cdn.net/var/folders/3p/x1hjmpx55zbf70vx528h1ph40000gn/T/TemporaryItems/NSIRD_screencaptureui_rNhPyw/Screen%20Shot%202024-02-21%20at%207.34.20%20PM.png?version%3D1708562067679)
![alt text](https://file%2B.vscode-resource.vscode-cdn.net/var/folders/3p/x1hjmpx55zbf70vx528h1ph40000gn/T/TemporaryItems/NSIRD_screencaptureui_mWZG4S/Screen%20Shot%202024-02-21%20at%207.35.12%20PM.png?version%3D1708562118838)