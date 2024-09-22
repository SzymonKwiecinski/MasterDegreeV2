# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP

PROBLEM INFO:

- A division of an auto parts manufacturer produces \var{P} different parts using \var{M} different machines.
- Batch of 100 part \var{p} requires \var{time_{m,p}} hours on machine \var{m}.
- The division incurs a charge of \var{cost_{m}} per hour for using machine \var{m}.
- Machine \var{m} has an availability of up to \var{available_{m}} hours per month.
- The division sells part \var{p} in batches of 100 at price of \var{price_{p}} per batch.
- The division must produce at least \var{min_batches_{p}} batches of part \var{p} each month to fulfill a contract.

INPUT FORMAT: 

{
    "time_required": [[time_{m,p} for p in 1, ..., P] for m in 1, ..., M],
    "machine_costs": [cost_{m} for m in 1, ..., M],
    "availability": [available_{m} for m in 1, ..., M],
    "prices": [price_{p} for p in 1, ..., P],
    "min_batches": [min_batches_{p} for p in 1, ..., P]
}

OBJECTIVE: How many batches of each part should the manufacturer produce each month to maximize profit?

OUTPUT INFO:

- the number of batches of each part produced \var{batches_{p}}.
- \var{total_profit} represents the total profit obtained for the month.

OUTPUT FORMAT:

{
    "batches": [batches_{p} for p in 1, ..., P],
    "total_profit": total_profit
}
</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
To solve this linear programming (LP) problem, we need to formulate it by defining the decision variables, objective function, and constraints.

1. **Decision Variables:**
   - Let \( x_p \) denote the number of batches of part \( p \) to be produced each month, for \( p = 1, \ldots, P \).

2. **Objective Function:**
   - The objective is to maximize the total profit. The profit for part \( p \) is given by the revenue from selling the part minus the cost of producing it. Therefore, the total profit can be expressed as:
   \[
   \text{Total Profit} = \sum_{p=1}^{P} \left( \text{price}_p \cdot x_p - \sum_{m=1}^{M} \text{time}_{m,p} \cdot \text{cost}_m \cdot x_p \right)
   \]
   The objective function is to maximize this total profit.

3. **Constraints:**
   - **Machine Availability:** For each machine \( m \), the total time used cannot exceed its availability.
     \[
     \sum_{p=1}^{P} \text{time}_{m,p} \cdot x_p \leq \text{available}_m, \quad \forall m = 1, \ldots, M
     \]
   - **Minimum Production Requirement:** For each part \( p \), at least a specified number of batches must be produced each month.
     \[
     x_p \geq \text{min\_batches}_p, \quad \forall p = 1, \ldots, P
     \]
   - **Non-negativity:** The number of batches produced must be non-negative.
     \[
     x_p \geq 0, \quad \forall p = 1, \ldots, P
     \]

Here is the complete mathematical formulation in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Formulation}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( x_p \): Number of batches of part \( p \) produced each month, for \( p = 1, \ldots, P \).
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Maximize } Z = \sum_{p=1}^{P} \left( \text{price}_p \cdot x_p - \sum_{m=1}^{M} \text{time}_{m,p} \cdot \text{cost}_m \cdot x_p \right)
\]

\subsection*{Constraints}
\begin{enumerate}
    \item \textbf{Machine Availability:}
    \[
    \sum_{p=1}^{P} \text{time}_{m,p} \cdot x_p \leq \text{available}_m, \quad \forall m = 1, \ldots, M
    \]
    \item \textbf{Minimum Production Requirement:}
    \[
    x_p \geq \text{min\_batches}_p, \quad \forall p = 1, \ldots, P
    \]
    \item \textbf{Non-negativity:}
    \[
    x_p \geq 0, \quad \forall p = 1, \ldots, P
    \]
\end{enumerate}

\end{document}
```

This LP model will provide the optimal number of batches for each part type \( p \) that maximizes profit while respecting machine time availability and contractual obligations.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Formulation}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( x_p \): Number of batches of part \( p \) produced each month, for \( p = 1, \ldots, P \).
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Maximize } Z = \sum_{p=1}^{P} \left( \text{price}_p \cdot x_p - \sum_{m=1}^{M} \text{time}_{m,p} \cdot \text{cost}_m \cdot x_p \right)
\]

\subsection*{Constraints}
\begin{enumerate}
    \item \textbf{Machine Availability:}
    \[
    \sum_{p=1}^{P} \text{time}_{m,p} \cdot x_p \leq \text{available}_m, \quad \forall m = 1, \ldots, M
    \]
    \item \textbf{Minimum Production Requirement:}
    \[
    x_p \geq \text{min\_batches}_p, \quad \forall p = 1, \ldots, P
    \]
    \item \textbf{Non-negativity:}
    \[
    x_p \geq 0, \quad \forall p = 1, \ldots, P
    \]
\end{enumerate}

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the provided JSON format
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10]
}

#### Number of parts (P) and machines (M)
P = len(data['prices'])
M = len(data['availability'])

#### Define the Linear Programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
x = [pulp.LpVariable(f'x_{p+1}', lowBound=data['min_batches'][p], cat='Continuous') for p in range(P)]

#### Objective function
total_profit = pulp.lpSum([(data['prices'][p] - pulp.lpSum([data['time_required'][m][p] * data['machine_costs'][m] for m in range(M)])) * x[p] for p in range(P)])
problem += total_profit

#### Constraints

#### Machine availability constraints
for m in range(M):
    problem += pulp.lpSum([data['time_required'][m][p] * x[p] for p in range(P)]) <= data['availability'][m], f'Availability_Constraint_{m+1}'

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

