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

\section*{Linear Programming Model for Maximizing Profit}

\subsection*{Decision Variables}
Let \( x_p \) be the number of batches of part \( p \) produced, where \( p = 1, \ldots, P \).

\subsection*{Objective Function}
We aim to maximize the total profit, which is the total revenue minus the total costs. The total revenue from selling the parts is:

\[
\text{Total Revenue} = \sum_{p=1}^P (\text{price}_p \cdot x_p)
\]

The total cost for machine usage is:

\[
\text{Total Cost} = \sum_{m=1}^M \left( \text{cost}_m \cdot \sum_{p=1}^P \left( \text{time}_{m,p} \cdot x_p \right) \right)
\]

Thus, the objective function is:

\[
\text{Maximize} \quad Z = \sum_{p=1}^P (\text{price}_p \cdot x_p) - \sum_{m=1}^M \left( \text{cost}_m \cdot \sum_{p=1}^P \left( \text{time}_{m,p} \cdot x_p \right) \right)
\]

\subsection*{Constraints}
1. Machine Time Constraints:
   \[
   \sum_{p=1}^P \left( \text{time}_{m,p} \cdot x_p \right) \leq \text{available}_m, \quad \forall m = 1, \ldots, M-2 
   \]

2. Combined Machine Availability for Machine \( M \) and \( M-1 \):
   \[
   \sum_{p=1}^P \left( \text{time}_{M,p} \cdot x_p \right) + \sum_{p=1}^P \left( \text{time}_{M-1,p} \cdot x_p \right) \leq \text{available}_M + \text{available}_{M-1}
   \]

3. Minimum Batch Production Constraints:
   \[
   x_p \geq \text{min\_batches}_p, \quad \forall p = 1, \ldots, P
   \]

4. Non-negativity Constraints:
   \[
   x_p \geq 0, \quad \forall p = 1, \ldots, P
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

\section*{Linear Programming Model for Maximizing Profit}

\subsection*{Decision Variables}
Let \( x_p \) be the number of batches of part \( p \) produced, where \( p = 1, \ldots, P \).

\subsection*{Objective Function}
We aim to maximize the total profit, which is the total revenue minus the total costs. The total revenue from selling the parts is:

\[
\text{Total Revenue} = \sum_{p=1}^P (\text{price}_p \cdot x_p)
\]

The total cost for machine usage is:

\[
\text{Total Cost} = \sum_{m=1}^M \left( \text{cost}_m \cdot \sum_{p=1}^P \left( \text{time}_{m,p} \cdot x_p \right) \right)
\]

Thus, the objective function is:

\[
\text{Maximize} \quad Z = \sum_{p=1}^P (\text{price}_p \cdot x_p) - \sum_{m=1}^M \left( \text{cost}_m \cdot \sum_{p=1}^P \left( \text{time}_{m,p} \cdot x_p \right) \right)
\]

\subsection*{Constraints}
1. Machine Time Constraints:
   \[
   \sum_{p=1}^P \left( \text{time}_{m,p} \cdot x_p \right) \leq \text{available}_m, \quad \forall m = 1, \ldots, M-2 
   \]

2. Combined Machine Availability for Machine \( M \) and \( M-1 \):
   \[
   \sum_{p=1}^P \left( \text{time}_{M,p} \cdot x_p \right) + \sum_{p=1}^P \left( \text{time}_{M-1,p} \cdot x_p \right) \leq \text{available}_M + \text{available}_{M-1}
   \]

3. Minimum Batch Production Constraints:
   \[
   x_p \geq \text{min\_batches}_p, \quad \forall p = 1, \ldots, P
   \]

4. Non-negativity Constraints:
   \[
   x_p \geq 0, \quad \forall p = 1, \ldots, P
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

#### Problem Variables
P = len(data['prices'])    #### Number of parts
M = len(data['machine_costs'])  #### Number of machines

#### Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
x = [pulp.LpVariable(f"x_{p+1}", lowBound=data['min_batches'][p], cat='Continuous') for p in range(P)]

#### Objective Function
revenue = pulp.lpSum([data['prices'][p] * x[p] for p in range(P)])
cost = pulp.lpSum([data['machine_costs'][m] * pulp.lpSum([data['time_required'][m][p] * x[p] for p in range(P)]) for m in range(M)])
problem += revenue - cost

#### Constraints

#### Machine Time Constraints
for m in range(M-2):
    problem += pulp.lpSum([data['time_required'][m][p] * x[p] for p in range(P)]) <= data['availability'][m]

#### Combined Machine Availability for Machine M and M-1
problem += pulp.lpSum([data['time_required'][M-1][p] * x[p] for p in range(P)]) + \
           pulp.lpSum([data['time_required'][M-2][p] * x[p] for p in range(P)]) <= data['availability'][M-1] + data['availability'][M-2]

#### Minimum Batch Production Constraints
for p in range(P):
    problem += x[p] >= data['min_batches'][p]

#### Solve the problem
problem.solve()

#### Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

