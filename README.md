# Composite-Trotter-qDrift-GAOP 
> In this project I explore the usage of a composite trotter-qdrift quantum simulator with genetic algorithm optimized partitioning

## Introduction
The operator $U(t) = e^{iHt}$ can be used to calculate how a quantum system evolves over time. This is extremely useful for numerous fields such as chemistry and condensed matter. Constructing this operator is not an easy task, and quantum computers are thought to be one effective way of tackling it. The two biggest quantum algorithms for this are Trotter methods and QDrift. Trotter methods being deterministic and QDrift being stochastic, both have their own merits.

In this project we propose a composite trotter-qdrift algorithm which uses a genetic algorithm to search for near optimal partitioning of the hamiltonian. 

## Partitioning
We can define the total channel as $U_H(t) = U_A(t) \circ U_B(t; N,M)$

The cost or total number of gates for this composite channel is defined as
$$C_{cost} \leq (L_A+N_B)\frac{t^2}{\epsilon}\left(\sum_{i< j}a_ia_j||[A_i, A_j]||+\frac{1}{2}\sum_{i,j}a_ib_j||[A_i,B_j]||+\frac{2\lambda^2}{N_B}\right)$$

We use this cost function as the fitness function in our genetic algorithm, and create partitions using the chromosomes

## Results
<img width="605" alt="Screen Shot 2024-02-21 at 7 43 47 PM" src="https://github.com/utterwqlnut/Composite-Trotter-qDrift-GAOP/assets/51377003/b3d81b1f-5b1a-4dc2-a4da-50baf1eed734">
<img width="605" alt="Screen Shot 2024-02-21 at 7 44 05 PM" src="https://github.com/utterwqlnut/Composite-Trotter-qDrift-GAOP/assets/51377003/3fe9ffd5-ff72-46b3-84b6-9c1a2e11bb3e">
