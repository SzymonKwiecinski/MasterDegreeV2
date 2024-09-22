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

\section*{Linear Programming Model for Production and Inventory Schedule}

\textbf{Indices:}
\begin{itemize}
    \item $i$: month index, where $i = 1, 2, \ldots, T$.
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item $deliver_i$: units to be delivered at the end of month $i$.
    \item $storage\_cost$: cost per unit per month for storage.
    \item $switch\_cost$: cost incurred for changing production levels between months.
\end{itemize}

\textbf{Variables:}
\begin{itemize}
    \item $x_i$: units produced in month $i$.
    \item $I_i$: inventory at the end of month $i$.
\end{itemize}

\textbf{Objective Function:}
\begin{align*}
\text{Minimize} \quad & \sum_{i=1}^{T} (storage\_cost \cdot I_i + switch\_cost \cdot |x_{i+1} - x_i|) \\
& \text{with } x_{T+1} = 0 \text{ (no production after month T)}
\end{align*}

\textbf{Subject to:}
\begin{align*}
I_1 &= x_1 - deliver_1 \\
I_i &= I_{i-1} + x_i - deliver_i \quad \text{for } i = 2, 3, \ldots, T \\
I_i &\geq 0 \quad \text{for } i = 1, 2, \ldots, T \\
x_i &\geq 0 \quad \text{for } i = 1, 2, \ldots, T
\end{align*}

\textbf{Note:} 
At the end of the year, the inventory $I_T$ does not incur storage costs and can be set to 0 for the last month's calculation.

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

\section*{Linear Programming Model for Production and Inventory Schedule}

\textbf{Indices:}
\begin{itemize}
    \item $i$: month index, where $i = 1, 2, \ldots, T$.
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item $deliver_i$: units to be delivered at the end of month $i$.
    \item $storage\_cost$: cost per unit per month for storage.
    \item $switch\_cost$: cost incurred for changing production levels between months.
\end{itemize}

\textbf{Variables:}
\begin{itemize}
    \item $x_i$: units produced in month $i$.
    \item $I_i$: inventory at the end of month $i$.
\end{itemize}

\textbf{Objective Function:}
\begin{align*}
\text{Minimize} \quad & \sum_{i=1}^{T} (storage\_cost \cdot I_i + switch\_cost \cdot |x_{i+1} - x_i|) \\
& \text{with } x_{T+1} = 0 \text{ (no production after month T)}
\end{align*}

\textbf{Subject to:}
\begin{align*}
I_1 &= x_1 - deliver_1 \\
I_i &= I_{i-1} + x_i - deliver_i \quad \text{for } i = 2, 3, \ldots, T \\
I_i &\geq 0 \quad \text{for } i = 1, 2, \ldots, T \\
x_i &\geq 0 \quad \text{for } i = 1, 2, \ldots, T
\end{align*}

\textbf{Note:} 
At the end of the year, the inventory $I_T$ does not incur storage costs and can be set to 0 for the last month's calculation.

\end{document}</MATH_MODEL>
<DATA>
{'T': 12, 'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], 'StorageCost': 5, 'SwitchCost': 10}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the provided JSON
data = {
    'T': 12,
    'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100],
    'StorageCost': 5,
    'SwitchCost': 10
}

#### Define the problem
problem = pulp.LpProblem("Production_Inventory_Schedule", pulp.LpMinimize)

#### Define decision variables
x = pulp.LpVariable.dicts("x", range(1, data['T'] + 1), lowBound=0)  #### units produced
I = pulp.LpVariable.dicts("I", range(1, data['T'] + 1), lowBound=0)  #### inventory

#### Objective function
problem += pulp.lpSum(data['StorageCost'] * I[i] for i in range(1, data['T'] + 1)) + \
           pulp.lpSum(data['SwitchCost'] * pulp.lpAbs(x[i + 1] - x[i]) for i in range(1, data['T']))  #### for switching costs

#### Constraints
#### Inventory at the end of the first month
problem += I[1] == x[1] - data['Deliver'][0]

#### Inventory for subsequent months
for i in range(2, data['T'] + 1):
    problem += I[i] == I[i - 1] + x[i] - data['Deliver'][i - 1]

#### Inventory should be non-negative
for i in range(1, data['T'] + 1):
    problem += I[i] >= 0

#### Production should be non-negative
for i in range(1, data['T'] + 1):
    problem += x[i] >= 0
    
#### Last month production constraint
problem += x[data['T'] + 1] == 0  #### No production after month T

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

