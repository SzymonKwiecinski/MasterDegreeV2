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
To model the given problem as a linear programming problem, we need to define decision variables, the objective function, and the constraints.

**Decision Variables:**
- Let \( x_p \) be the number of batches of part \( p \) produced (\( p = 1, \ldots, P \)).
- Let \( e_m \) be the extra hours purchased for machine \( m \) (\( m = 1, \ldots, M \)).

**Objective Function:**
The objective is to maximize the total profit, which is the difference between the revenue and the total cost. The revenue for part \( p \) is given by \( \text{price}_p \times x_p \). The total cost includes:
- The machine usage cost: \( \sum_{m=1}^M \sum_{p=1}^P \text{time}_{m,p} \times x_p \times \text{cost}_m \).
- The extra hours cost: \( \sum_{m=1}^M e_m \times \text{extra\_cost}_m \).

Thus, the objective function to maximize is:
\[
\text{Maximize:} \quad \sum_{p=1}^P (\text{price}_p \times x_p) - \sum_{m=1}^M \left( \sum_{p=1}^P \text{time}_{m,p} \times x_p \times \text{cost}_m + e_m \times \text{extra\_cost}_m \right)
\]

**Constraints:**
1. Time availability on machines:
   \[
   \sum_{p=1}^P \text{time}_{m,p} \times x_p \leq \text{available}_m + e_m, \quad \forall m = 1, \ldots, M
   \]
2. Minimum production requirement:
   \[
   x_p \geq \text{min\_batches}_p, \quad \forall p = 1, \ldots, P
   \]
3. Non-negativity and extra time limits:
   \[
   x_p \geq 0, \quad e_m \geq 0 \quad \text{and} \quad e_m \leq \text{max\_extra}_m, \quad \forall m = 1, \ldots, M
   \]

Here is the mathematical model in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\subsection*{Indices}
\begin{align*}
    p &= 1, \ldots, P \quad \text{(parts)} \\
    m &= 1, \ldots, M \quad \text{(machines)}
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
    x_p &= \text{Number of batches of part } p \\
    e_m &= \text{Extra hours purchased for machine } m
\end{align*}

\subsection*{Objective Function}
\[
\text{Maximize:} \quad \sum_{p=1}^P (\text{price}_p \times x_p) - \sum_{m=1}^M \left( \sum_{p=1}^P \text{time}_{m,p} \times x_p \times \text{cost}_m + e_m \times \text{extra\_cost}_m \right)
\]

\subsection*{Constraints}
\begin{align*}
    &\sum_{p=1}^P \text{time}_{m,p} \times x_p \leq \text{available}_m + e_m, \quad \forall m = 1, \ldots, M \\
    &x_p \geq \text{min\_batches}_p, \quad \forall p = 1, \ldots, P \\
    &x_p \geq 0, \quad e_m \geq 0 \quad \text{and} \quad e_m \leq \text{max\_extra}_m, \quad \forall m = 1, \ldots, M
\end{align*}

\end{document}
```

This LaTeX code defines the complete linear programming model for the problem. The model aims to maximize profit by determining the optimal number of batches to produce and any extra machine hours to purchase, subject to constraints on machine availability and minimum production requirements.

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

\subsection*{Indices}
\begin{align*}
    p &= 1, \ldots, P \quad \text{(parts)} \\
    m &= 1, \ldots, M \quad \text{(machines)}
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
    x_p &= \text{Number of batches of part } p \\
    e_m &= \text{Extra hours purchased for machine } m
\end{align*}

\subsection*{Objective Function}
\[
\text{Maximize:} \quad \sum_{p=1}^P (\text{price}_p \times x_p) - \sum_{m=1}^M \left( \sum_{p=1}^P \text{time}_{m,p} \times x_p \times \text{cost}_m + e_m \times \text{extra\_cost}_m \right)
\]

\subsection*{Constraints}
\begin{align*}
    &\sum_{p=1}^P \text{time}_{m,p} \times x_p \leq \text{available}_m + e_m, \quad \forall m = 1, \ldots, M \\
    &x_p \geq \text{min\_batches}_p, \quad \forall p = 1, \ldots, P \\
    &x_p \geq 0, \quad e_m \geq 0 \quad \text{and} \quad e_m \leq \text{max\_extra}_m, \quad \forall m = 1, \ldots, M
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10], 'extra_costs': [0, 15, 22.5], 'max_extra': [0, 80, 80]}</DATA>


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
    'min_batches': [10, 10, 10, 10], 
    'extra_costs': [0, 15, 22.5], 
    'max_extra': [0, 80, 80]
}

#### Indices
P = len(data['prices'])  #### Number of parts
M = len(data['availability'])  #### Number of machines

#### Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
x = [pulp.LpVariable(f'x_{p}', lowBound=data['min_batches'][p]) for p in range(P)]
e = [pulp.LpVariable(f'e_{m}', lowBound=0, upBound=data['max_extra'][m]) for m in range(M)]

#### Objective Function
profit_terms = [data['prices'][p] * x[p] for p in range(P)]
cost_terms = [data['time_required'][m][p] * x[p] * data['machine_costs'][m] for m in range(M) for p in range(P)]
extra_hours_costs = [e[m] * data['extra_costs'][m] for m in range(M)]

problem += pulp.lpSum(profit_terms) - (pulp.lpSum(cost_terms) + pulp.lpSum(extra_hours_costs))

#### Constraints
for m in range(M):
    problem += pulp.lpSum(data['time_required'][m][p] * x[p] for p in range(P)) <= data['availability'][m] + e[m], f"Machine_{m}_time_availability"

#### Solve
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

