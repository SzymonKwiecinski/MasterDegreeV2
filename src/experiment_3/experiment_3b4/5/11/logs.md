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
To model this problem as a Linear Programming (LP) formulation, we need to consider decision variables, an objective function, and constraints that represent the problem accurately.

######### Decision Variables
- \( x_i \): Number of units produced in month \( i \).
- \( I_i \): Inventory at the end of month \( i \).

######### Parameters
- \( \text{deliver}_i \): Number of units required to be delivered at the end of month \( i \).
- \( \text{storage\_cost} \): Storage cost per unit per month.
- \( \text{switch\_cost} \): Cost incurred for changing production levels between consecutive months.
- \( T \): Total number of months.

######### Objective Function
Minimize the total cost, which includes storage costs and switching costs:
\[
\text{Minimize } \sum_{i=1}^{T} (\text{storage\_cost} \cdot I_i) + \sum_{i=1}^{T-1} (\text{switch\_cost} \cdot |x_{i+1} - x_i|)
\]

######### Constraints
1. Inventory Balance: 
   \[
   I_{i-1} + x_i = \text{deliver}_i + I_i \quad \forall i = 1, \ldots, T
   \]
   With \( I_0 = 0 \) because the year begins with zero inventory.

2. Non-Negative Variables:
   \[
   x_i \geq 0, \quad I_i \geq 0 \quad \forall i = 1, \ldots, T
   \]

To linearize the absolute value term in the objective function, we introduce auxiliary variables \( y_i \geq 0 \) and split constraints:
\[
y_i \geq x_{i+1} - x_i
\]
\[
y_i \geq x_i - x_{i+1}
\]
which correspond to \(|x_{i+1} - x_i|\).

######### Linear Programming Model in LaTeX

Below is the complete LP formulation in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\textbf{Objective:}
\[
\text{Minimize } \sum_{i=1}^{T} (\text{storage\_cost} \cdot I_i) + \sum_{i=1}^{T-1} (\text{switch\_cost} \cdot y_i)
\]

\textbf{Subject to:}
\[
I_{i-1} + x_i = \text{deliver}_i + I_i \quad \forall i = 1, \ldots, T
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
x_i \geq 0, \quad I_i \geq 0, \quad y_i \geq 0 \quad \forall i = 1, \ldots, T
\]

\end{document}
```

This formulation ensures that the company's total costs from production and inventory scheduling are minimized while satisfying delivery requirements each month.

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
\text{Minimize } \sum_{i=1}^{T} (\text{storage\_cost} \cdot I_i) + \sum_{i=1}^{T-1} (\text{switch\_cost} \cdot y_i)
\]

\textbf{Subject to:}
\[
I_{i-1} + x_i = \text{deliver}_i + I_i \quad \forall i = 1, \ldots, T
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
x_i \geq 0, \quad I_i \geq 0, \quad y_i \geq 0 \quad \forall i = 1, \ldots, T
\]

\end{document}</MATH_MODEL>
<DATA>
{'T': 12, 'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], 'StorageCost': 5, 'SwitchCost': 10}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data provided
data = {'T': 12, 'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], 'StorageCost': 5, 'SwitchCost': 10}

#### Variables from the data
T = data['T']
deliver = data['Deliver']
storage_cost = data['StorageCost']
switch_cost = data['SwitchCost']

#### Problem definition
problem = pulp.LpProblem("Minimize_Storage_and_Switch_Cost", pulp.LpMinimize)

#### Decision Variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Continuous') for i in range(T)]
I = [pulp.LpVariable(f'I_{i}', lowBound=0, cat='Continuous') for i in range(T)]
y = [pulp.LpVariable(f'y_{i}', lowBound=0, cat='Continuous') for i in range(T-1)]

#### Objective Function
problem += pulp.lpSum([storage_cost * I[i] for i in range(T)]) + \
           pulp.lpSum([switch_cost * y[i] for i in range(T-1)])

#### Constraints
problem += I[0] == 0, "Initial Inventory"

for i in range(T):
    problem += x[i] + (I[i-1] if i > 0 else 0) == deliver[i] + I[i], f"Inventory_Balance_{i}"

for i in range(T-1):
    problem += y[i] >= x[i+1] - x[i], f"Switch_Constraint_Positive_{i}"
    problem += y[i] >= x[i] - x[i+1], f"Switch_Constraint_Negative_{i}"

#### Solving the problem
problem.solve()

#### Output the objective value
print(f" (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")
```

