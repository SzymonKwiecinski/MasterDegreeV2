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
To formulate the problem as a linear programming model, we can define variables and constraints based on the given problem description.

Let's define:
- \( x_i \) as the number of units produced in month \( i \).
- \( I_i \) as the number of units in inventory at the end of month \( i \).

The objective is to minimize the total cost, which includes storage costs and switching costs. The storage cost per month for each unit stored is given by \( \text{storage\_cost} \), and the switching cost incurred when changing production levels is given by \( \text{switch\_cost} \).

The problem can be formulated as follows:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective Function:}

\[
\text{Minimize } \sum_{i=1}^{T} \text{storage\_cost} \times I_i + \sum_{i=1}^{T-1} \text{switch\_cost} \times |x_{i+1} - x_i|
\]

\textbf{Subject to:}

\[
I_0 = 0
\]

\[
I_1 = x_1 - \text{deliver}_1
\]

For \( i = 2, \ldots, T \):
\[
I_i = I_{i-1} + x_i - \text{deliver}_i
\]

\[
I_i \geq 0 \quad \text{for all } i
\]

The decision variables are:
- \( x_i \geq 0 \) for all \( i = 1, \ldots, T \).
- \( I_i \geq 0 \) for all \( i = 1, \ldots, T \).

In this model, the cost term for switching involves absolute values. In a standard linear programming formulation, we need to handle these absolute values by introducing additional variables and constraints, such as using the technique of piecewise linearization or other methods suitable for the LP solvers in use.

\end{document}
```

This model defines the objective and constraints necessary to solve the linear programming problem. Remember that handling absolute values in LP formulations typically requires auxiliary variables and additional constraints. Depending on the solver, different methodologies can be employed for handling absolute values in linear constraints.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective Function:}

\[
\text{Minimize } \sum_{i=1}^{T} \text{storage\_cost} \times I_i + \sum_{i=1}^{T-1} \text{switch\_cost} \times |x_{i+1} - x_i|
\]

\textbf{Subject to:}

\[
I_0 = 0
\]

\[
I_1 = x_1 - \text{deliver}_1
\]

For \( i = 2, \ldots, T \):
\[
I_i = I_{i-1} + x_i - \text{deliver}_i
\]

\[
I_i \geq 0 \quad \text{for all } i
\]

The decision variables are:
- \( x_i \geq 0 \) for all \( i = 1, \ldots, T \).
- \( I_i \geq 0 \) for all \( i = 1, \ldots, T \).

In this model, the cost term for switching involves absolute values. In a standard linear programming formulation, we need to handle these absolute values by introducing additional variables and constraints, such as using the technique of piecewise linearization or other methods suitable for the LP solvers in use.

\end{document}</MATH_MODEL>
<DATA>
{'T': 12, 'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], 'StorageCost': 5, 'SwitchCost': 10}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Given data
data = json.loads('{"T": 12, "Deliver": [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], "StorageCost": 5, "SwitchCost": 10}')
T = data['T']
deliveries = data['Deliver']
storage_cost = data['StorageCost']
switch_cost = data['SwitchCost']

#### Create the problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

#### Decision variables
x = pulp.LpVariable.dicts("x", range(1, T + 1), lowBound=0)
I = pulp.LpVariable.dicts("I", range(1, T + 1), lowBound=0)
switch_vars = pulp.LpVariable.dicts("switch", range(1, T), lowBound=0)

#### Objective function
problem += pulp.lpSum(storage_cost * I[i] for i in range(1, T + 1)) + \
           pulp.lpSum(switch_cost * switch_vars[i] for i in range(1, T)), "Total_Cost"

#### Constraints
problem += I[1] == x[1] - deliveries[0], "Initial_Inventory_1"
for i in range(2, T + 1):
    problem += I[i] == I[i - 1] + x[i] - deliveries[i - 1], f"Inventory_Balance_{i}"

for i in range(1, T):
    problem += switch_vars[i] >= x[i + 1] - x[i], f"Switch_Positive_{i}"
    problem += switch_vars[i] >= -(x[i + 1] - x[i]), f"Switch_Negative_{i}"

for i in range(1, T + 1):
    problem += I[i] >= 0, f"Non_Negative_Inventory_{i}"

#### Solve the problem
problem.solve()

#### Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

