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

\textbf{Variables:}

Let \( b_p \) be the number of batches of part \( p \) produced per month, where \( p = 1, 2, \ldots, P \).

\textbf{Objective Function:}

Maximize the total profit:
\[
\text{Maximize } Z = \sum_{p=1}^{P} \left( \text{price}_p \cdot b_p \right) - \sum_{m=1}^{M} \left( \text{cost}_m \cdot \sum_{p=1}^{P} (time_{m,p} \cdot b_p) \right)
\]

\textbf{Subject to:}

1. **Machine Availability Constraints**:
   \[
   \sum_{p=1}^{P} (time_{m,p} \cdot b_p) \leq \text{available}_m \quad \text{for each } m = 1, \ldots, M
   \]

2. **Shared Availability for Machine \( M \) and Machine \( M-1 \)**:
   \[
   \sum_{p=1}^{P} (time_{M,p} \cdot b_p) + \sum_{p=1}^{P} (time_{M-1,p} \cdot b_p) \leq \text{available}_{M} + \text{available}_{M-1}
   \]

3. **Minimum Production Requirements**:
   \[
   b_p \geq \text{min\_batches}_p \quad \text{for each } p = 1, \ldots, P
   \]

\textbf{Non-negativity Constraints:}
\[
b_p \geq 0 \quad \text{for each } p = 1, \ldots, P
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

\textbf{Variables:}

Let \( b_p \) be the number of batches of part \( p \) produced per month, where \( p = 1, 2, \ldots, P \).

\textbf{Objective Function:}

Maximize the total profit:
\[
\text{Maximize } Z = \sum_{p=1}^{P} \left( \text{price}_p \cdot b_p \right) - \sum_{m=1}^{M} \left( \text{cost}_m \cdot \sum_{p=1}^{P} (time_{m,p} \cdot b_p) \right)
\]

\textbf{Subject to:}

1. **Machine Availability Constraints**:
   \[
   \sum_{p=1}^{P} (time_{m,p} \cdot b_p) \leq \text{available}_m \quad \text{for each } m = 1, \ldots, M
   \]

2. **Shared Availability for Machine \( M \) and Machine \( M-1 \)**:
   \[
   \sum_{p=1}^{P} (time_{M,p} \cdot b_p) + \sum_{p=1}^{P} (time_{M-1,p} \cdot b_p) \leq \text{available}_{M} + \text{available}_{M-1}
   \]

3. **Minimum Production Requirements**:
   \[
   b_p \geq \text{min\_batches}_p \quad \text{for each } p = 1, \ldots, P
   \]

\textbf{Non-negativity Constraints:}
\[
b_p \geq 0 \quad \text{for each } p = 1, \ldots, P
\]

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data in JSON format
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10]
}

#### Extract data
time_required = data['time_required']  #### time_required[m][p]
machine_costs = data['machine_costs']  #### cost_m
availability = data['availability']      #### available_m
prices = data['prices']                  #### price_p
min_batches = data['min_batches']        #### min_batches_p

#### Define problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Number of parts and machines
P = len(prices)
M = len(machine_costs)

#### Decision Variables
b = pulp.LpVariable.dicts("b", range(P), lowBound=0)

#### Objective Function
profit = pulp.lpSum(prices[p] * b[p] for p in range(P)) - \
         pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * b[p] for p in range(P)) for m in range(M))

problem += profit, "Total_Profit"

#### Machine Availability Constraints
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * b[p] for p in range(P)) <= availability[m], f"Availability_Constraint_{m+1}"

#### Shared Availability Constraint for last two machines
problem += pulp.lpSum(time_required[M-1][p] * b[p] for p in range(P)) + \
           pulp.lpSum(time_required[M-2][p] * b[p] for p in range(P)) <= \
           availability[M-1] + availability[M-2], "Shared_Availability_Constraint"

#### Minimum Production Requirements
for p in range(P):
    problem += b[p] >= min_batches[p], f"Min_Production_Requirement_{p+1}"

#### Solve the problem
problem.solve()

#### Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

