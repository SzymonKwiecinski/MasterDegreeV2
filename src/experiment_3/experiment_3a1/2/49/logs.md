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

\subsection*{Variables}
Let \(batches_{p}\) be the number of batches produced for part \(p\), where \(p = 1, \ldots, P\).

\subsection*{Objective Function}
The objective is to maximize total profit, which can be expressed as: 
\[
\text{Maximize } Z = \sum_{p=1}^{P} \left( price_{p} \cdot batches_{p} - \sum_{m=1}^{M} (cost_{m} \cdot time_{m,p} \cdot batches_{p}) \right)
\]

\subsection*{Constraints}
1. **Machine Time Availability**: Ensure that the total time required on each machine does not exceed its availability.
   \[
   \sum_{p=1}^{P} time_{m,p} \cdot batches_{p} \leq available_{m} \quad \forall m = 1, \ldots, M
   \]
   Note that Machine \(M\) and Machine \(M-1\) can share availability.

2. **Minimum Production Requirement**: Each part must meet its minimum batch requirement.
   \[
   batches_{p} \geq min\_batches_{p} \quad \forall p = 1, \ldots, P
   \]

\subsection*{Non-negativity Constraints}
\[
batches_{p} \geq 0 \quad \forall p = 1, \ldots, P
\]

\subsection*{Output}
The result will provide the number of batches produced for each part:
\[
\text{Output: } \{ batches = [batches_{1}, batches_{2}, \ldots, batches_{P}], total\_profit = Z \}
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

\subsection*{Variables}
Let \(batches_{p}\) be the number of batches produced for part \(p\), where \(p = 1, \ldots, P\).

\subsection*{Objective Function}
The objective is to maximize total profit, which can be expressed as: 
\[
\text{Maximize } Z = \sum_{p=1}^{P} \left( price_{p} \cdot batches_{p} - \sum_{m=1}^{M} (cost_{m} \cdot time_{m,p} \cdot batches_{p}) \right)
\]

\subsection*{Constraints}
1. **Machine Time Availability**: Ensure that the total time required on each machine does not exceed its availability.
   \[
   \sum_{p=1}^{P} time_{m,p} \cdot batches_{p} \leq available_{m} \quad \forall m = 1, \ldots, M
   \]
   Note that Machine \(M\) and Machine \(M-1\) can share availability.

2. **Minimum Production Requirement**: Each part must meet its minimum batch requirement.
   \[
   batches_{p} \geq min\_batches_{p} \quad \forall p = 1, \ldots, P
   \]

\subsection*{Non-negativity Constraints}
\[
batches_{p} \geq 0 \quad \forall p = 1, \ldots, P
\]

\subsection*{Output}
The result will provide the number of batches produced for each part:
\[
\text{Output: } \{ batches = [batches_{1}, batches_{2}, \ldots, batches_{P}], total\_profit = Z \}
\]

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data input
data = json.loads('{"time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "machine_costs": [160, 10, 15], "availability": [200, 300, 500], "prices": [570, 250, 585, 430], "min_batches": [10, 10, 10, 10]}')

#### Extracting data from the JSON
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']

#### Number of parts and machines
P = len(prices)
M = len(machine_costs)

#### Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Create decision variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0)

#### Objective function
profit_expr = pulp.lpSum([
    prices[p] * batches[p] - 
    pulp.lpSum([machine_costs[m] * time_required[m][p] * batches[p] for m in range(M)])
    for p in range(P)
])
problem += profit_expr, "Total_Profit"

#### Constraints
#### Machine Time Availability
for m in range(M):
    problem += pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) <= availability[m], f"Availability_Constraint_Machine_{m+1}"

#### Minimum Production Requirement
for p in range(P):
    problem += batches[p] >= min_batches[p], f"Min_Batch_Requirement_Part_{p+1}"

#### Solve the problem
problem.solve()

#### Output results
batches_produced = [batches[p].varValue for p in range(P)]
total_profit = pulp.value(problem.objective)

#### Print the objective value
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')
```

