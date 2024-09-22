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

\section*{Production Scheduling Linear Programming Model}

\subsection*{Parameters}
\begin{itemize}
    \item $N$: Total number of months
    \item $demand_n$: Demand in month $n$ for $n = 1, \ldots, N$
    \item $max\_regular\_amount$: Maximum units that can be produced using regular production in any month
    \item $cost\_regular$: Cost per unit produced using regular production
    \item $cost\_overtime$: Cost per unit produced using overtime production
    \item $store\_cost$: Cost of storing one unit for one month
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $reg\_quant_n$: Quantity of products produced using regular production in month $n$
    \item $over\_quant_n$: Quantity of products produced using overtime production in month $n$
    \item $inventory_n$: Inventory (stored units) at the end of month $n$
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost:
\[
\text{Minimize } Z = \sum_{n=1}^{N} \left( cost\_regular \cdot reg\_quant_n + cost\_overtime \cdot over\_quant_n + store\_cost \cdot inventory_n \right)
\]

\subsection*{Constraints}
\begin{align*}
1. & \quad reg\_quant_n + over\_quant_n + inventory_{n-1} - inventory_n = demand_n, \quad \forall n = 1, \ldots, N \\
2. & \quad reg\_quant_n \leq max\_regular\_amount, \quad \forall n = 1, \ldots, N \\
3. & \quad inventory_n \geq 0, \quad \forall n = 1, \ldots, N \\
4. & \quad inventory_0 = 0 \quad (\text{initial inventory}) \\
\end{align*}

\subsection*{Output}
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

\section*{Production Scheduling Linear Programming Model}

\subsection*{Parameters}
\begin{itemize}
    \item $N$: Total number of months
    \item $demand_n$: Demand in month $n$ for $n = 1, \ldots, N$
    \item $max\_regular\_amount$: Maximum units that can be produced using regular production in any month
    \item $cost\_regular$: Cost per unit produced using regular production
    \item $cost\_overtime$: Cost per unit produced using overtime production
    \item $store\_cost$: Cost of storing one unit for one month
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $reg\_quant_n$: Quantity of products produced using regular production in month $n$
    \item $over\_quant_n$: Quantity of products produced using overtime production in month $n$
    \item $inventory_n$: Inventory (stored units) at the end of month $n$
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost:
\[
\text{Minimize } Z = \sum_{n=1}^{N} \left( cost\_regular \cdot reg\_quant_n + cost\_overtime \cdot over\_quant_n + store\_cost \cdot inventory_n \right)
\]

\subsection*{Constraints}
\begin{align*}
1. & \quad reg\_quant_n + over\_quant_n + inventory_{n-1} - inventory_n = demand_n, \quad \forall n = 1, \ldots, N \\
2. & \quad reg\_quant_n \leq max\_regular\_amount, \quad \forall n = 1, \ldots, N \\
3. & \quad inventory_n \geq 0, \quad \forall n = 1, \ldots, N \\
4. & \quad inventory_0 = 0 \quad (\text{initial inventory}) \\
\end{align*}

\subsection*{Output}
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

#### Data from JSON input
data = {
    'demand': [10.0, 20.0, 10.0],
    'max_regular_amount': 5.0,
    'cost_regular': 10.0,
    'cost_overtime': 12.0,
    'store_cost': 1.0
}

N = len(data['demand'])
demand = data['demand']
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']

#### Create the linear programming problem
problem = pulp.LpProblem("Production_Scheduling", pulp.LpMinimize)

#### Decision Variables
reg_quant = pulp.LpVariable.dicts("RegQuant", range(N), lowBound=0, upBound=max_regular_amount)
over_quant = pulp.LpVariable.dicts("OverQuant", range(N), lowBound=0)
inventory = pulp.LpVariable.dicts("Inventory", range(N + 1), lowBound=0)

#### Objective Function
problem += pulp.lpSum(cost_regular * reg_quant[n] + cost_overtime * over_quant[n] + store_cost * inventory[n] for n in range(N))

#### Constraints
#### Initial inventory
problem += (inventory[0] == 0)

#### Monthly constraints
for n in range(N):
    if n == 0:
        problem += (reg_quant[n] + over_quant[n] - inventory[n] == demand[n])
    else:
        problem += (reg_quant[n] + over_quant[n] + inventory[n-1] - inventory[n] == demand[n])
    
    #### Maximum regular production constraint
    problem += (reg_quant[n] <= max_regular_amount)
    
    #### Non-negativity of inventory
    problem += (inventory[n] >= 0)

#### Solve the problem
problem.solve()

#### Output results
reg_quant_result = [reg_quant[n].varValue for n in range(N)]
over_quant_result = [over_quant[n].varValue for n in range(N)]

print(f'Regular Production Quantities: {reg_quant_result}')
print(f'Overtime Production Quantities: {over_quant_result}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

