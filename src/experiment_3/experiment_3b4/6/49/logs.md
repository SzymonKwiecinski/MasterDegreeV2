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
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Auto Parts Manufacturer}

\subsection*{Sets and Indices}
- Let \( P \) denote the set of parts produced, indexed by \( p = 1, 2, \ldots, P \).
- Let \( M \) denote the set of machines available, indexed by \( m = 1, 2, \ldots, M \).

\subsection*{Parameters}
- \( \text{time\_required}_{m,p} \): Time required in hours on machine \( m \) to produce a batch of part \( p \).
- \( \text{cost}_{m} \): Cost per hour for using machine \( m \).
- \( \text{available}_{m} \): Available hours per month for machine \( m \).
- \( \text{price}_{p} \): Selling price per batch of part \( p \).
- \( \text{min\_batches}_{p} \): Minimum number of batches required for part \( p \).

\subsection*{Decision Variables}
- \( \text{batches}_{p} \): Number of batches of part \( p \) to produce each month.

\subsection*{Objective Function}
Maximize the total profit, which is the revenue from selling the parts minus the cost of operating the machines:

\[
\text{Maximize } Z = \sum_{p=1}^{P} (\text{price}_{p} \times \text{batches}_{p}) - \sum_{m=1}^{M} (\text{cost}_{m} \times \sum_{p=1}^{P} \text{time\_required}_{m,p} \times \text{batches}_{p})
\]

\subsection*{Constraints}

1. **Minimum Production Requirement**: Ensure the minimum number of batches for each part are produced:
   \[
   \text{batches}_{p} \geq \text{min\_batches}_{p}, \quad \forall p = 1, 2, \ldots, P
   \]

2. **Machine Availability Constraints**: Machines can only be used up to their available hours per month. For machines \( M \) and \( M-1 \), they can share their availability:
   \[
   \sum_{p=1}^{P} \text{time\_required}_{m,p} \times \text{batches}_{p} \leq \text{available}_{m}, \quad \forall m = 1, 2, \ldots, M-2
   \]

   \[
   \sum_{p=1}^{P} \text{time\_required}_{M,p} \times \text{batches}_{p} + \sum_{p=1}^{P} \text{time\_required}_{M-1,p} \times \text{batches}_{p} \leq \text{available}_{M} + \text{available}_{M-1}
   \]

3. **Non-negativity**: 
   \[
   \text{batches}_{p} \geq 0, \quad \forall p = 1, 2, \ldots, P
   \]

\end{document}
```

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Auto Parts Manufacturer}

\subsection*{Sets and Indices}
- Let \( P \) denote the set of parts produced, indexed by \( p = 1, 2, \ldots, P \).
- Let \( M \) denote the set of machines available, indexed by \( m = 1, 2, \ldots, M \).

\subsection*{Parameters}
- \( \text{time\_required}_{m,p} \): Time required in hours on machine \( m \) to produce a batch of part \( p \).
- \( \text{cost}_{m} \): Cost per hour for using machine \( m \).
- \( \text{available}_{m} \): Available hours per month for machine \( m \).
- \( \text{price}_{p} \): Selling price per batch of part \( p \).
- \( \text{min\_batches}_{p} \): Minimum number of batches required for part \( p \).

\subsection*{Decision Variables}
- \( \text{batches}_{p} \): Number of batches of part \( p \) to produce each month.

\subsection*{Objective Function}
Maximize the total profit, which is the revenue from selling the parts minus the cost of operating the machines:

\[
\text{Maximize } Z = \sum_{p=1}^{P} (\text{price}_{p} \times \text{batches}_{p}) - \sum_{m=1}^{M} (\text{cost}_{m} \times \sum_{p=1}^{P} \text{time\_required}_{m,p} \times \text{batches}_{p})
\]

\subsection*{Constraints}

1. **Minimum Production Requirement**: Ensure the minimum number of batches for each part are produced:
   \[
   \text{batches}_{p} \geq \text{min\_batches}_{p}, \quad \forall p = 1, 2, \ldots, P
   \]

2. **Machine Availability Constraints**: Machines can only be used up to their available hours per month. For machines \( M \) and \( M-1 \), they can share their availability:
   \[
   \sum_{p=1}^{P} \text{time\_required}_{m,p} \times \text{batches}_{p} \leq \text{available}_{m}, \quad \forall m = 1, 2, \ldots, M-2
   \]

   \[
   \sum_{p=1}^{P} \text{time\_required}_{M,p} \times \text{batches}_{p} + \sum_{p=1}^{P} \text{time\_required}_{M-1,p} \times \text{batches}_{p} \leq \text{available}_{M} + \text{available}_{M-1}
   \]

3. **Non-negativity**: 
   \[
   \text{batches}_{p} \geq 0, \quad \forall p = 1, 2, \ldots, P
   \]

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10]
}

#### Parameters
P = len(data['prices'])    #### Number of parts
M = len(data['machine_costs'])  #### Number of machines

#### Problem
problem = pulp.LpProblem("AutoPartsManufacturer", pulp.LpMaximize)

#### Decision Variables
batches_vars = [pulp.LpVariable(f'batches_{p}', lowBound=0, cat='Continuous') for p in range(P)]

#### Objective Function
revenue = pulp.lpSum(data['prices'][p] * batches_vars[p] for p in range(P))
cost = pulp.lpSum(data['machine_costs'][m] * pulp.lpSum(data['time_required'][m][p] * batches_vars[p] for p in range(P)) for m in range(M))
problem += revenue - cost

#### Constraints

#### Minimum Production Requirement
for p in range(P):
    problem += batches_vars[p] >= data['min_batches'][p]

#### Machine Availability Constraints for 1 to M-2
for m in range(M-2):
    problem += pulp.lpSum(data['time_required'][m][p] * batches_vars[p] for p in range(P)) <= data['availability'][m]

#### Combined machine availability for M-1 and M
problem += (pulp.lpSum(data['time_required'][M-1][p] * batches_vars[p] for p in range(P)) + 
            pulp.lpSum(data['time_required'][M-2][p] * batches_vars[p] for p in range(P)) <= 
            data['availability'][M-1] + data['availability'][M-2])

#### Solve
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

