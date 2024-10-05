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
- Machine \var{M} and Machine \var{M-1} can share availability.
- Individual availability conditions for Machine \var{M} and Machine \var{M-1} can be disregarded.
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
Based on the problem description, we need to create a linear programming model to maximize the profit by determining how many batches of each part to produce. Let's define the mathematical model in LaTeX format.

```latex
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\title{Linear Programming Model for Auto Parts Manufacturing}
\author{}
\date{}
\maketitle

\section*{Problem Description}

The objective is to determine the number of batches of each part, denoted as \( \text{batches}_p \), to be produced each month, in order to maximize the total profit while respecting the constraints on machine availability and production requirements.

\section*{Decision Variables}

Let \( x_p \) be the number of batches of part \( p \) produced each month, for \( p = 1, 2, \ldots, P \).

\section*{Objective Function}

Maximize the total profit:
\[
\text{Maximize } Z = \sum_{p=1}^{P} \left( \text{price}_p \cdot x_p \right) - \sum_{m=1}^{M} \left( \text{cost}_m \cdot \sum_{p=1}^{P} \left( \text{time}_{m,p} \cdot x_p \right) \right)
\]

\section*{Constraints}

1. Demand Constraints: 
   \[
   x_p \geq \text{min\_batches}_p \quad \text{for each } p = 1, 2, \ldots, P
   \]

2. Machine Availability Constraints:
   \[
   \sum_{p=1}^{P} \left( \text{time}_{m,p} \cdot x_p \right) \leq \text{available}_m \quad \text{for each } m = 1, 2, \ldots, M-2
   \]
   
   For machines \( M \) and \( M-1 \) sharing availability:
   \[
   \sum_{p=1}^{P} \left( \text{time}_{M,p} \cdot x_p \right) + \sum_{p=1}^{P} \left( \text{time}_{M-1,p} \cdot x_p \right) \leq \text{available}_M + \text{available}_{M-1}
   \]

3. Non-negativity:
   \[
   x_p \geq 0 \quad \text{for each } p = 1, 2, \ldots, P
   \]

\end{document}
```

This linear programming model captures the essence of the problem. The objective is to maximize profits by selecting the optimal number of batches for each part, subject to machine availability and contractual obligations for minimum batches. The machines \( M \) and \( M-1 \) have a shared availability constraint, allowing them to share their total available hours.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\title{Linear Programming Model for Auto Parts Manufacturing}
\author{}
\date{}
\maketitle

\section*{Problem Description}

The objective is to determine the number of batches of each part, denoted as \( \text{batches}_p \), to be produced each month, in order to maximize the total profit while respecting the constraints on machine availability and production requirements.

\section*{Decision Variables}

Let \( x_p \) be the number of batches of part \( p \) produced each month, for \( p = 1, 2, \ldots, P \).

\section*{Objective Function}

Maximize the total profit:
\[
\text{Maximize } Z = \sum_{p=1}^{P} \left( \text{price}_p \cdot x_p \right) - \sum_{m=1}^{M} \left( \text{cost}_m \cdot \sum_{p=1}^{P} \left( \text{time}_{m,p} \cdot x_p \right) \right)
\]

\section*{Constraints}

1. Demand Constraints: 
   \[
   x_p \geq \text{min\_batches}_p \quad \text{for each } p = 1, 2, \ldots, P
   \]

2. Machine Availability Constraints:
   \[
   \sum_{p=1}^{P} \left( \text{time}_{m,p} \cdot x_p \right) \leq \text{available}_m \quad \text{for each } m = 1, 2, \ldots, M-2
   \]
   
   For machines \( M \) and \( M-1 \) sharing availability:
   \[
   \sum_{p=1}^{P} \left( \text{time}_{M,p} \cdot x_p \right) + \sum_{p=1}^{P} \left( \text{time}_{M-1,p} \cdot x_p \right) \leq \text{available}_M + \text{available}_{M-1}
   \]

3. Non-negativity:
   \[
   x_p \geq 0 \quad \text{for each } p = 1, 2, \ldots, P
   \]

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
time_required = [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]]
machine_costs = [160, 10, 15]
availability = [200, 300, 500]
prices = [570, 250, 585, 430]
min_batches = [10, 10, 10, 10]

P = len(prices)  #### Number of parts
M = len(machine_costs)  #### Number of machines

#### Create the LP problem
problem = pulp.LpProblem("AutoPartsManufacturing", pulp.LpMaximize)

#### Decision Variables
batches = [pulp.LpVariable(f'x_{p+1}', lowBound=min_batches[p], cat='Continuous') for p in range(P)]

#### Objective Function
profit = pulp.lpSum([prices[p] * batches[p] for p in range(P)])
machining_cost = pulp.lpSum([machine_costs[m] * pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) for m in range(M)])
problem += profit - machining_cost

#### Constraints

#### Machine availability constraints for M-2 machines
for m in range(M - 2):
    problem += pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) <= availability[m]

#### Combined machine availability for machines M and M-1
problem += pulp.lpSum([time_required[M-1][p] * batches[p] for p in range(P)]) + pulp.lpSum([time_required[M-2][p] * batches[p] for p in range(P)]) <= availability[M-1] + availability[M-2]

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

