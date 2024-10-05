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
To create a linear programming model for this problem, let's define the decision variables and set up the objective function and constraints. We'll use LaTeX to write the mathematical model.

Let's define the decision variables:
- \( x_p \) represents the number of batches of part \( p \) to be produced for \( p = 1, \ldots, P \).
- \( e_m \) represents the extra hours acquired for machine \( m \) for \( m = 1, \ldots, M \).

The objective is to maximize the total profit, considering the revenue from selling the parts and the cost associated with using machines, including any extra hours.

Here's the LaTeX representation of the linear programming model:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:} Maximize Total Profit

\begin{align*}
\text{Maximize } & \sum_{p=1}^{P} \text{price}_p \cdot x_p - \sum_{m=1}^{M} \left( \text{cost}_m \cdot \sum_{p=1}^{P} \text{time}_{m,p} \cdot x_p + \text{extra\_cost}_m \cdot e_m \right)
\end{align*}

\textbf{Subject to:}

\begin{align*}
& \sum_{p=1}^{P} \text{time}_{m,p} \cdot x_p \leq \text{available}_m + e_m & \forall m = 1, \ldots, M \\
& x_p \geq \text{min\_batches}_p & \forall p = 1, \ldots, P \\
& e_m \leq \text{max\_extra}_m & \forall m = 1, \ldots, M \\
& x_p \geq 0 & \forall p = 1, \ldots, P \\
& e_m \geq 0 & \forall m = 1, \ldots, M
\end{align*}

\end{document}
```

Explanation:
- The objective function maximizes the total profit by calculating the revenue from selling \( x_p \) batches of each part \( p \) and subtracting the cost of using machines, including any extra hours purchased.
- The first constraint ensures that the total time spent on each machine \( m \) does not exceed the available hours plus any extra hours purchased.
- The second constraint ensures that at least the minimum required batches of each part are produced.
- The third constraint limits the extra hours purchased for each machine.
- Non-negativity constraints for decision variables \( x_p \) (batches produced) and \( e_m \) (extra hours).

This model helps determine the optimal number of batches for each part to maximize the division's profit.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:} Maximize Total Profit

\begin{align*}
\text{Maximize } & \sum_{p=1}^{P} \text{price}_p \cdot x_p - \sum_{m=1}^{M} \left( \text{cost}_m \cdot \sum_{p=1}^{P} \text{time}_{m,p} \cdot x_p + \text{extra\_cost}_m \cdot e_m \right)
\end{align*}

\textbf{Subject to:}

\begin{align*}
& \sum_{p=1}^{P} \text{time}_{m,p} \cdot x_p \leq \text{available}_m + e_m & \forall m = 1, \ldots, M \\
& x_p \geq \text{min\_batches}_p & \forall p = 1, \ldots, P \\
& e_m \leq \text{max\_extra}_m & \forall m = 1, \ldots, M \\
& x_p \geq 0 & \forall p = 1, \ldots, P \\
& e_m \geq 0 & \forall m = 1, \ldots, M
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10], 'extra_costs': [0, 15, 22.5], 'max_extra': [0, 80, 80]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data from the provided JSON format
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10],
    'extra_costs': [0, 15, 22.5],
    'max_extra': [0, 80, 80]
}

#### Constants
P = len(data['prices'])
M = len(data['machine_costs'])

#### Initialize the problem
problem = pulp.LpProblem("Maximize_Total_Profit", pulp.LpMaximize)

#### Define decision variables
x = pulp.LpVariable.dicts("x", range(P), lowBound=0)
e = pulp.LpVariable.dicts("e", range(M), lowBound=0)

#### Objective Function
profit = pulp.lpSum(data['prices'][p] * x[p] for p in range(P)) - \
         pulp.lpSum(data['machine_costs'][m] * pulp.lpSum(data['time_required'][m][p] * x[p] for p in range(P)) + data['extra_costs'][m] * e[m] for m in range(M))

problem += profit, "Total_Profit"

#### Constraints
#### Machine time constraints
for m in range(M):
    problem += pulp.lpSum(data['time_required'][m][p] * x[p] for p in range(P)) <= data['availability'][m] + e[m], f"Time_Constraint_{m}"

#### Minimum batches constraints
for p in range(P):
    problem += x[p] >= data['min_batches'][p], f"Min_Batch_Constraint_{p}"

#### Extra capacity constraints
for m in range(M):
    problem += e[m] <= data['max_extra'][m], f"Max_Extra_Constraint_{m}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

