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

\section*{Linear Programming Model for Production Scheduling}

\textbf{Parameters:}
\begin{itemize}
    \item Let $N$ be the number of months.
    \item Let $demand_n$ be the demand for month $n$ where $n = 1, 2, ..., N$.
    \item Let $max\_regular\_amount$ be the maximum number of units that can be produced using regular production in a month.
    \item Let $cost\_regular$ be the cost per unit for regular production.
    \item Let $cost\_overtime$ be the cost per unit for overtime production.
    \item Let $store\_cost$ be the cost of storing one unit for one month.
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item Let $reg\_quant_n$ be the quantity of products produced using regular production in month $n$.
    \item Let $over\_quant_n$ be the quantity of products produced using overtime production in month $n$.
    \item Let $inventory_n$ be the inventory carried over to month $n$.
\end{itemize}

\textbf{Objective Function:}
\begin{align*}
\text{Minimize } Z = \sum_{n=1}^{N} \left( cost\_regular \cdot reg\_quant_n + cost\_overtime \cdot over\_quant_n + store\_cost \cdot inventory_n \right)
\end{align*}

\textbf{Constraints:}
\begin{align*}
1. & \quad reg\_quant_n + over\_quant_n + inventory_{n-1} - inventory_n = demand_n, \quad \forall n = 1, 2, ..., N \\
2. & \quad reg\_quant_n \leq max\_regular\_amount, \quad \forall n = 1, 2, ..., N \\
3. & \quad inventory_n \geq 0, \quad \forall n = 1, 2, ..., N \\
4. & \quad reg\_quant_n \geq 0, \quad \forall n = 1, 2, ..., N \\
5. & \quad over\_quant_n \geq 0, \quad \forall n = 1, 2, ..., N \\
\end{align*}

\textbf{Output:}
\begin{align*}
\{ 
    "reg\_quant": [reg\_quant_1, reg\_quant_2, \ldots, reg\_quant_N], \\
    "over\_quant": [over\_quant_1, over\_quant_2, \ldots, over\_quant_N] 
\}
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

\section*{Linear Programming Model for Production Scheduling}

\textbf{Parameters:}
\begin{itemize}
    \item Let $N$ be the number of months.
    \item Let $demand_n$ be the demand for month $n$ where $n = 1, 2, ..., N$.
    \item Let $max\_regular\_amount$ be the maximum number of units that can be produced using regular production in a month.
    \item Let $cost\_regular$ be the cost per unit for regular production.
    \item Let $cost\_overtime$ be the cost per unit for overtime production.
    \item Let $store\_cost$ be the cost of storing one unit for one month.
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item Let $reg\_quant_n$ be the quantity of products produced using regular production in month $n$.
    \item Let $over\_quant_n$ be the quantity of products produced using overtime production in month $n$.
    \item Let $inventory_n$ be the inventory carried over to month $n$.
\end{itemize}

\textbf{Objective Function:}
\begin{align*}
\text{Minimize } Z = \sum_{n=1}^{N} \left( cost\_regular \cdot reg\_quant_n + cost\_overtime \cdot over\_quant_n + store\_cost \cdot inventory_n \right)
\end{align*}

\textbf{Constraints:}
\begin{align*}
1. & \quad reg\_quant_n + over\_quant_n + inventory_{n-1} - inventory_n = demand_n, \quad \forall n = 1, 2, ..., N \\
2. & \quad reg\_quant_n \leq max\_regular\_amount, \quad \forall n = 1, 2, ..., N \\
3. & \quad inventory_n \geq 0, \quad \forall n = 1, 2, ..., N \\
4. & \quad reg\_quant_n \geq 0, \quad \forall n = 1, 2, ..., N \\
5. & \quad over\_quant_n \geq 0, \quad \forall n = 1, 2, ..., N \\
\end{align*}

\textbf{Output:}
\begin{align*}
\{ 
    "reg\_quant": [reg\_quant_1, reg\_quant_2, \ldots, reg\_quant_N], \\
    "over\_quant": [over\_quant_1, over\_quant_2, \ldots, over\_quant_N] 
\}
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'demand': [10.0, 20.0, 10.0], 'max_regular_amount': 5.0, 'cost_regular': 10.0, 'cost_overtime': 12.0, 'store_cost': 1.0}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data provided
data = {'demand': [10.0, 20.0, 10.0], 
        'max_regular_amount': 5.0, 
        'cost_regular': 10.0, 
        'cost_overtime': 12.0, 
        'store_cost': 1.0}

#### Parameters
demand = data['demand']
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']
N = len(demand)

#### Problem definition
problem = pulp.LpProblem("Production_Scheduling", pulp.LpMinimize)

#### Decision Variables
reg_quant = [pulp.LpVariable(f'reg_quant_{n+1}', lowBound=0) for n in range(N)]
over_quant = [pulp.LpVariable(f'over_quant_{n+1}', lowBound=0) for n in range(N)]
inventory = [pulp.LpVariable(f'inventory_{n+1}', lowBound=0) for n in range(N)]

#### Objective Function
problem += pulp.lpSum(
    cost_regular * reg_quant[n] + 
    cost_overtime * over_quant[n] + 
    store_cost * inventory[n] for n in range(N)
)

#### Constraints
for n in range(N):
    if n == 0:
        #### For the first month, assume initial inventory is zero
        problem += reg_quant[n] + over_quant[n] - inventory[n] == demand[n]
    else:
        problem += reg_quant[n] + over_quant[n] + inventory[n-1] - inventory[n] == demand[n]

    problem += reg_quant[n] <= max_regular_amount

#### Solve the Problem
problem.solve()

#### Output results
reg_quant_output = [pulp.value(reg_quant[n]) for n in range(N)]
over_quant_output = [pulp.value(over_quant[n]) for n in range(N)]

print(f'Regular Production Quantities: {reg_quant_output}')
print(f'Overtime Production Quantities: {over_quant_output}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

