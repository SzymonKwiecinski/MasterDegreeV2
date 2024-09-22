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

\subsection*{Indices}
\begin{itemize}
    \item $i$: month index, for $i = 1, 2, \ldots, T$
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item $deliver_i$: units that must be delivered at the end of month $i$
    \item $storage\_cost$: cost of storing one unit of the product for one month
    \item $switch\_cost$: cost of switching production levels between two consecutive months
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $x_i$: number of units produced in month $i$
    \item $I_i$: inventory at the end of month $i$
\end{itemize}

\subsection*{Objective Function}
The objective is to minimize the total cost, which includes production costs, storage costs, and switching costs:

\[
\text{Minimize } Z = \sum_{i=1}^{T} \left( storage\_cost \cdot I_i + switch\_cost \cdot |x_{i} - x_{i-1}| \right)
\]
with the understanding that $x_0 = 0$ (initial production level).

\subsection*{Constraints}
1. \textbf{Delivery Requirement:}
   \[
   I_{i-1} + x_i - deliver_i = I_i \quad \forall i = 1, 2, \ldots, T
   \]
   where $I_0 = 0$ (no initial inventory).

2. \textbf{Non-negativity:}
   \[
   x_i \geq 0 \quad \forall i = 1, 2, \ldots, T
   \]
   \[
   I_i \geq 0 \quad \forall i = 1, 2, \ldots, T
   \]

3. \textbf{No Inventory Cost at Year End:}
   \[
   I_T = 0
   \]

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

\subsection*{Indices}
\begin{itemize}
    \item $i$: month index, for $i = 1, 2, \ldots, T$
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item $deliver_i$: units that must be delivered at the end of month $i$
    \item $storage\_cost$: cost of storing one unit of the product for one month
    \item $switch\_cost$: cost of switching production levels between two consecutive months
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $x_i$: number of units produced in month $i$
    \item $I_i$: inventory at the end of month $i$
\end{itemize}

\subsection*{Objective Function}
The objective is to minimize the total cost, which includes production costs, storage costs, and switching costs:

\[
\text{Minimize } Z = \sum_{i=1}^{T} \left( storage\_cost \cdot I_i + switch\_cost \cdot |x_{i} - x_{i-1}| \right)
\]
with the understanding that $x_0 = 0$ (initial production level).

\subsection*{Constraints}
1. \textbf{Delivery Requirement:}
   \[
   I_{i-1} + x_i - deliver_i = I_i \quad \forall i = 1, 2, \ldots, T
   \]
   where $I_0 = 0$ (no initial inventory).

2. \textbf{Non-negativity:}
   \[
   x_i \geq 0 \quad \forall i = 1, 2, \ldots, T
   \]
   \[
   I_i \geq 0 \quad \forall i = 1, 2, \ldots, T
   \]

3. \textbf{No Inventory Cost at Year End:}
   \[
   I_T = 0
   \]

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

#### Create the model
problem = pulp.LpProblem("Minimize_Total_Cost", pulp.LpMinimize)

#### Decision Variables
x = pulp.LpVariable.dicts("Production", range(1, data['T'] + 1), lowBound=0)
I = pulp.LpVariable.dicts("Inventory", range(0, data['T'] + 1), lowBound=0)

#### Objective Function
problem += pulp.lpSum(data['StorageCost'] * I[i] for i in range(1, data['T'] + 1)) + \
           pulp.lpSum(data['SwitchCost'] * (x[i] - x[i-1]) for i in range(2, data['T'] + 1))

#### Constraints
problem += I[0] == 0  #### Initial inventory is zero

for i in range(1, data['T'] + 1):
    if i == 1:
        problem += I[i] == x[i] - data['Deliver'][i-1]  #### For the first month
    else:
        problem += I[i] == I[i-1] + x[i] - data['Deliver'][i-1]  #### Delivery requirement

#### Ensure no inventory costs at the end of the year
problem += I[data['T']] == 0

#### Solve the problem
problem.solve()

#### Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

