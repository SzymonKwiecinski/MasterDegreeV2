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
To formulate this problem as a linear programming model, we will define the decision variables, objective function, and constraints based on the given problem description.

**Decision Variables:**
Let \( x_p \) be the number of batches of part \( p \) produced each month.

**Objective Function:**
We want to maximize the total profit. The profit from producing part \( p \) is the revenue from selling it minus the cost of production. The revenue from part \( p \) is \( \text{price}_p \times x_p \), and the cost for using machines is the sum of all machine usages multiplied by their respective costs.

The total profit function can be expressed as:
\[
\text{Profit} = \sum_{p=1}^{P} (\text{price}_p \times x_p) - \sum_{m=1}^{M} \left( \sum_{p=1}^{P} \text{time}_{m,p} \times x_p \times \text{cost}_m \right)
\]

**Constraints:**
1. Each machine has a limited availability of hours per month:
   \[
   \sum_{p=1}^{P} \text{time}_{m,p} \times x_p \leq \text{available}_m \quad \text{for each machine } m
   \]
   
2. There is a minimum production requirement for each part:
   \[
   x_p \geq \text{min\_batches}_p \quad \text{for each part } p
   \]

3. Non-negativity constraints:
   \[
   x_p \geq 0 \quad \text{for each part } p
   \]

Using these components, the linear programming model can be written in LaTeX code:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\subsection*{Decision Variables}
\begin{align*}
x_p & : \text{Number of batches of part } p \text{ produced each month.}
\end{align*}

\subsection*{Objective Function}
Maximize the total profit:
\begin{align*}
\text{Maximize} \quad Z = \sum_{p=1}^{P} \text{price}_p \times x_p - \sum_{m=1}^{M} \left( \sum_{p=1}^{P} \text{time}_{m,p} \times x_p \times \text{cost}_m \right)
\end{align*}

\subsection*{Constraints}
\begin{align*}
& \text{Machine availability:} \\
& \sum_{p=1}^{P} \text{time}_{m,p} \times x_p \leq \text{available}_m, \quad \forall m = 1, \ldots, M \\
\\
& \text{Minimum production requirement:} \\
& x_p \geq \text{min\_batches}_p, \quad \forall p = 1, \ldots, P \\
\\
& \text{Non-negativity:} \\
& x_p \geq 0, \quad \forall p = 1, \ldots, P
\end{align*}

\end{document}
```

This linear programming model will help determine the optimal number of batches of each part to maximize profit while respecting machine availability and contract production requirements.

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
x_p & : \text{Number of batches of part } p \text{ produced each month.}
\end{align*}

\subsection*{Objective Function}
Maximize the total profit:
\begin{align*}
\text{Maximize} \quad Z = \sum_{p=1}^{P} \text{price}_p \times x_p - \sum_{m=1}^{M} \left( \sum_{p=1}^{P} \text{time}_{m,p} \times x_p \times \text{cost}_m \right)
\end{align*}

\subsection*{Constraints}
\begin{align*}
& \text{Machine availability:} \\
& \sum_{p=1}^{P} \text{time}_{m,p} \times x_p \leq \text{available}_m, \quad \forall m = 1, \ldots, M \\
\\
& \text{Minimum production requirement:} \\
& x_p \geq \text{min\_batches}_p, \quad \forall p = 1, \ldots, P \\
\\
& \text{Non-negativity:} \\
& x_p \geq 0, \quad \forall p = 1, \ldots, P
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10]}</DATA>


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
    'min_batches': [10, 10, 10, 10]
}

#### Indices
P = len(data['prices'])
M = len(data['machine_costs'])

#### Problem definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
x = [pulp.LpVariable(f'x_{p}', lowBound=0, cat='Continuous') for p in range(P)]

#### Objective Function
profit = pulp.lpSum([data['prices'][p] * x[p] for p in range(P)])
machine_costs = pulp.lpSum([data['time_required'][m][p] * x[p] * data['machine_costs'][m] for p in range(P) for m in range(M)])
problem += profit - machine_costs

#### Constraints

#### Machine availability constraints
for m in range(M):
    problem += pulp.lpSum([data['time_required'][m][p] * x[p] for p in range(P)]) <= data['availability'][m], f"Machine_availability_{m}"

#### Minimum production requirement constraints
for p in range(P):
    problem += x[p] >= data['min_batches'][p], f"Min_batches_{p}"

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

