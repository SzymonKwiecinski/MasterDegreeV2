# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP

PROBLEM INFO: 
- A company must deliver \var{deliver_i} units of its product at the end of the \var{i}_th month.
- Material produced during a month can be delivered either at the end of the same month or can be stored as inventory and delivered at the end of a subsequent month.
- There is a storage cost of \var{storage_cost} dollars per month for each unit of product held in inventory. 
- The year begins with zero inventory. 
- If the company produces \var{x_i} units in month \var{i} and \var{x_{i+1}} units in month \var{i}+1, it incurs a cost of \var{switch_cost} |\var{x_{i+1}} - \var{x_i}|  dollars, reflecting the cost of switching to a new production level. 
- Assume that inventory left at the end of the year has no value and does not incur any storage cost.
- The company wants to minimize the total cost of the production and inventory schedule over the next \var{T} months.

INPUT FORMAT: 

{
    "deliver": [deliver_i for i in 1, ..., T],
    "storage_cost": storage_cost,
    "switch_cost": switch_cost,
}

OBJECTIVE: Minimize the total cost of the production and inventory schedule over the whole period.

OUTPUT INFO:

- \var{x_i} is the number of units produced in month \var{i}.

OUTPUT FORMAT:

{
    "x": [x_i for i in 1, ..., T],
    "cost": cost,
}

</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
To formulate this problem as a linear programming (LP) model, we need to establish decision variables, constraints, and an objective function.

**Decision Variables:**
- \( x_i \): Number of units produced in month \( i \) for \( i = 1, \ldots, T \).
- \( I_i \): Inventory at the end of month \( i \) for \( i = 1, \ldots, T \).

**Objective Function:**
- Minimize the total cost, which consists of storage costs and switching costs.
- Storage cost is calculated as \( \text{storage\_cost} \sum_{i=1}^{T-1} I_i \).
- Switching cost for production changes is \( \text{switch\_cost} \sum_{i=1}^{T-1} |x_{i+1} - x_i| \).

Given that the switching cost involves an absolute value, we can use auxiliary variables \( y_i \) to linearize this:

\[ |x_{i+1} - x_i| = y_i \quad \text{where} \quad y_i \geq x_{i+1} - x_i \quad \text{and} \quad y_i \geq x_i - x_{i+1} \]

**Constraints:**
1. Inventory and production balance:
   \[
   x_i + I_{i-1} = \text{deliver}_i + I_i \quad \text{for} \quad i = 1, \ldots, T
   \]
   with \( I_0 = 0 \).

2. Non-negativity:
   \[
   x_i \geq 0, \quad I_i \geq 0 \quad \forall i
   \]

Using these components, the linear programming model for the given problem can be represented as follows in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Linear Programming Model:}

\textbf{Objective:}
\[
\text{Minimize } \sum_{i=1}^{T-1} \text{storage\_cost} \cdot I_i + \sum_{i=1}^{T-1} \text{switch\_cost} \cdot y_i
\]

\textbf{Subject to:}
\[
x_i + I_{i-1} = \text{deliver}_i + I_i \quad \forall i = 1, \ldots, T
\]

\[
I_0 = 0
\]

\[
y_i \geq x_{i+1} - x_i \quad \forall i = 1, \ldots, T-1
\]

\[
y_i \geq x_i - x_{i+1} \quad \forall i = 1, \ldots, T-1
\]

\[
x_i \geq 0 \quad \forall i = 1, \ldots, T
\]

\[
I_i \geq 0 \quad \forall i = 1, \ldots, T
\]

\end{document}
```

This LaTeX formulation provides a clear mathematical model for minimizing the total cost of production and inventory scheduling over the specified period, considering both storage and switch costs.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Linear Programming Model:}

\textbf{Objective:}
\[
\text{Minimize } \sum_{i=1}^{T-1} \text{storage\_cost} \cdot I_i + \sum_{i=1}^{T-1} \text{switch\_cost} \cdot y_i
\]

\textbf{Subject to:}
\[
x_i + I_{i-1} = \text{deliver}_i + I_i \quad \forall i = 1, \ldots, T
\]

\[
I_0 = 0
\]

\[
y_i \geq x_{i+1} - x_i \quad \forall i = 1, \ldots, T-1
\]

\[
y_i \geq x_i - x_{i+1} \quad \forall i = 1, \ldots, T-1
\]

\[
x_i \geq 0 \quad \forall i = 1, \ldots, T
\]

\[
I_i \geq 0 \quad \forall i = 1, \ldots, T
\]

\end{document}</MATH_MODEL>
<DATA>
{'T': 12, 'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], 'StorageCost': 5, 'SwitchCost': 10}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data
data = {'T': 12, 'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], 
        'StorageCost': 5, 'SwitchCost': 10}

T = data['T']
deliver = data['Deliver']
storage_cost = data['StorageCost']
switch_cost = data['SwitchCost']

#### Create a linear programming problem
problem = pulp.LpProblem("Minimize_Costs", pulp.LpMinimize)

#### Decision variables
x = pulp.LpVariable.dicts("x", range(T), lowBound=0)
I = pulp.LpVariable.dicts("I", range(T), lowBound=0)
y = pulp.LpVariable.dicts("y", range(T-1), lowBound=0)

#### Objective function
problem += pulp.lpSum(storage_cost * I[i] for i in range(T)) + pulp.lpSum(switch_cost * y[i] for i in range(T-1))

#### Constraints
problem += I[0] == 0  #### Initial Inventory

for i in range(1, T):
    problem += x[i] + I[i-1] == deliver[i] + I[i]  #### Inventory balance
    problem += y[i-1] >= x[i] - x[i-1]  #### Switch cost constraint
    problem += y[i-1] >= x[i-1] - x[i]  #### Switch cost constraint

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

