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
To model this problem using Linear Programming, we will define decision variables, an objective function, and a set of constraints.

Let:
- \( x_p \) be the number of batches of part \( p \) produced, for \( p = 1, 2, \ldots, P \).
- \( e_m \) be the extra hours purchased for machine \( m \), for \( m = 1, 2, \ldots, M \).

**Objective Function:**

We aim to maximize the profit, which is the total revenue from selling the parts minus the costs of using the machines and the extra time purchased. Therefore, the objective function is:

\[
\text{Maximize: } \sum_{p=1}^P \text{price}_p \cdot x_p - \sum_{m=1}^M \left( \text{cost}_m \cdot \sum_{p=1}^P \text{time}_{m,p} \cdot x_p + \text{extra\_cost}_m \cdot e_m \right)
\]

**Constraints:**

1. **Machine Availability Constraints:**

   The total time used on each machine, including any extra time purchased, must not exceed the available time plus the extra time purchased:
   
   \[
   \sum_{p=1}^P \text{time}_{m,p} \cdot x_p \leq \text{available}_m + e_m, \quad \forall m = 1, 2, \ldots, M
   \]

2. **Minimum Production Constraints:**

   Each part must satisfy its minimum batch production requirement:
   
   \[
   x_p \geq \text{min\_batches}_p, \quad \forall p = 1, 2, \ldots, P
   \]

3. **Extra Time Constraints:**

   The extra time purchased for each machine must not exceed the maximum extra time allowed:
   
   \[
   0 \leq e_m \leq \text{max\_extra}_m, \quad \forall m = 1, 2, \ldots, M
   \]

**Decision Variables:**

- \( x_p \geq 0 \) (integer)
- \( e_m \geq 0 \)

Now, let's represent this mathematical model in LaTeX code:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:}

Maximize:
\[
\sum_{p=1}^P \text{price}_p \cdot x_p - \sum_{m=1}^M \left( \text{cost}_m \cdot \sum_{p=1}^P \text{time}_{m,p} \cdot x_p + \text{extra\_cost}_m \cdot e_m \right)
\]

\textbf{Subject to:}

\begin{align*}
& \sum_{p=1}^P \text{time}_{m,p} \cdot x_p \leq \text{available}_m + e_m, && \forall m = 1, \ldots, M \\
& x_p \geq \text{min\_batches}_p, && \forall p = 1, \ldots, P \\
& 0 \leq e_m \leq \text{max\_extra}_m, && \forall m = 1, \ldots, M \\
& x_p \geq 0, \quad \text{integer}, && \forall p = 1, \ldots, P \\
& e_m \geq 0, && \forall m = 1, \ldots, M
\end{align*}

\end{document}
```

This LaTeX code describes the entire linear programming model for the problem.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:}

Maximize:
\[
\sum_{p=1}^P \text{price}_p \cdot x_p - \sum_{m=1}^M \left( \text{cost}_m \cdot \sum_{p=1}^P \text{time}_{m,p} \cdot x_p + \text{extra\_cost}_m \cdot e_m \right)
\]

\textbf{Subject to:}

\begin{align*}
& \sum_{p=1}^P \text{time}_{m,p} \cdot x_p \leq \text{available}_m + e_m, && \forall m = 1, \ldots, M \\
& x_p \geq \text{min\_batches}_p, && \forall p = 1, \ldots, P \\
& 0 \leq e_m \leq \text{max\_extra}_m, && \forall m = 1, \ldots, M \\
& x_p \geq 0, \quad \text{integer}, && \forall p = 1, \ldots, P \\
& e_m \geq 0, && \forall m = 1, \ldots, M
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

#### Problem
problem = pulp.LpProblem("Batch_Maximization", pulp.LpMaximize)

#### Variables
x = [pulp.LpVariable(f'x_{p}', lowBound=min_batches[p], cat='Integer') for p in range(P)]
e = [pulp.LpVariable(f'e_{m}', lowBound=0, upBound=max_extra[m], cat='Continuous') for m in range(M)]

#### Objective Function
revenue = pulp.lpSum(prices[p] * x[p] for p in range(P))
cost = pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * x[p] for p in range(P)) + extra_costs[m] * e[m] for m in range(M))
problem += revenue - cost

#### Constraints
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * x[p] for p in range(P)) <= availability[m] + e[m]

#### Solve
problem.solve()

#### Output
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

