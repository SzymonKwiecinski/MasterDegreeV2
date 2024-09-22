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

\textbf{Definitions:}
\begin{itemize}
    \item Let $T$ be the number of months.
    \item Let $\text{deliver}_i$ be the units that must be delivered at the end of month $i$ for $i = 1, 2, \ldots, T$.
    \item Let $x_i$ be the number of units produced in month $i$.
    \item Let $I_i$ be the inventory at the end of month $i$.
    \item Let $C$ be the total cost to minimize.
    \item Let $\text{storage\_cost}$ be the cost of holding one unit in inventory for one month.
    \item Let $\text{switch\_cost}$ be the cost incurred when changing production levels from month $i$ to month $i+1$.
\end{itemize}

\textbf{Objective Function:}
\[
\text{Minimize } C = \sum_{i=1}^{T} \text{storage\_cost} \cdot I_i + \sum_{i=1}^{T-1} \text{switch\_cost} \cdot |x_{i+1} - x_i|
\]

\textbf{Constraints:}
\begin{enumerate}
    \item Inventory balance:
    \[
    I_i = I_{i-1} + x_i - \text{deliver}_i, \quad \text{for } i = 1, \ldots, T
    \]
    with $I_0 = 0$ (no initial inventory).
    
    \item Non-negativity of inventory:
    \[
    I_i \geq 0, \quad \text{for } i = 1, \ldots, T
    \]
    
    \item Non-negativity of production:
    \[
    x_i \geq 0, \quad \text{for } i = 1, \ldots, T
    \]
    
    \item At the end of the year:
    \[
    I_T = 0
    \]
\end{enumerate}

\textbf{Output:}
\begin{itemize}
    \item $x = [x_1, x_2, \ldots, x_T]$: the production schedule.
    \item $\text{cost}$: the minimized total cost $C$.
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

\textbf{Definitions:}
\begin{itemize}
    \item Let $T$ be the number of months.
    \item Let $\text{deliver}_i$ be the units that must be delivered at the end of month $i$ for $i = 1, 2, \ldots, T$.
    \item Let $x_i$ be the number of units produced in month $i$.
    \item Let $I_i$ be the inventory at the end of month $i$.
    \item Let $C$ be the total cost to minimize.
    \item Let $\text{storage\_cost}$ be the cost of holding one unit in inventory for one month.
    \item Let $\text{switch\_cost}$ be the cost incurred when changing production levels from month $i$ to month $i+1$.
\end{itemize}

\textbf{Objective Function:}
\[
\text{Minimize } C = \sum_{i=1}^{T} \text{storage\_cost} \cdot I_i + \sum_{i=1}^{T-1} \text{switch\_cost} \cdot |x_{i+1} - x_i|
\]

\textbf{Constraints:}
\begin{enumerate}
    \item Inventory balance:
    \[
    I_i = I_{i-1} + x_i - \text{deliver}_i, \quad \text{for } i = 1, \ldots, T
    \]
    with $I_0 = 0$ (no initial inventory).
    
    \item Non-negativity of inventory:
    \[
    I_i \geq 0, \quad \text{for } i = 1, \ldots, T
    \]
    
    \item Non-negativity of production:
    \[
    x_i \geq 0, \quad \text{for } i = 1, \ldots, T
    \]
    
    \item At the end of the year:
    \[
    I_T = 0
    \]
\end{enumerate}

\textbf{Output:}
\begin{itemize}
    \item $x = [x_1, x_2, \ldots, x_T]$: the production schedule.
    \item $\text{cost}$: the minimized total cost $C$.
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'T': 12, 'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], 'StorageCost': 5, 'SwitchCost': 10}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Load data
data = json.loads('{"T": 12, "Deliver": [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], "StorageCost": 5, "SwitchCost": 10}')
T = data['T']
deliver = data['Deliver']
storage_cost = data['StorageCost']
switch_cost = data['SwitchCost']

#### Create the Linear Programming problem
problem = pulp.LpProblem("Production_Problem", pulp.LpMinimize)

#### Variables
x = pulp.LpVariable.dicts("x", range(1, T + 1), lowBound=0, cat='Continuous')  #### Production variables
I = pulp.LpVariable.dicts("I", range(1, T + 1), lowBound=0, cat='Continuous')  #### Inventory variables

#### Objective Function
problem += pulp.lpSum(storage_cost * I[i] for i in range(1, T + 1)) + \
           pulp.lpSum(switch_cost * pulp.lpAbs(x[i + 1] - x[i]) for i in range(1, T))

#### Constraints
problem += I[1] == x[1] - deliver[0]  #### Inventory balance for month 1
for i in range(2, T + 1):
    problem += I[i] == I[i - 1] + x[i] - deliver[i - 1]  #### Inventory balance for months 2 to T

#### Non-negativity of inventory
for i in range(1, T + 1):
    problem += I[i] >= 0

#### Non-negativity of production
for i in range(1, T + 1):
    problem += x[i] >= 0

#### End of the year inventory
problem += I[T] == 0

#### Solve the problem
problem.solve()

#### Output
production_schedule = [x[i].varValue for i in range(1, T + 1)]
minimized_cost = pulp.value(problem.objective)

print(f'Production Schedule: {production_schedule}')
print(f' (Objective Value): <OBJ>{minimized_cost}</OBJ>')
```

