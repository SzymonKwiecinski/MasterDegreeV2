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
To formulate this problem as a Linear Programming model, we need to define the decision variables, objective function, and constraints based on the problem description. Here is the mathematical model in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\subsection*{Decision Variables}
Let \( x_i \) be the number of units produced in month \( i \) for \( i = 1, 2, \ldots, T \).

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{deliver}_i \): Units to be delivered at the end of month \( i \).
    \item \text{storage\_cost}: Storage cost per unit per month.
    \item \text{switch\_cost}: Cost incurred for changing production levels between consecutive months.
    \item \( T \): Total number of months.
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost, which consists of the storage and switch costs:
\[
\text{Minimize} \quad \sum_{i=1}^{T} \text{storage\_cost} \cdot s_i + \sum_{i=1}^{T-1} \text{switch\_cost} \cdot |x_{i+1} - x_i|
\]

\subsection*{Constraints}
\begin{itemize}
    \item Inventory balance constraints for each month:
    \[
    \begin{aligned}
        & s_1 = x_1 - \text{deliver}_1, \\
        & s_i = s_{i-1} + x_i - \text{deliver}_i \quad \text{for } i = 2, \ldots, T,
    \end{aligned}
    \]
    where \( s_i \) is the inventory at the end of month \( i \).

    \item Non-negativity constraints:
    \[
    \begin{aligned}
        & x_i \geq 0 \quad \text{for all } i, \\
        & s_i \geq 0 \quad \text{for all } i.
    \end{aligned}
    \]

    \item Initial inventory is zero:
    \[
    s_0 = 0
    \]

    \item Ending inventory at the end of year \( T \) (not required but implicitly zero in cost).
\end{itemize}

\subsection*{Special Note}
The term \( |x_{i+1} - x_i| \) requires additional constraints to linearize it for use in a linear programming solver.

\end{document}
```

This model minimizes the cost over the planning horizon, accounting for storage and switching costs while satisfying delivery requirements. The absolute value in the objective function for switching costs often needs a linearization technique when implementing in a solver.

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
Let \( x_i \) be the number of units produced in month \( i \) for \( i = 1, 2, \ldots, T \).

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{deliver}_i \): Units to be delivered at the end of month \( i \).
    \item \text{storage\_cost}: Storage cost per unit per month.
    \item \text{switch\_cost}: Cost incurred for changing production levels between consecutive months.
    \item \( T \): Total number of months.
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost, which consists of the storage and switch costs:
\[
\text{Minimize} \quad \sum_{i=1}^{T} \text{storage\_cost} \cdot s_i + \sum_{i=1}^{T-1} \text{switch\_cost} \cdot |x_{i+1} - x_i|
\]

\subsection*{Constraints}
\begin{itemize}
    \item Inventory balance constraints for each month:
    \[
    \begin{aligned}
        & s_1 = x_1 - \text{deliver}_1, \\
        & s_i = s_{i-1} + x_i - \text{deliver}_i \quad \text{for } i = 2, \ldots, T,
    \end{aligned}
    \]
    where \( s_i \) is the inventory at the end of month \( i \).

    \item Non-negativity constraints:
    \[
    \begin{aligned}
        & x_i \geq 0 \quad \text{for all } i, \\
        & s_i \geq 0 \quad \text{for all } i.
    \end{aligned}
    \]

    \item Initial inventory is zero:
    \[
    s_0 = 0
    \]

    \item Ending inventory at the end of year \( T \) (not required but implicitly zero in cost).
\end{itemize}

\subsection*{Special Note}
The term \( |x_{i+1} - x_i| \) requires additional constraints to linearize it for use in a linear programming solver.

\end{document}</MATH_MODEL>
<DATA>
{'T': 12, 'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], 'StorageCost': 5, 'SwitchCost': 10}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the JSON format
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

#### Create the Linear Programming Problem
problem = pulp.LpProblem("Production_Planning", pulp.LpMinimize)

#### Decision Variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Continuous') for i in range(1, T + 1)]
s = [pulp.LpVariable(f's_{i}', lowBound=0, cat='Continuous') for i in range(1, T + 1)]
switch = [pulp.LpVariable(f'switch_{i}', lowBound=0, cat='Continuous') for i in range(1, T)]

#### Objective Function
problem += pulp.lpSum(storage_cost * s[i] for i in range(T)) + pulp.lpSum(switch_cost * switch[i] for i in range(T - 1))

#### Constraints
#### Inventory balance constraints
problem += s[0] == x[0] - deliver[0]  #### for the first month
for i in range(1, T):
    problem += s[i] == s[i - 1] + x[i] - deliver[i]

#### Linearizing absolute value of production change for switch costs
for i in range(T - 1):
    problem += x[i + 1] - x[i] <= switch[i]
    problem += x[i] - x[i + 1] <= switch[i]

#### Initial inventory is zero
problem += s[0] == x[0] - deliver[0]

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

