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
The problem is to determine the optimal production schedule to minimize the total cost, which includes both the inventory storage costs and the switching costs between different production levels. Let's create a mathematical model for this problem using linear programming.

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\subsection*{Parameters}
\begin{itemize}
    \item $T$: Number of months.
    \item $d_i$: Demand in units at the end of month $i$, for $i = 1, 2, \ldots, T$.
    \item $c_s$: Storage cost per unit per month.
    \item $c_{sw}$: Switching cost per unit change in production level.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $x_i$: Number of units produced in month $i$, for $i = 1, 2, \ldots, T$.
    \item $I_i$: Inventory at the end of month $i$, for $i = 1, 2, \ldots, T$.
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost, which is the sum of storage costs and switching costs:
\[
\text{Minimize } Z = c_s \sum_{i=1}^{T} I_i + c_{sw} \sum_{i=1}^{T-1} |x_{i+1} - x_i|
\]

\subsection*{Constraints}
\begin{align}
    & I_0 = 0 \quad \text{(Starting inventory)} \\
    & x_i + I_{i-1} = d_i + I_i, \quad i = 1, 2, \ldots, T \quad \text{(Flow balance constraint)} \\
    & I_i \geq 0, \quad i = 1, 2, \ldots, T \quad \text{(Non-negativity of inventory)} \\
    & x_i \geq 0, \quad i = 1, 2, \ldots, T \quad \text{(Non-negativity of production)}
\end{align}

Note: The absolute value constraint can be linearized using the following method:
Introduce auxiliary variables $y_i^{+}$ and $y_i^{-}$ for $i=1,2,\ldots,T-1$. Then add the constraints:
\begin{align}
    & x_{i+1} - x_i = y_i^{+} - y_i^{-}, \quad i = 1, 2, \ldots, T-1 \\
    & y_i^{+}, y_i^{-} \geq 0, \quad i = 1, 2, \ldots, T-1
\end{align}

Replace the switching cost term in the objective function by:
\[
c_{sw} \sum_{i=1}^{T-1} (y_i^{+} + y_i^{-})
\]

\end{document}
```

This model, when implemented in a suitable LP solver, will yield the optimal production quantities \( x_i \) for each month \( i \) that minimize the total cost, considering both the storage and switching costs.

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

\subsection*{Parameters}
\begin{itemize}
    \item $T$: Number of months.
    \item $d_i$: Demand in units at the end of month $i$, for $i = 1, 2, \ldots, T$.
    \item $c_s$: Storage cost per unit per month.
    \item $c_{sw}$: Switching cost per unit change in production level.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $x_i$: Number of units produced in month $i$, for $i = 1, 2, \ldots, T$.
    \item $I_i$: Inventory at the end of month $i$, for $i = 1, 2, \ldots, T$.
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost, which is the sum of storage costs and switching costs:
\[
\text{Minimize } Z = c_s \sum_{i=1}^{T} I_i + c_{sw} \sum_{i=1}^{T-1} |x_{i+1} - x_i|
\]

\subsection*{Constraints}
\begin{align}
    & I_0 = 0 \quad \text{(Starting inventory)} \\
    & x_i + I_{i-1} = d_i + I_i, \quad i = 1, 2, \ldots, T \quad \text{(Flow balance constraint)} \\
    & I_i \geq 0, \quad i = 1, 2, \ldots, T \quad \text{(Non-negativity of inventory)} \\
    & x_i \geq 0, \quad i = 1, 2, \ldots, T \quad \text{(Non-negativity of production)}
\end{align}

Note: The absolute value constraint can be linearized using the following method:
Introduce auxiliary variables $y_i^{+}$ and $y_i^{-}$ for $i=1,2,\ldots,T-1$. Then add the constraints:
\begin{align}
    & x_{i+1} - x_i = y_i^{+} - y_i^{-}, \quad i = 1, 2, \ldots, T-1 \\
    & y_i^{+}, y_i^{-} \geq 0, \quad i = 1, 2, \ldots, T-1
\end{align}

Replace the switching cost term in the objective function by:
\[
c_{sw} \sum_{i=1}^{T-1} (y_i^{+} + y_i^{-})
\]

\end{document}</MATH_MODEL>
<DATA>
{'T': 12, 'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], 'StorageCost': 5, 'SwitchCost': 10}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
Here's the Python code using the Pulp library based on the provided mathematical model and input data in JSON format:

```python
import pulp

#### Data
data = {
    'T': 12, 
    'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], 
    'StorageCost': 5, 
    'SwitchCost': 10
}

#### Parameters
T = data['T']
d = data['Deliver']
c_s = data['StorageCost']
c_sw = data['SwitchCost']

#### Create the linear programming problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

#### Decision variables
x = pulp.LpVariable.dicts("Production", range(1, T + 1), lowBound=0, cat='Continuous')
I = pulp.LpVariable.dicts("Inventory", range(1, T + 1), lowBound=0, cat='Continuous')
y_plus = pulp.LpVariable.dicts("y_plus", range(1, T), lowBound=0, cat='Continuous')
y_minus = pulp.LpVariable.dicts("y_minus", range(1, T), lowBound=0, cat='Continuous')

#### Objective function
problem += (c_s * pulp.lpSum(I[i] for i in range(1, T + 1)) + 
             c_sw * pulp.lpSum(y_plus[i] + y_minus[i] for i in range(1, T)))

#### Constraints
problem += (I[1] == x[1] - d[0], "Flow_Balance_1")
for i in range(2, T + 1):
    problem += (x[i] + I[i - 1] == d[i - 1] + I[i], f"Flow_Balance_{i}")

#### Non-negativity of inventory
for i in range(1, T + 1):
    problem += (I[i] >= 0, f"NonNegativity_Inventory_{i}")
    problem += (x[i] >= 0, f"NonNegativity_Production_{i}")

#### Absolute value linearization constraints
for i in range(1, T):
    problem += (x[i + 1] - x[i] == y_plus[i] - y_minus[i], f"Linearization_{i}")
    problem += (y_plus[i] >= 0, f"NonNegativity_y_plus_{i}")
    problem += (y_minus[i] >= 0, f"NonNegativity_y_minus_{i}")

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
``` 

This code sets up and solves the linear programming problem according to the provided model, using the parameters and constraints laid out in the prompt. The final objective value is printed as requested.

