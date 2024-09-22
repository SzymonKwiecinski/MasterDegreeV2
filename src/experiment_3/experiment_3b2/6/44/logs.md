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
To solve this linear programming problem, we need to formulate the mathematical model that captures the objective and constraints described. We aim to determine how many batches of each part should be produced to maximize profit, considering the constraints on machine time availability and minimum batch production.

Below is the linear programming model in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Formulation}

\subsection*{Decision Variables}
Let \( \text{batches}_p \) be the number of batches of part \( p \) produced, where \( p = 1, \ldots, P \).

\subsection*{Objective Function}
Maximize the profit, which is total revenue minus total cost:
\[
\text{Profit} = \sum_{p=1}^{P} \left( \text{price}_p \times \text{batches}_p \right) - \sum_{m=1}^{M} \left( \text{cost}_m \times \sum_{p=1}^{P} \text{time}_{m,p} \times \text{batches}_p \right)
\]

\subsection*{Constraints}

1. Machine availability constraints:
   \[
   \sum_{p=1}^{P} \text{time}_{m,p} \times \text{batches}_p \leq \text{available}_m, \quad \forall m = 1, \ldots, M
   \]

2. Minimum batch production constraints:
   \[
   \text{batches}_p \geq \text{min\_batches}_p, \quad \forall p = 1, \ldots, P
   \]

3. Non-negativity constraints:
   \[
   \text{batches}_p \geq 0, \quad \forall p = 1, \ldots, P
   \]

\subsection*{Objective}
Formulate the objective as
\[
\text{Maximize } Z = \sum_{p=1}^{P} \left( \text{price}_p \times \text{batches}_p \right) - \sum_{m=1}^{M} \left( \text{cost}_m \times \sum_{p=1}^{P} \text{time}_{m,p} \times \text{batches}_p \right)
\]

\subsection*{Subject to}
\[
\begin{align*}
& \sum_{p=1}^{P} \text{time}_{m,p} \times \text{batches}_p \leq \text{available}_m, && \forall m = 1, \ldots, M \\
& \text{batches}_p \geq \text{min\_batches}_p, && \forall p = 1, \ldots, P \\
& \text{batches}_p \geq 0, && \forall p = 1, \ldots, P
\end{align*}
\]

\end{document}
```

This model aims to maximize the profitability by optimizing the number of batches produced while respecting the constraints of machine availability and contract obligations. Each term in the objective function accounts for the revenue from selling parts and the cost incurred for machine usage.

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
Let \( \text{batches}_p \) be the number of batches of part \( p \) produced, where \( p = 1, \ldots, P \).

\subsection*{Objective Function}
Maximize the profit, which is total revenue minus total cost:
\[
\text{Profit} = \sum_{p=1}^{P} \left( \text{price}_p \times \text{batches}_p \right) - \sum_{m=1}^{M} \left( \text{cost}_m \times \sum_{p=1}^{P} \text{time}_{m,p} \times \text{batches}_p \right)
\]

\subsection*{Constraints}

1. Machine availability constraints:
   \[
   \sum_{p=1}^{P} \text{time}_{m,p} \times \text{batches}_p \leq \text{available}_m, \quad \forall m = 1, \ldots, M
   \]

2. Minimum batch production constraints:
   \[
   \text{batches}_p \geq \text{min\_batches}_p, \quad \forall p = 1, \ldots, P
   \]

3. Non-negativity constraints:
   \[
   \text{batches}_p \geq 0, \quad \forall p = 1, \ldots, P
   \]

\subsection*{Objective}
Formulate the objective as
\[
\text{Maximize } Z = \sum_{p=1}^{P} \left( \text{price}_p \times \text{batches}_p \right) - \sum_{m=1}^{M} \left( \text{cost}_m \times \sum_{p=1}^{P} \text{time}_{m,p} \times \text{batches}_p \right)
\]

\subsection*{Subject to}
\[
\begin{align*}
& \sum_{p=1}^{P} \text{time}_{m,p} \times \text{batches}_p \leq \text{available}_m, && \forall m = 1, \ldots, M \\
& \text{batches}_p \geq \text{min\_batches}_p, && \forall p = 1, \ldots, P \\
& \text{batches}_p \geq 0, && \forall p = 1, \ldots, P
\end{align*}
\]

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data provided in JSON format
data = json.loads('{"time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "machine_costs": [160, 10, 15], "availability": [200, 300, 500], "prices": [570, 250, 585, 430], "min_batches": [10, 10, 10, 10]}')

#### Extracting data from JSON
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']

P = len(prices)  #### Number of products
M = len(machine_costs)  #### Number of machines

#### Create a linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0)

#### Objective function
profit = pulp.lpSum(prices[p] * batches[p] for p in range(P))
costs = pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) for m in range(M))
problem += profit - costs

#### Constraints
#### Machine availability constraints
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m]

#### Minimum batch production constraints
for p in range(P):
    problem += batches[p] >= min_batches[p]

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

