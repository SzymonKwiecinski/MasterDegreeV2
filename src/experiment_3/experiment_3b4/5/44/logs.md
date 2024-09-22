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
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Maximizing Profit}

Let:
\begin{align*}
P & : \text{number of different parts}, \\
M & : \text{number of different machines}, \\
batches_p & : \text{number of batches of part } p \text{ produced per month}, \\
time_{m,p} & : \text{time in hours required on machine } m \text{ for a batch of part } p, \\
cost_m & : \text{cost per hour for using machine } m, \\
available_m & : \text{availability in hours of machine } m \text{ per month}, \\
price_p & : \text{selling price per batch of part } p, \\
min\_batches_p & : \text{minimum number of batches of part } p \text{ required}.
\end{align*}

\subsection*{Objective Function}
The objective is to maximize the total profit, which is the revenue from selling the parts minus the cost of operating the machines.

\begin{align*}
\text{max } & \text{Profit} = \sum_{p=1}^{P} \left( price_p \cdot batches_p \right) - \sum_{m=1}^{M} \left( cost_m \cdot \sum_{p=1}^{P} \left( time_{m,p} \cdot batches_p \right) \right)
\end{align*}

\subsection*{Constraints}
1. Machine availability constraints:
\[
\sum_{p=1}^{P} \left( time_{m,p} \cdot batches_p \right) \leq available_m, \quad \forall m = 1, \ldots, M
\]

2. Minimum contract production constraints:
\[
batches_p \geq min\_batches_p, \quad \forall p = 1, \ldots, P
\]

3. Non-negativity constraints:
\[
batches_p \geq 0, \quad \forall p = 1, \ldots, P
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

Let:
\begin{align*}
P & : \text{number of different parts}, \\
M & : \text{number of different machines}, \\
batches_p & : \text{number of batches of part } p \text{ produced per month}, \\
time_{m,p} & : \text{time in hours required on machine } m \text{ for a batch of part } p, \\
cost_m & : \text{cost per hour for using machine } m, \\
available_m & : \text{availability in hours of machine } m \text{ per month}, \\
price_p & : \text{selling price per batch of part } p, \\
min\_batches_p & : \text{minimum number of batches of part } p \text{ required}.
\end{align*}

\subsection*{Objective Function}
The objective is to maximize the total profit, which is the revenue from selling the parts minus the cost of operating the machines.

\begin{align*}
\text{max } & \text{Profit} = \sum_{p=1}^{P} \left( price_p \cdot batches_p \right) - \sum_{m=1}^{M} \left( cost_m \cdot \sum_{p=1}^{P} \left( time_{m,p} \cdot batches_p \right) \right)
\end{align*}

\subsection*{Constraints}
1. Machine availability constraints:
\[
\sum_{p=1}^{P} \left( time_{m,p} \cdot batches_p \right) \leq available_m, \quad \forall m = 1, \ldots, M
\]

2. Minimum contract production constraints:
\[
batches_p \geq min\_batches_p, \quad \forall p = 1, \ldots, P
\]

3. Non-negativity constraints:
\[
batches_p \geq 0, \quad \forall p = 1, \ldots, P
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

time_required = data['time_required']
cost_m = data['machine_costs']
available_m = data['availability']
price_p = data['prices']
min_batches_p = data['min_batches']

P = len(price_p)
M = len(cost_m)

#### Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
batches = [pulp.LpVariable(f'batches_{p+1}', lowBound=0, cat='Continuous') for p in range(P)]

#### Objective Function
revenue = pulp.lpSum([price_p[p] * batches[p] for p in range(P)])
machine_costs = pulp.lpSum([cost_m[m] * pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) for m in range(M)])

problem += revenue - machine_costs, "Total Profit"

#### Constraints
#### Machine availability
for m in range(M):
    problem += pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) <= available_m[m], f"Machine_Usage_{m+1}"

#### Minimum batch requirements
for p in range(P):
    problem += batches[p] >= min_batches_p[p], f"Min_Batches_{p+1}"

#### Solve
problem.solve()

#### Output
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```


