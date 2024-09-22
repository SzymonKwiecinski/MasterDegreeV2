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
To formulate this problem as a linear programming model, we need to define the decision variables, objective function, and constraints based on the given information.

Let:
- \( x_p \) be the number of batches of part \( p \) to be produced.
- \( e_m \) be the extra hours purchased for machine \( m \).

Given:
- \( time_{m,p} \) is the time in hours machine \( m \) requires to produce a batch of part \( p \).
- \( cost_m \) is the hourly cost for using machine \( m \).
- \( available_m \) is the available hours per month for machine \( m \).
- \( price_p \) is the selling price per batch of part \( p \).
- \( min\_batches_p \) is the minimum number of batches of part \( p \) to fulfill contracts.
- \( extra\_cost_m \) is the cost of acquiring additional hours for machine \( m \).
- \( max\_extra_m \) is the maximum additional hours that can be purchased for machine \( m \).

Objective:
Maximize the profit, which is the total revenue minus the total cost (including costs of using machines and purchasing extra machine hours).

Constraints:
1. Production constraints based on machine hours.
2. Contractual constraints for the minimum production of parts.
3. Limits on extra hours that can be purchased.

The linear programming model in LaTeX is as follows:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\subsection*{Decision Variables}
\begin{align*}
x_p &: \text{Number of batches of part } p \text{ to be produced} \\
e_m &: \text{Extra hours purchased for machine } m
\end{align*}

\subsection*{Objective Function}
Maximize the total profit:
\[
Z = \sum_{p=1}^{P} price_p \cdot x_p - \sum_{m=1}^{M} \left( cost_m \cdot \sum_{p=1}^{P} time_{m,p} \cdot x_p + extra\_cost_m \cdot e_m \right)
\]

\subsection*{Constraints}
\begin{align*}
\text{Machine availability constraints:} \\
& \sum_{p=1}^{P} time_{m,p} \cdot x_p \leq available_m + e_m, \quad \forall m = 1, \ldots, M \\

\text{Minimum production constraints:} \\
& x_p \geq min\_batches_p, \quad \forall p = 1, \ldots, P \\

\text{Extra hours constraints:} \\
& 0 \leq e_m \leq max\_extra_m, \quad \forall m = 1, \ldots, M \\

\text{Non-negativity constraints:} \\
& x_p \geq 0, \quad \forall p = 1, \ldots, P \\
& e_m \geq 0, \quad \forall m = 1, \ldots, M 
\end{align*}

\end{document}
```

This formulation will allow you to find the optimal number of batches of each part to produce and the extra time to purchase for each machine to maximize the monthly profit.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\subsection*{Decision Variables}
\begin{align*}
x_p &: \text{Number of batches of part } p \text{ to be produced} \\
e_m &: \text{Extra hours purchased for machine } m
\end{align*}

\subsection*{Objective Function}
Maximize the total profit:
\[
Z = \sum_{p=1}^{P} price_p \cdot x_p - \sum_{m=1}^{M} \left( cost_m \cdot \sum_{p=1}^{P} time_{m,p} \cdot x_p + extra\_cost_m \cdot e_m \right)
\]

\subsection*{Constraints}
\begin{align*}
\text{Machine availability constraints:} \\
& \sum_{p=1}^{P} time_{m,p} \cdot x_p \leq available_m + e_m, \quad \forall m = 1, \ldots, M \\

\text{Minimum production constraints:} \\
& x_p \geq min\_batches_p, \quad \forall p = 1, \ldots, P \\

\text{Extra hours constraints:} \\
& 0 \leq e_m \leq max\_extra_m, \quad \forall m = 1, \ldots, M \\

\text{Non-negativity constraints:} \\
& x_p \geq 0, \quad \forall p = 1, \ldots, P \\
& e_m \geq 0, \quad \forall m = 1, \ldots, M 
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10], 'extra_costs': [0, 15, 22.5], 'max_extra': [0, 80, 80]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data provided
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
    'machine_costs': [160, 10, 15], 
    'availability': [200, 300, 500], 
    'prices': [570, 250, 585, 430], 
    'min_batches': [10, 10, 10, 10], 
    'extra_costs': [0, 15, 22.5], 
    'max_extra': [0, 80, 80]
}

#### Numbers of parts and machines
P = len(data['prices'])
M = len(data['machine_costs'])

#### Decision Variables
x = [pulp.LpVariable(f"x_{p}", lowBound=data['min_batches'][p]) for p in range(P)]
e = [pulp.LpVariable(f"e_{m}", lowBound=0, upBound=data['max_extra'][m]) for m in range(M)]

#### Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Objective Function
profit = pulp.lpSum(data['prices'][p] * x[p] for p in range(P))
machine_costs = pulp.lpSum(
    data['machine_costs'][m] * pulp.lpSum(data['time_required'][m][p] * x[p] for p in range(P)) + data['extra_costs'][m] * e[m]
    for m in range(M)
)
problem += profit - machine_costs

#### Constraints
#### Machine availability constraints
for m in range(M):
    problem += pulp.lpSum(data['time_required'][m][p] * x[p] for p in range(P)) <= data['availability'][m] + e[m]

#### Solve the problem
problem.solve()

#### Print the objectives
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

