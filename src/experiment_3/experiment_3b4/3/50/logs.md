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
To formulate this problem as a Linear Programming (LP) model, we will define decision variables, the objective function, and the constraints.

######### Decision Variables:
- Let \( x_p \) be the number of batches of part \( p \) to be produced each month.
- Let \( e_m \) be the additional hours purchased for machine \( m \) each month.

######### Objective Function:
We want to maximize the total profit, which is the total revenue minus the total production costs and extra machine costs.

\[
\text{Maximize: } Z = \sum_{p=1}^{P} \text{price}_p \cdot x_p - \sum_{m=1}^{M} \left( \text{cost}_m \cdot \left( \sum_{p=1}^{P} \text{time}_{m,p} \cdot x_p \right) + \text{extra\_cost}_m \cdot e_m \right)
\]

######### Constraints:
1. **Machine Time Constraints**: For each machine \( m \), the total time used by all parts should not exceed the available hours plus any extra hours purchased.
   \[
   \sum_{p=1}^{P} \text{time}_{m,p} \cdot x_p \leq \text{available}_m + e_m, \quad \forall m = 1, \ldots, M
   \]

2. **Minimum Batch Production Constraints**: Each part \( p \) must be produced at least the minimum required batches.
   \[
   x_p \geq \text{min\_batches}_p, \quad \forall p = 1, \ldots, P
   \]

3. **Extra Hours Purchase Constraints**: The extra hours purchased for each machine must not exceed the maximum allowed.
   \[
   e_m \leq \text{max\_extra}_m, \quad \forall m = 1, \ldots, M
   \]

4. **Non-negativity Constraints**: 
   \[
   x_p \geq 0, \quad \forall p = 1, \ldots, P
   \]
   \[
   e_m \geq 0, \quad \forall m = 1, \ldots, M
   \]

Now, here's the LaTeX code for the mathematical model:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:}

\[
\text{Maximize: } Z = \sum_{p=1}^{P} \text{price}_p \cdot x_p - \sum_{m=1}^{M} \left( \text{cost}_m \cdot \left( \sum_{p=1}^{P} \text{time}_{m,p} \cdot x_p \right) + \text{extra\_cost}_m \cdot e_m \right)
\]

\textbf{Subject to:}

\[
\sum_{p=1}^{P} \text{time}_{m,p} \cdot x_p \leq \text{available}_m + e_m, \quad \forall m = 1, \ldots, M
\]

\[
x_p \geq \text{min\_batches}_p, \quad \forall p = 1, \ldots, P
\]

\[
e_m \leq \text{max\_extra}_m, \quad \forall m = 1, \ldots, M
\]

\[
x_p \geq 0, \quad \forall p = 1, \ldots, P
\]

\[
e_m \geq 0, \quad \forall m = 1, \ldots, M
\]

\end{document}
```

This formulation provides the structure needed to solve the problem using linear programming techniques. It lays out how to determine the optimal number of batches for each part and the optimal additional hours needed, ensuring maximum profit while adhering to constraints.

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

\[
\text{Maximize: } Z = \sum_{p=1}^{P} \text{price}_p \cdot x_p - \sum_{m=1}^{M} \left( \text{cost}_m \cdot \left( \sum_{p=1}^{P} \text{time}_{m,p} \cdot x_p \right) + \text{extra\_cost}_m \cdot e_m \right)
\]

\textbf{Subject to:}

\[
\sum_{p=1}^{P} \text{time}_{m,p} \cdot x_p \leq \text{available}_m + e_m, \quad \forall m = 1, \ldots, M
\]

\[
x_p \geq \text{min\_batches}_p, \quad \forall p = 1, \ldots, P
\]

\[
e_m \leq \text{max\_extra}_m, \quad \forall m = 1, \ldots, M
\]

\[
x_p \geq 0, \quad \forall p = 1, \ldots, P
\]

\[
e_m \geq 0, \quad \forall m = 1, \ldots, M
\]

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10], 'extra_costs': [0, 15, 22.5], 'max_extra': [0, 80, 80]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10],
    'extra_costs': [0, 15, 22.5],
    'max_extra': [0, 80, 80]
}

#### Variables
P = len(data['prices'])
M = len(data['machine_costs'])

#### Initialize the problem
problem = pulp.LpProblem("Production_Scheduling", pulp.LpMaximize)

#### Decision variables
x = [pulp.LpVariable(f'x_{p}', lowBound=data['min_batches'][p]) for p in range(P)]
e = [pulp.LpVariable(f'e_{m}', lowBound=0, upBound=data['max_extra'][m]) for m in range(M)]

#### Objective function
profit = sum(data['prices'][p] * x[p] for p in range(P))
machine_costs = sum(data['machine_costs'][m] * sum(data['time_required'][m][p] * x[p] for p in range(P)) for m in range(M))
extra_costs = sum(data['extra_costs'][m] * e[m] for m in range(M))

problem += profit - machine_costs - extra_costs

#### Constraints
for m in range(M):
    problem += sum(data['time_required'][m][p] * x[p] for p in range(P)) <= data['availability'][m] + e[m]

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

