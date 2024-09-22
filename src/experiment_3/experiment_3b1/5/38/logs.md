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

\section*{Production Schedule Optimization}

Let:
\begin{itemize}
    \item $N$ be the total number of months.
    \item $demand_n$ be the demand in month $n$.
    \item $max\_regular\_amount$ be the maximum regular production in any month.
    \item $cost\_regular$ be the cost of regular production per unit.
    \item $cost\_overtime$ be the cost of overtime production per unit.
    \item $store\_cost$ be the cost of storing units per unit per month.
    \item $reg\_quant_n$ be the quantity of products produced using regular production in month $n$.
    \item $over\_quant_n$ be the quantity of products produced using overtime production in month $n$.
    \item $inventory_n$ be the inventory carried over to month $n$.
\end{itemize}

\subsection*{Objective Function}

The objective is to minimize the total cost, which can be expressed as:

\[
\text{Minimize } Z = \sum_{n=1}^{N} \left( cost\_regular \cdot reg\_quant_n + cost\_overtime \cdot over\_quant_n + store\_cost \cdot inventory_n \right)
\]

\subsection*{Constraints}

\begin{itemize}
    \item Demand satisfaction:
    \[
    inventory_{n-1} + reg\_quant_n + over\_quant_n - demand_n = inventory_n \quad \text{for } n=1,\ldots,N
    \]
    with $inventory_0 = 0$ (initial inventory).

    \item Regular production limit:
    \[
    reg\_quant_n \leq max\_regular\_amount \quad \text{for } n=1,\ldots,N
    \]

    \item Non-negativity constraints:
    \[
    reg\_quant_n \geq 0, \quad over\_quant_n \geq 0, \quad inventory_n \geq 0 \quad \text{for } n=1,\ldots,N
    \]
\end{itemize}

\subsection*{Input Format}

The model takes the following input:

\[
\{ 
    "demand": [demand_{n} \text{ for } n = 1,\ldots,N], 
    "max\_regular\_amount": max\_regular\_amount, 
    "cost\_regular": cost\_regular, 
    "cost\_overtime": cost\_overtime, 
    "store\_cost": store\_cost 
\}
\]

\subsection*{Output Format}

The model outputs:

\[
\{ 
    "reg\_quant": [reg\_quant_{n} \text{ for } n = 1,\ldots,N], 
    "over\_quant": [over\_quant_{n} \text{ for } n = 1,\ldots,N] 
\}
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

\section*{Production Schedule Optimization}

Let:
\begin{itemize}
    \item $N$ be the total number of months.
    \item $demand_n$ be the demand in month $n$.
    \item $max\_regular\_amount$ be the maximum regular production in any month.
    \item $cost\_regular$ be the cost of regular production per unit.
    \item $cost\_overtime$ be the cost of overtime production per unit.
    \item $store\_cost$ be the cost of storing units per unit per month.
    \item $reg\_quant_n$ be the quantity of products produced using regular production in month $n$.
    \item $over\_quant_n$ be the quantity of products produced using overtime production in month $n$.
    \item $inventory_n$ be the inventory carried over to month $n$.
\end{itemize}

\subsection*{Objective Function}

The objective is to minimize the total cost, which can be expressed as:

\[
\text{Minimize } Z = \sum_{n=1}^{N} \left( cost\_regular \cdot reg\_quant_n + cost\_overtime \cdot over\_quant_n + store\_cost \cdot inventory_n \right)
\]

\subsection*{Constraints}

\begin{itemize}
    \item Demand satisfaction:
    \[
    inventory_{n-1} + reg\_quant_n + over\_quant_n - demand_n = inventory_n \quad \text{for } n=1,\ldots,N
    \]
    with $inventory_0 = 0$ (initial inventory).

    \item Regular production limit:
    \[
    reg\_quant_n \leq max\_regular\_amount \quad \text{for } n=1,\ldots,N
    \]

    \item Non-negativity constraints:
    \[
    reg\_quant_n \geq 0, \quad over\_quant_n \geq 0, \quad inventory_n \geq 0 \quad \text{for } n=1,\ldots,N
    \]
\end{itemize}

\subsection*{Input Format}

The model takes the following input:

\[
\{ 
    "demand": [demand_{n} \text{ for } n = 1,\ldots,N], 
    "max\_regular\_amount": max\_regular\_amount, 
    "cost\_regular": cost\_regular, 
    "cost\_overtime": cost\_overtime, 
    "store\_cost": store\_cost 
\}
\]

\subsection*{Output Format}

The model outputs:

\[
\{ 
    "reg\_quant": [reg\_quant_{n} \text{ for } n = 1,\ldots,N], 
    "over\_quant": [over\_quant_{n} \text{ for } n = 1,\ldots,N] 
\}
\]

\end{document}</MATH_MODEL>
<DATA>
{'demand': [10.0, 20.0, 10.0], 'max_regular_amount': 5.0, 'cost_regular': 10.0, 'cost_overtime': 12.0, 'store_cost': 1.0}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data input in JSON format
data = json.loads('{"demand": [10.0, 20.0, 10.0], "max_regular_amount": 5.0, "cost_regular": 10.0, "cost_overtime": 12.0, "store_cost": 1.0}')

#### Extracting data
demand = data['demand']
N = len(demand)
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']

#### Creating the problem
problem = pulp.LpProblem("Production_Schedule_Optimization", pulp.LpMinimize)

#### Decision Variables
reg_quant = [pulp.LpVariable(f'reg_quant_{n}', lowBound=0) for n in range(N)]
over_quant = [pulp.LpVariable(f'over_quant_{n}', lowBound=0) for n in range(N)]
inventory = [pulp.LpVariable(f'inventory_{n}', lowBound=0) for n in range(N)]

#### Objective Function
problem += pulp.lpSum(cost_regular * reg_quant[n] + cost_overtime * over_quant[n] + store_cost * inventory[n] for n in range(N))

#### Constraints
#### Demand satisfaction
for n in range(N):
    if n == 0:
        problem += (0 + reg_quant[n] + over_quant[n] - demand[n] == inventory[n])
    else:
        problem += (inventory[n-1] + reg_quant[n] + over_quant[n] - demand[n] == inventory[n])

#### Regular production limit
for n in range(N):
    problem += (reg_quant[n] <= max_regular_amount)

#### Solve the problem
problem.solve()

#### Output Results
reg_quant_values = [reg_quant[n].varValue for n in range(N)]
over_quant_values = [over_quant[n].varValue for n in range(N)]

print(f'Regular Production Quantities: {reg_quant_values}')
print(f'Overtime Production Quantities: {over_quant_values}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

