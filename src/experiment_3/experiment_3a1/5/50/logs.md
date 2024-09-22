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
- Extra available time for machine \var{m} can be acquired at $\var{extra_costs_{m}}/hour. 
- Up to \var{max_extra_{m}} hours can be purchased for each machine \var{m}.

INPUT FORMAT: 

{
    "time_required": [[time_{m,p} for p in 1, ..., P] for m in 1, ..., M],
    "machine_costs": [cost_{m} for m in 1, ..., M],
    "availability": [available_{m} for m in 1, ..., M],
    "prices": [price_{p} for p in 1, ..., P],
    "min_batches": [min_batches_{p} for p in 1, ..., P],
    "extra_costs": [extra_cost_{m} for m in 1, ..., M],
    "max_extra": [max_extra_{m} for m in 1, ..., M]
}

OBJECTIVE: How many batches of each part should the manufacturer produce each month to maximize profit?

OUTPUT INFO:

- the number of batches of each part produced \var{batches_{p}}.
- \var{extra_time} denotes the additional hours purchased for each machine \var{m}.
- \var{total_profit} represents the total profit obtained for the month.

OUTPUT FORMAT:

{
    "batches": [batches_{p} for p in 1, ..., P],
    "extra_time": [extra_time_{p} for p in 1, ..., P],
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
\begin{align*}
x_p & = \text{number of batches produced for part } p \quad \text{for } p = 1, \ldots, P \\
y_m & = \text{extra hours purchased for machine } m \quad \text{for } m = 1, \ldots, M 
\end{align*}

\subsection*{Parameters}
\begin{align*}
\text{time}_{m,p} & = \text{time required on machine } m \text{ to produce one batch of part } p \quad \forall m, p \\
\text{cost}_m & = \text{cost per hour for using machine } m \quad \forall m \\
\text{available}_m & = \text{available hours for machine } m \text{ per month} \quad \forall m \\
\text{price}_p & = \text{price per batch of part } p \quad \forall p \\
\text{min\_batches}_p & = \text{minimum batches of part } p \text{ needed} \quad \forall p \\
\text{extra\_costs}_m & = \text{cost per hour for extra machine time for machine } m \quad \forall m \\
\text{max\_extra}_m & = \text{maximum extra hours that can be purchased for machine } m \quad \forall m 
\end{align*}

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Total Profit} = \sum_{p=1}^{P} \text{price}_p \cdot x_p - \sum_{m=1}^{M} \text{cost}_m \cdot \left(\text{available}_m + y_m\right) - \sum_{m=1}^{M} \text{extra\_costs}_m \cdot y_m
\]

\subsection*{Constraints}
1. Time constraints for each machine:
\[
\sum_{p=1}^{P} \text{time}_{m,p} \cdot x_p \leq \text{available}_m + y_m \quad \forall m
\]
2. Minimum production requirements:
\[
x_p \geq \text{min\_batches}_p \quad \forall p
\]
3. Maximum extra hours constraints:
\[
y_m \leq \text{max\_extra}_m \quad \forall m
\]
4. Non-negativity constraints:
\[
x_p \geq 0 \quad \forall p \\
y_m \geq 0 \quad \forall m 
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
\begin{align*}
x_p & = \text{number of batches produced for part } p \quad \text{for } p = 1, \ldots, P \\
y_m & = \text{extra hours purchased for machine } m \quad \text{for } m = 1, \ldots, M 
\end{align*}

\subsection*{Parameters}
\begin{align*}
\text{time}_{m,p} & = \text{time required on machine } m \text{ to produce one batch of part } p \quad \forall m, p \\
\text{cost}_m & = \text{cost per hour for using machine } m \quad \forall m \\
\text{available}_m & = \text{available hours for machine } m \text{ per month} \quad \forall m \\
\text{price}_p & = \text{price per batch of part } p \quad \forall p \\
\text{min\_batches}_p & = \text{minimum batches of part } p \text{ needed} \quad \forall p \\
\text{extra\_costs}_m & = \text{cost per hour for extra machine time for machine } m \quad \forall m \\
\text{max\_extra}_m & = \text{maximum extra hours that can be purchased for machine } m \quad \forall m 
\end{align*}

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Total Profit} = \sum_{p=1}^{P} \text{price}_p \cdot x_p - \sum_{m=1}^{M} \text{cost}_m \cdot \left(\text{available}_m + y_m\right) - \sum_{m=1}^{M} \text{extra\_costs}_m \cdot y_m
\]

\subsection*{Constraints}
1. Time constraints for each machine:
\[
\sum_{p=1}^{P} \text{time}_{m,p} \cdot x_p \leq \text{available}_m + y_m \quad \forall m
\]
2. Minimum production requirements:
\[
x_p \geq \text{min\_batches}_p \quad \forall p
\]
3. Maximum extra hours constraints:
\[
y_m \leq \text{max\_extra}_m \quad \forall m
\]
4. Non-negativity constraints:
\[
x_p \geq 0 \quad \forall p \\
y_m \geq 0 \quad \forall m 
\]

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10], 'extra_costs': [0, 15, 22.5], 'max_extra': [0, 80, 80]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Load data
data = json.loads('{"time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "machine_costs": [160, 10, 15], "availability": [200, 300, 500], "prices": [570, 250, 585, 430], "min_batches": [10, 10, 10, 10], "extra_costs": [0, 15, 22.5], "max_extra": [0, 80, 80]}')

#### Parameters
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']
extra_costs = data['extra_costs']
max_extra = data['max_extra']

P = len(prices)
M = len(machine_costs)

#### Create the problem
problem = pulp.LpProblem("Auto_Parts_Manufacturer", pulp.LpMaximize)

#### Variables
x = pulp.LpVariable.dicts("x", range(P), lowBound=0, cat='Continuous')  #### batches produced for part p
y = pulp.LpVariable.dicts("y", range(M), lowBound=0, upBound=max_extra, cat='Continuous')  #### extra hours purchased for machine m

#### Objective Function
problem += pulp.lpSum(prices[p] * x[p] for p in range(P)) - \
           pulp.lpSum(machine_costs[m] * (availability[m] + y[m]) for m in range(M)) - \
           pulp.lpSum(extra_costs[m] * y[m] for m in range(M)), "Total Profit"

#### Constraints
#### Time constraints for each machine
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * x[p] for p in range(P)) <= availability[m] + y[m], f"Machine_{m+1}_Time_Constraint"

#### Minimum production requirements
for p in range(P):
    problem += x[p] >= min_batches[p], f"Min_Batches_Required_for_Part_{p+1}"

#### Non-negativity constraints are already defined by default

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

