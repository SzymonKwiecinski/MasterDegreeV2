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
To tackle this problem, we need to formulate a linear programming model. The objective is to maximize the total profit by deciding the number of batches for each part to produce and the additional machine hours to purchase.

Here's the formulation of the linear programming model:

```latex
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\section*{Mathematical Model}

Given:
\begin{itemize}
    \item $P$: Number of different parts.
    \item $M$: Number of different machines.
    \item $time_{m,p}$: Time in hours required to produce a batch of part $p$ on machine $m$.
    \item $cost_{m}$: Cost per hour for using machine $m$.
    \item $available_{m}$: Available hours for machine $m$ per month.
    \item $price_{p}$: Selling price per batch of part $p$.
    \item $min\_batches_{p}$: Minimum batches of part $p$ required to be produced each month.
    \item $extra\_cost_{m}$: Additional cost per hour for extra machine time on machine $m$.
    \item $max\_extra_{m}$: Maximum extra hours for machine $m$.
\end{itemize}

Decision Variables:
\begin{align*}
    & batches_{p} \geq 0, && \text{number of batches of part } p \text{ to produce each month.} \\
    & extra\_time_{m} \geq 0, && \text{extra hours purchased for each machine } m.
\end{align*}

Objective Function:
\[
\text{Maximize } \sum_{p=1}^{P} \left( price_{p} \times batches_{p} \right) - \sum_{m=1}^{M} \left( cost_{m} \times \left(\sum_{p=1}^{P} time_{m,p} \times batches_{p} + extra\_time_{m}\right) \right) - \sum_{m=1}^{M} \left( extra\_cost_{m} \times extra\_time_{m} \right)
\]

Subject to:
\begin{align*}
    & \sum_{p=1}^{P} time_{m,p} \times batches_{p} \leq available_{m} + extra\_time_{m}, && \forall m = 1, ..., M \\
    & batches_{p} \geq min\_batches_{p}, && \forall p = 1, ..., P \\
    & extra\_time_{m} \leq max\_extra_{m}, && \forall m = 1, ..., M \\
    & batches_{p} \geq 0, && \forall p = 1, ..., P \\
    & extra\_time_{m} \geq 0, && \forall m = 1, ..., M
\end{align*}

\end{document}
```

This linear program will provide the optimal number of batches for each part to produce and the additional hours to purchase for each machine, while maximizing the profit for the month.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\section*{Mathematical Model}

Given:
\begin{itemize}
    \item $P$: Number of different parts.
    \item $M$: Number of different machines.
    \item $time_{m,p}$: Time in hours required to produce a batch of part $p$ on machine $m$.
    \item $cost_{m}$: Cost per hour for using machine $m$.
    \item $available_{m}$: Available hours for machine $m$ per month.
    \item $price_{p}$: Selling price per batch of part $p$.
    \item $min\_batches_{p}$: Minimum batches of part $p$ required to be produced each month.
    \item $extra\_cost_{m}$: Additional cost per hour for extra machine time on machine $m$.
    \item $max\_extra_{m}$: Maximum extra hours for machine $m$.
\end{itemize}

Decision Variables:
\begin{align*}
    & batches_{p} \geq 0, && \text{number of batches of part } p \text{ to produce each month.} \\
    & extra\_time_{m} \geq 0, && \text{extra hours purchased for each machine } m.
\end{align*}

Objective Function:
\[
\text{Maximize } \sum_{p=1}^{P} \left( price_{p} \times batches_{p} \right) - \sum_{m=1}^{M} \left( cost_{m} \times \left(\sum_{p=1}^{P} time_{m,p} \times batches_{p} + extra\_time_{m}\right) \right) - \sum_{m=1}^{M} \left( extra\_cost_{m} \times extra\_time_{m} \right)
\]

Subject to:
\begin{align*}
    & \sum_{p=1}^{P} time_{m,p} \times batches_{p} \leq available_{m} + extra\_time_{m}, && \forall m = 1, ..., M \\
    & batches_{p} \geq min\_batches_{p}, && \forall p = 1, ..., P \\
    & extra\_time_{m} \leq max\_extra_{m}, && \forall m = 1, ..., M \\
    & batches_{p} \geq 0, && \forall p = 1, ..., P \\
    & extra\_time_{m} \geq 0, && \forall m = 1, ..., M
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10], 'extra_costs': [0, 15, 22.5], 'max_extra': [0, 80, 80]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data in JSON format
data = json.loads('{"time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "machine_costs": [160, 10, 15], "availability": [200, 300, 500], "prices": [570, 250, 585, 430], "min_batches": [10, 10, 10, 10], "extra_costs": [0, 15, 22.5], "max_extra": [0, 80, 80]}')

#### Extracting data
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']
extra_costs = data['extra_costs']
max_extra = data['max_extra']

P = len(prices)
M = len(machine_costs)

#### Initialize problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0)
extra_time = pulp.LpVariable.dicts("extra_time", range(M), lowBound=0)

#### Objective Function
problem += pulp.lpSum(prices[p] * batches[p] for p in range(P)) - \
           pulp.lpSum(machine_costs[m] * (pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) + extra_time[m]) for m in range(M)) - \
           pulp.lpSum(extra_costs[m] * extra_time[m] for m in range(M))

#### Constraints
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m] + extra_time[m]

for p in range(P):
    problem += batches[p] >= min_batches[p]

for m in range(M):
    problem += extra_time[m] <= max_extra[m]

#### Solve problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

