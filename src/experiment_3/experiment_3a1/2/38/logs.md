# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP
PROBLEM INFO:

- A small computer manufacturing company forecasts the demand over the next \var{n}-th month to be \var{demand_{n}}.
- These demands must be satisfied and can not be shorted.
- In any month it can produce at most \var{max_regular_amount} units, using regular production, at a cost of \var{cost_regular} dollars per unit. 
- By using overtime, it can produce additional units at \var{cost_overtime} dollars per unit. 
- The firm can store units from month to month at a cost of \var{store_cost} dollars per unit per month. 

INPUT FORMAT:

{
	"demand": [demand_{n} for n in 1,...,N],
	"max_regular_amount": max_regular_amount,
	"cost_regular": cost_regular,
	"cost_overtime": cost_overtime,
	"store_cost": store_cost
}


OBJECTIVE: Formulate the problem of determining the production schedule that minimizes the cost.

OUTPUT INFO:

- \var{reg_quant} represents the quantity of products produced using regular production in each future month
- \var{over_quant} represents the quantity of products produced using overtime production in each future month

OUTPUT FORMAT:

{
	"reg_quant": [reg_quant_{n} for n in 1,...,N]
	"over_quant": [over_quant_{n} for n in 1,...,N]
}
</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Production Schedule}

\textbf{Variables:}
\begin{itemize}
    \item Let $reg\_quant_n$ be the quantity of products produced using regular production in month $n$.
    \item Let $over\_quant_n$ be the quantity of products produced using overtime production in month $n$.
    \item Let $inventory_n$ be the quantity of products stored at the end of month $n$.
\end{itemize}

\textbf{Objective Function:}
\[
\text{Minimize } Z = \sum_{n=1}^{N} \left( cost\_regular \cdot reg\_quant_n + cost\_overtime \cdot over\_quant_n + store\_cost \cdot inventory_n \right)
\]

\textbf{Constraints:}

1. \textbf{Demand Satisfaction:}
\[
reg\_quant_n + over\_quant_n + inventory_{n-1} - inventory_n = demand_n \quad \forall n = 1, 2, \ldots, N
\]
Where we define $inventory_0 = 0$ (no initial inventory).

2. \textbf{Regular Production Capacity:}
\[
reg\_quant_n \leq max\_regular\_amount \quad \forall n = 1, 2, \ldots, N
\]

3. \textbf{Non-negativity Constraints:}
\[
reg\_quant_n \geq 0, \quad over\_quant_n \geq 0, \quad inventory_n \geq 0 \quad \forall n = 1, 2, \ldots, N
\]

\textbf{Output Variables:}
\begin{itemize}
    \item $reg\_quant = [reg\_quant_1, reg\_quant_2, \ldots, reg\_quant_N]$
    \item $over\_quant = [over\_quant_1, over\_quant_2, \ldots, over\_quant_N]$
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

\section*{Linear Programming Model for Production Schedule}

\textbf{Variables:}
\begin{itemize}
    \item Let $reg\_quant_n$ be the quantity of products produced using regular production in month $n$.
    \item Let $over\_quant_n$ be the quantity of products produced using overtime production in month $n$.
    \item Let $inventory_n$ be the quantity of products stored at the end of month $n$.
\end{itemize}

\textbf{Objective Function:}
\[
\text{Minimize } Z = \sum_{n=1}^{N} \left( cost\_regular \cdot reg\_quant_n + cost\_overtime \cdot over\_quant_n + store\_cost \cdot inventory_n \right)
\]

\textbf{Constraints:}

1. \textbf{Demand Satisfaction:}
\[
reg\_quant_n + over\_quant_n + inventory_{n-1} - inventory_n = demand_n \quad \forall n = 1, 2, \ldots, N
\]
Where we define $inventory_0 = 0$ (no initial inventory).

2. \textbf{Regular Production Capacity:}
\[
reg\_quant_n \leq max\_regular\_amount \quad \forall n = 1, 2, \ldots, N
\]

3. \textbf{Non-negativity Constraints:}
\[
reg\_quant_n \geq 0, \quad over\_quant_n \geq 0, \quad inventory_n \geq 0 \quad \forall n = 1, 2, \ldots, N
\]

\textbf{Output Variables:}
\begin{itemize}
    \item $reg\_quant = [reg\_quant_1, reg\_quant_2, \ldots, reg\_quant_N]$
    \item $over\_quant = [over\_quant_1, over\_quant_2, \ldots, over\_quant_N]$
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'demand': [10.0, 20.0, 10.0], 'max_regular_amount': 5.0, 'cost_regular': 10.0, 'cost_overtime': 12.0, 'store_cost': 1.0}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data in JSON format
data = json.loads('{"demand": [10.0, 20.0, 10.0], "max_regular_amount": 5.0, "cost_regular": 10.0, "cost_overtime": 12.0, "store_cost": 1.0}')

#### Extracting data
demand = data['demand']
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']

#### Number of months
N = len(demand)

#### Setting up the problem
problem = pulp.LpProblem("Production_Scheduling", pulp.LpMinimize)

#### Decision Variables
reg_quant = [pulp.LpVariable(f'reg_quant_{n}', lowBound=0) for n in range(1, N + 1)]
over_quant = [pulp.LpVariable(f'over_quant_{n}', lowBound=0) for n in range(1, N + 1)]
inventory = [pulp.LpVariable(f'inventory_{n}', lowBound=0) for n in range(1, N + 1)]

#### Objective Function
problem += pulp.lpSum(cost_regular * reg_quant[n - 1] + cost_overtime * over_quant[n - 1] + store_cost * inventory[n - 1] for n in range(1, N + 1)), "Total_Cost"

#### Constraints
#### Demand Satisfaction
for n in range(1, N + 1):
    if n == 1:
        problem += reg_quant[n - 1] + over_quant[n - 1] - inventory[n - 1] == demand[n - 1], f"Demand_Satisfaction_{n}"
    else:
        problem += reg_quant[n - 1] + over_quant[n - 1] + inventory[n - 2] - inventory[n - 1] == demand[n - 1], f"Demand_Satisfaction_{n}"

#### Regular Production Capacity
for n in range(1, N + 1):
    problem += reg_quant[n - 1] <= max_regular_amount, f"Regular_Production_Capacity_{n}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

