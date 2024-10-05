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

\subsection*{Parameters}
\begin{itemize}
    \item Let \( N \) be the number of months.
    \item Let \( demand_n \) be the demand in month \( n \) for \( n = 1, 2, \ldots, N \).
    \item Let \( max\_regular\_amount \) be the maximum units produced using regular production in any month.
    \item Let \( cost\_regular \) be the cost of producing one unit using regular production.
    \item Let \( cost\_overtime \) be the cost of producing one unit using overtime production.
    \item Let \( store\_cost \) be the cost of storing one unit for one month.
    \item Let \( reg\_quant_n \) be the quantity of products produced using regular production in month \( n \).
    \item Let \( over\_quant_n \) be the quantity of products produced using overtime production in month \( n \).
    \item Let \( inventory_n \) be the inventory at the end of month \( n \).
\end{itemize}

\subsection*{Constraints}
\begin{align}
    & reg\_quant_n + over\_quant_n + inventory_{n-1} = demand_n + inventory_n, \quad \forall n \in \{1, 2, \ldots, N\} \\
    & reg\_quant_n \leq max\_regular\_amount, \quad \forall n \in \{1, 2, \ldots, N\} \\
    & reg\_quant_n, over\_quant_n \geq 0, \quad \forall n \in \{1, 2, \ldots, N\} \\
    & inventory_0 = 0 \text{ (initial inventory)}
\end{align}

\subsection*{Objective Function}
\begin{align}
    \text{Minimize } Z = \sum_{n=1}^{N} \left( cost\_regular \cdot reg\_quant_n + cost\_overtime \cdot over\_quant_n + store\_cost \cdot inventory_n \right)
\end{align}

\subsection*{Output}
The output will consist of:
\begin{itemize}
    \item \( reg\_quant = [reg\_quant_1, reg\_quant_2, \ldots, reg\_quant_N] \)
    \item \( over\_quant = [over\_quant_1, over\_quant_2, \ldots, over\_quant_N] \)
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

\section*{Production Schedule Optimization}

\subsection*{Parameters}
\begin{itemize}
    \item Let \( N \) be the number of months.
    \item Let \( demand_n \) be the demand in month \( n \) for \( n = 1, 2, \ldots, N \).
    \item Let \( max\_regular\_amount \) be the maximum units produced using regular production in any month.
    \item Let \( cost\_regular \) be the cost of producing one unit using regular production.
    \item Let \( cost\_overtime \) be the cost of producing one unit using overtime production.
    \item Let \( store\_cost \) be the cost of storing one unit for one month.
    \item Let \( reg\_quant_n \) be the quantity of products produced using regular production in month \( n \).
    \item Let \( over\_quant_n \) be the quantity of products produced using overtime production in month \( n \).
    \item Let \( inventory_n \) be the inventory at the end of month \( n \).
\end{itemize}

\subsection*{Constraints}
\begin{align}
    & reg\_quant_n + over\_quant_n + inventory_{n-1} = demand_n + inventory_n, \quad \forall n \in \{1, 2, \ldots, N\} \\
    & reg\_quant_n \leq max\_regular\_amount, \quad \forall n \in \{1, 2, \ldots, N\} \\
    & reg\_quant_n, over\_quant_n \geq 0, \quad \forall n \in \{1, 2, \ldots, N\} \\
    & inventory_0 = 0 \text{ (initial inventory)}
\end{align}

\subsection*{Objective Function}
\begin{align}
    \text{Minimize } Z = \sum_{n=1}^{N} \left( cost\_regular \cdot reg\_quant_n + cost\_overtime \cdot over\_quant_n + store\_cost \cdot inventory_n \right)
\end{align}

\subsection*{Output}
The output will consist of:
\begin{itemize}
    \item \( reg\_quant = [reg\_quant_1, reg\_quant_2, \ldots, reg\_quant_N] \)
    \item \( over\_quant = [over\_quant_1, over\_quant_2, \ldots, over\_quant_N] \)
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'demand': [10.0, 20.0, 10.0], 'max_regular_amount': 5.0, 'cost_regular': 10.0, 'cost_overtime': 12.0, 'store_cost': 1.0}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the JSON format
data = {'demand': [10.0, 20.0, 10.0], 
        'max_regular_amount': 5.0, 
        'cost_regular': 10.0, 
        'cost_overtime': 12.0, 
        'store_cost': 1.0}

#### Extracting parameters
demand = data['demand']
N = len(demand)
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']

#### Defining the problem
problem = pulp.LpProblem("Production_Schedule_Optimization", pulp.LpMinimize)

#### Variables
reg_quant = [pulp.LpVariable(f'reg_quant_{n}', lowBound=0, cat='Continuous') for n in range(N)]
over_quant = [pulp.LpVariable(f'over_quant_{n}', lowBound=0, cat='Continuous') for n in range(N)]
inventory = [pulp.LpVariable(f'inventory_{n}', lowBound=0, cat='Continuous') for n in range(N)]

#### Constraints
for n in range(N):
    if n == 0:
        prev_inventory = 0  #### inventory_0 = 0
    else:
        prev_inventory = inventory[n-1]
    
    #### Inventory balance constraint
    problem += reg_quant[n] + over_quant[n] + prev_inventory == demand[n] + inventory[n]
    
    #### Maximum regular production constraint
    problem += reg_quant[n] <= max_regular_amount

#### Objective function
problem += pulp.lpSum(
    cost_regular * reg_quant[n] + 
    cost_overtime * over_quant[n] + 
    store_cost * inventory[n]
    for n in range(N)
)

#### Solve the problem
problem.solve()

#### Output
reg_quant_values = [reg_quant[n].varValue for n in range(N)]
over_quant_values = [over_quant[n].varValue for n in range(N)]

print('Regular Production Quantities:', reg_quant_values)
print('Overtime Production Quantities:', over_quant_values)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

