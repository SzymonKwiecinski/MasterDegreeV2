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
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\textbf{Decision Variables:} \\
Let \( x_i \) be the number of units produced in month \( i \) for \( i = 1, 2, \ldots, T \). \\
Let \( I_i \) be the inventory at the end of month \( i \) for \( i = 1, 2, \ldots, T \).

\textbf{Objective Function:} \\
Minimize the total cost, given by:
\[
\text{Cost} = \sum_{i=1}^{T} \text{storage\_cost} \cdot I_i + \sum_{i=1}^{T-1} \text{switch\_cost} \cdot |x_{i+1} - x_i| 
\]

\textbf{Constraints:} \\

1. Inventory Balance:
\[
I_i = I_{i-1} + x_i - \text{deliver}_i \quad \text{for } i = 1, 2, \ldots, T
\]
with initial condition:
\[
I_0 = 0
\]

2. Non-negativity of Production and Inventory:
\[
x_i \geq 0 \quad \text{for } i = 1, 2, \ldots, T
\]
\[
I_i \geq 0 \quad \text{for } i = 1, 2, \ldots, T
\]

3. The inventory at the end of the year has no value:
\[
I_T = 0
\]

\textbf{Final Output:}
The output will provide the production schedule \( x_i \) for each month and the total cost incurred:

\begin{itemize}
    \item \( x = [x_1, x_2, \ldots, x_T] \)
    \item cost = Total Cost
\end{itemize}

\end{document}
```

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

\textbf{Decision Variables:} \\
Let \( x_i \) be the number of units produced in month \( i \) for \( i = 1, 2, \ldots, T \). \\
Let \( I_i \) be the inventory at the end of month \( i \) for \( i = 1, 2, \ldots, T \).

\textbf{Objective Function:} \\
Minimize the total cost, given by:
\[
\text{Cost} = \sum_{i=1}^{T} \text{storage\_cost} \cdot I_i + \sum_{i=1}^{T-1} \text{switch\_cost} \cdot |x_{i+1} - x_i| 
\]

\textbf{Constraints:} \\

1. Inventory Balance:
\[
I_i = I_{i-1} + x_i - \text{deliver}_i \quad \text{for } i = 1, 2, \ldots, T
\]
with initial condition:
\[
I_0 = 0
\]

2. Non-negativity of Production and Inventory:
\[
x_i \geq 0 \quad \text{for } i = 1, 2, \ldots, T
\]
\[
I_i \geq 0 \quad \text{for } i = 1, 2, \ldots, T
\]

3. The inventory at the end of the year has no value:
\[
I_T = 0
\]

\textbf{Final Output:}
The output will provide the production schedule \( x_i \) for each month and the total cost incurred:

\begin{itemize}
    \item \( x = [x_1, x_2, \ldots, x_T] \)
    \item cost = Total Cost
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'T': 12, 'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], 'StorageCost': 5, 'SwitchCost': 10}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data input in JSON format
data = json.loads("{'T': 12, 'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], 'StorageCost': 5, 'SwitchCost': 10}")

#### Extracting parameters
T = data['T']
deliveries = data['Deliver']
storage_cost = data['StorageCost']
switch_cost = data['SwitchCost']

#### Create the LP problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

#### Decision Variables
x = pulp.LpVariable.dicts("Production", range(1, T + 1), lowBound=0, cat='Continuous')  #### Production variables
I = pulp.LpVariable.dicts("Inventory", range(1, T + 1), lowBound=0, cat='Continuous')  #### Inventory variables

#### Objective Function
problem += pulp.lpSum(storage_cost * I[i] for i in range(1, T + 1)) + \
           pulp.lpSum(switch_cost * pulp.lpAbs(x[i + 1] - x[i]) for i in range(1, T)), "Total_Cost"

#### Constraints

#### Inventory Balance and initial condition
problem += I[1] == x[1] - deliveries[0], "Inventory_Balance_1"
for i in range(2, T + 1):
    problem += I[i] == I[i - 1] + x[i] - deliveries[i - 1], f"Inventory_Balance_{i}"

#### Ensure the inventory at the end of the year has no value
problem += I[T] == 0, "No_Inventory_End_Year"

#### Solve the problem
problem.solve()

#### Output the production schedule and total cost
productions = [x[i].varValue for i in range(1, T + 1)]
total_cost = pulp.value(problem.objective)

print(f'Productions: {productions}')
print(f'Total Cost: {total_cost}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

