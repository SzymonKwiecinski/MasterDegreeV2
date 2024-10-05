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
To formulate this problem as a linear program, we will define variables, constraints, and the objective function. The decision variables will be the production levels for each month, the inventory levels for each month, and the production switch variables. Below is the mathematical model in LaTeX format.

```latex
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\section*{Linear Programming Model}

\subsection*{Problem Parameters}

\begin{itemize}
    \item $T$: Total number of months.
    \item $d_i$: Number of units to deliver at the end of the $i$-th month, for $i = 1, \ldots, T$.
    \item $c_s$: Storage cost per unit per month.
    \item $c_{\text{switch}}$: Cost per unit change in production level.
\end{itemize}

\subsection*{Decision Variables}

\begin{itemize}
    \item $x_i$: Number of units produced in month $i$, for $i = 1, \ldots, T$.
    \item $I_i$: Inventory level at the end of month $i$, for $i = 1, \ldots, T$.
    \item $z_i$: Absolute change in production between month $i$ and month $i+1$, $z_i = |x_{i+1} - x_i|$, for $i = 1, \ldots, T-1$.
\end{itemize}

\subsection*{Objective Function}

Minimize the total cost:
\[
\min \sum_{i=1}^{T} c_s \cdot I_i + \sum_{i=1}^{T-1} c_{\text{switch}} \cdot z_i
\]

\subsection*{Constraints}

\begin{align}
    & \text{(Inventory Balance)} \notag \\
    & I_0 = 0 \\
    & x_i + I_{i-1} = d_i + I_i \quad \forall i = 1, \ldots, T \\    
    & \text{(Production Switch Adjustment)} \notag \\
    & z_i \geq x_{i+1} - x_i \quad \forall i = 1, \ldots, T-1 \\
    & z_i \geq x_i - x_{i+1} \quad \forall i = 1, \ldots, T-1 \\
    & \text{(Non-negativity)} \notag \\
    & x_i \geq 0, \ I_i \geq 0, \ z_i \geq 0 \quad \forall i
\end{align}

This linear program will yield the optimal production levels $x_i$ for each month $i$, such that the total cost of production, inventory holding, and production level switching is minimized.

\end{document}
```

This LaTeX code provides a clear and structured linear programming model for the given problem, outlining the objective, constraints, and decision variables needed to solve the problem efficiently.

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

\subsection*{Problem Parameters}

\begin{itemize}
    \item $T$: Total number of months.
    \item $d_i$: Number of units to deliver at the end of the $i$-th month, for $i = 1, \ldots, T$.
    \item $c_s$: Storage cost per unit per month.
    \item $c_{\text{switch}}$: Cost per unit change in production level.
\end{itemize}

\subsection*{Decision Variables}

\begin{itemize}
    \item $x_i$: Number of units produced in month $i$, for $i = 1, \ldots, T$.
    \item $I_i$: Inventory level at the end of month $i$, for $i = 1, \ldots, T$.
    \item $z_i$: Absolute change in production between month $i$ and month $i+1$, $z_i = |x_{i+1} - x_i|$, for $i = 1, \ldots, T-1$.
\end{itemize}

\subsection*{Objective Function}

Minimize the total cost:
\[
\min \sum_{i=1}^{T} c_s \cdot I_i + \sum_{i=1}^{T-1} c_{\text{switch}} \cdot z_i
\]

\subsection*{Constraints}

\begin{align}
    & \text{(Inventory Balance)} \notag \\
    & I_0 = 0 \\
    & x_i + I_{i-1} = d_i + I_i \quad \forall i = 1, \ldots, T \\    
    & \text{(Production Switch Adjustment)} \notag \\
    & z_i \geq x_{i+1} - x_i \quad \forall i = 1, \ldots, T-1 \\
    & z_i \geq x_i - x_{i+1} \quad \forall i = 1, \ldots, T-1 \\
    & \text{(Non-negativity)} \notag \\
    & x_i \geq 0, \ I_i \geq 0, \ z_i \geq 0 \quad \forall i
\end{align}

This linear program will yield the optimal production levels $x_i$ for each month $i$, such that the total cost of production, inventory holding, and production level switching is minimized.

\end{document}</MATH_MODEL>
<DATA>
{'T': 12, 'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], 'StorageCost': 5, 'SwitchCost': 10}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON
data = {
    'T': 12,
    'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100],
    'StorageCost': 5,
    'SwitchCost': 10
}

T = data['T']
d = data['Deliver']
c_s = data['StorageCost']
c_switch = data['SwitchCost']

#### Create the problem
problem = pulp.LpProblem("Production_Inventory_Problem", pulp.LpMinimize)

#### Decision Variables
x = pulp.LpVariable.dicts("Production", range(1, T + 1), lowBound=0)  #### Production per month
I = pulp.LpVariable.dicts("Inventory", range(1, T + 1), lowBound=0)  #### Inventory at the end of month
z = pulp.LpVariable.dicts("Switch", range(1, T), lowBound=0)  #### Change in production level

#### Objective Function
problem += pulp.lpSum(c_s * I[i] for i in range(1, T + 1)) + pulp.lpSum(c_switch * z[i] for i in range(1, T)), "Total_Cost"

#### Constraints

#### Inventory Balance
problem += (I[1] == x[1] + 0 - d[0]), "Inventory_Balance_1"  #### I_0 = 0
for i in range(2, T + 1):
    problem += (I[i] == x[i] + I[i - 1] - d[i - 1]), f"Inventory_Balance_{i}"

#### Production Switch Adjustment
for i in range(1, T):
    problem += (z[i] >= x[i + 1] - x[i]), f"Switch_Upper_{i}"
    problem += (z[i] >= x[i] - x[i + 1]), f"Switch_Lower_{i}"

#### Solve the problem
problem.solve()

#### Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
for i in range(1, T + 1):
    print(f'Production in month {i}: {x[i].varValue}, Inventory at end of month {i}: {I[i].varValue}')
```

