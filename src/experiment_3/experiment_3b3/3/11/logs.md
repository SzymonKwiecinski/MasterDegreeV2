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

\title{Linear Programming Model for Production and Inventory Scheduling}
\author{}
\date{}
\maketitle

\section*{Problem Formulation}

Consider the following variables and parameters:

\begin{itemize}
    \item Let \( x_i \) be the number of units produced in month \( i \) for \( i = 1, 2, \ldots, T \).
    \item Let \( I_i \) be the inventory at the end of month \( i \), where \( I_0 = 0 \).
    \item Let \( \text{deliver}_i \) be the units required to be delivered at the end of month \( i \).
    \item Let \( \text{storage\_cost} \) be the cost of storing one unit for one month.
    \item Let \( \text{switch\_cost} \) be the cost incurred for switching production levels between two consecutive months.
\end{itemize}

The total cost to minimize can be defined as:
\[
\text{Total Cost} = \sum_{i=1}^{T} \left( \text{storage\_cost} \cdot I_i + \text{switch\_cost} \cdot |x_{i+1} - x_i| \right)
\]

\section*{Constraints}

The following constraints must be satisfied:

\begin{itemize}
    \item Inventory balance for each month:
    \[
    I_i = I_{i-1} + x_i - \text{deliver}_i \quad \text{for } i = 1, 2, \ldots, T
    \]
    \item Non-negativity constraints on production and inventory:
    \[
    x_i \geq 0 \quad \text{and} \quad I_i \geq 0 \quad \text{for } i = 1, 2, \ldots, T
    \]
    \item The inventory must not incur costs at the end of the year:
    \[
    I_T = 0
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

\title{Linear Programming Model for Production and Inventory Scheduling}
\author{}
\date{}
\maketitle

\section*{Problem Formulation}

Consider the following variables and parameters:

\begin{itemize}
    \item Let \( x_i \) be the number of units produced in month \( i \) for \( i = 1, 2, \ldots, T \).
    \item Let \( I_i \) be the inventory at the end of month \( i \), where \( I_0 = 0 \).
    \item Let \( \text{deliver}_i \) be the units required to be delivered at the end of month \( i \).
    \item Let \( \text{storage\_cost} \) be the cost of storing one unit for one month.
    \item Let \( \text{switch\_cost} \) be the cost incurred for switching production levels between two consecutive months.
\end{itemize}

The total cost to minimize can be defined as:
\[
\text{Total Cost} = \sum_{i=1}^{T} \left( \text{storage\_cost} \cdot I_i + \text{switch\_cost} \cdot |x_{i+1} - x_i| \right)
\]

\section*{Constraints}

The following constraints must be satisfied:

\begin{itemize}
    \item Inventory balance for each month:
    \[
    I_i = I_{i-1} + x_i - \text{deliver}_i \quad \text{for } i = 1, 2, \ldots, T
    \]
    \item Non-negativity constraints on production and inventory:
    \[
    x_i \geq 0 \quad \text{and} \quad I_i \geq 0 \quad \text{for } i = 1, 2, \ldots, T
    \]
    \item The inventory must not incur costs at the end of the year:
    \[
    I_T = 0
    \end{itemize}
\end{document}</MATH_MODEL>
<DATA>
{'T': 12, 'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], 'StorageCost': 5, 'SwitchCost': 10}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {
    'T': 12,
    'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100],
    'StorageCost': 5,
    'SwitchCost': 10
}

T = data['T']
deliver = data['Deliver']
storage_cost = data['StorageCost']
switch_cost = data['SwitchCost']

#### Create an LP problem
problem = pulp.LpProblem("Production_Inventory_Scheduling", pulp.LpMinimize)

#### Decision Variables
x = [pulp.LpVariable(f'x{i}', lowBound=0, cat='Continuous') for i in range(1, T+1)]
I = [pulp.LpVariable(f'I{i}', lowBound=0, cat='Continuous') for i in range(1, T+1)]

#### Objective Function
problem += pulp.lpSum(storage_cost * I[i] + switch_cost * (pulp.lpSum([pulp.lpDot([1, -1], [x[i+1], x[i]])]) if i < T - 1 else 0) for i in range(T))

#### Constraints
#### Inventory balance for each month
for i in range(T):
    if i == 0:
        problem += x[i] - deliver[i] == I[i]
    else:
        problem += I[i-1] + x[i] - deliver[i] == I[i]

#### Inventory must be zero at the end of the year
problem += I[T-1] == 0

#### Solve the problem
problem.solve()

#### Output the value of the objective function
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

