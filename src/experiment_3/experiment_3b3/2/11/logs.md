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

\textbf{Indices:}
\begin{itemize}
    \item $i$: month index, where $i = 1, 2, \ldots, T$
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item $deliver_i$: units of product to deliver at the end of month $i$
    \item $storage\_cost$: cost per month for holding one unit in inventory
    \item $switch\_cost$: cost of switching production level between months
\end{itemize}

\textbf{Variables:}
\begin{itemize}
    \item $x_i$: units produced in month $i$
    \item $I_i$: inventory at the end of month $i$
\end{itemize}

\textbf{Objective Function:}
\begin{align*}
\text{Minimize} \quad & \sum_{i=1}^{T} (storage\_cost \cdot I_i + switch\_cost \cdot |x_{i+1} - x_i|) \\
\end{align*}

\textbf{Constraints:}
\begin{align*}
I_1 & = x_1 - deliver_1 \\
I_i & = I_{i-1} + x_i - deliver_i \quad \text{for } i = 2, \ldots, T \\
I_i & \geq 0 \quad \text{for } i = 1, \ldots, T \\
I_T & = 0 \\
\end{align*}

\textbf{Non-negativity:}
\begin{align*}
x_i & \geq 0 \quad \text{for } i = 1, \ldots, T \\
I_i & \geq 0 \quad \text{for } i = 1, \ldots, T \\
\end{align*}

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

\textbf{Indices:}
\begin{itemize}
    \item $i$: month index, where $i = 1, 2, \ldots, T$
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item $deliver_i$: units of product to deliver at the end of month $i$
    \item $storage\_cost$: cost per month for holding one unit in inventory
    \item $switch\_cost$: cost of switching production level between months
\end{itemize}

\textbf{Variables:}
\begin{itemize}
    \item $x_i$: units produced in month $i$
    \item $I_i$: inventory at the end of month $i$
\end{itemize}

\textbf{Objective Function:}
\begin{align*}
\text{Minimize} \quad & \sum_{i=1}^{T} (storage\_cost \cdot I_i + switch\_cost \cdot |x_{i+1} - x_i|) \\
\end{align*}

\textbf{Constraints:}
\begin{align*}
I_1 & = x_1 - deliver_1 \\
I_i & = I_{i-1} + x_i - deliver_i \quad \text{for } i = 2, \ldots, T \\
I_i & \geq 0 \quad \text{for } i = 1, \ldots, T \\
I_T & = 0 \\
\end{align*}

\textbf{Non-negativity:}
\begin{align*}
x_i & \geq 0 \quad \text{for } i = 1, \ldots, T \\
I_i & \geq 0 \quad \text{for } i = 1, \ldots, T \\
\end{align*}

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

#### Problem
problem = pulp.LpProblem("Production_Plan", pulp.LpMinimize)

#### Variables
x = [pulp.LpVariable(f"x_{i}", lowBound=0) for i in range(T)]
I = [pulp.LpVariable(f"I_{i}", lowBound=0) for i in range(T)]

#### Objective Function
problem += pulp.lpSum(storage_cost * I[i] + switch_cost * (pulp.lpSum(x[i+1] - x[i] for i in range(T-1))) for i in range(T))

#### Constraints
problem += (I[0] == x[0] - deliver[0])
for i in range(1, T):
    problem += (I[i] == I[i-1] + x[i] - deliver[i])

problem += (I[T-1] == 0)

#### Solve
problem.solve()

#### Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```


