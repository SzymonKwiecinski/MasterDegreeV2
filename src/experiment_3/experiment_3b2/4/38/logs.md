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

\section*{Linear Programming Model for Minimizing Production and Storage Costs}

Given the forecasted demand, production limits, and costs, the goal is to determine the production schedule that minimizes costs over \(N\) months.

\subsection*{Parameters}
\begin{itemize}
    \item \(demand_n\): Demand for month \(n\), \(n = 1, \ldots, N\)
    \item \(max\_regular\_amount\): Maximum units produced using regular production per month
    \item \(cost\_regular\): Cost per unit for regular production
    \item \(cost\_overtime\): Cost per unit for overtime production
    \item \(store\_cost\): Cost per unit for storing inventory each month
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \(reg\_quant_n\): Quantity produced using regular production in month \(n\)
    \item \(over\_quant_n\): Quantity produced using overtime in month \(n\)
    \item \(store_n\): Inventory stored at the end of month \(n\)
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost:
\[
\min \sum_{n=1}^{N} \left( cost\_regular \cdot reg\_quant_n + cost\_overtime \cdot over\_quant_n + store\_cost \cdot store_n \right)
\]

\subsection*{Constraints}
\begin{align}
    & reg\_quant_n \leq max\_regular\_amount \quad \forall n = 1, \ldots, N \\
    & reg\_quant_n + over\_quant_n + store_{n-1} = demand_n + store_n \quad \forall n = 1, \ldots, N \\
    & store_0 = 0 \\
    & reg\_quant_n, over\_quant_n, store_n \geq 0 \quad \forall n = 1, \ldots, N
\end{align}

\subsection*{Explanation}
- Constraint (1) ensures the production using regular hours does not exceed the maximum allowed.
- Constraint (2) ensures the flow balance: production plus previous inventory meets the demand and leaves some inventory for the next month.
- Constraint (3) sets the initial inventory as zero.
- Constraint (4) ensures non-negativity of production and inventory.

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

\section*{Linear Programming Model for Minimizing Production and Storage Costs}

Given the forecasted demand, production limits, and costs, the goal is to determine the production schedule that minimizes costs over \(N\) months.

\subsection*{Parameters}
\begin{itemize}
    \item \(demand_n\): Demand for month \(n\), \(n = 1, \ldots, N\)
    \item \(max\_regular\_amount\): Maximum units produced using regular production per month
    \item \(cost\_regular\): Cost per unit for regular production
    \item \(cost\_overtime\): Cost per unit for overtime production
    \item \(store\_cost\): Cost per unit for storing inventory each month
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \(reg\_quant_n\): Quantity produced using regular production in month \(n\)
    \item \(over\_quant_n\): Quantity produced using overtime in month \(n\)
    \item \(store_n\): Inventory stored at the end of month \(n\)
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost:
\[
\min \sum_{n=1}^{N} \left( cost\_regular \cdot reg\_quant_n + cost\_overtime \cdot over\_quant_n + store\_cost \cdot store_n \right)
\]

\subsection*{Constraints}
\begin{align}
    & reg\_quant_n \leq max\_regular\_amount \quad \forall n = 1, \ldots, N \\
    & reg\_quant_n + over\_quant_n + store_{n-1} = demand_n + store_n \quad \forall n = 1, \ldots, N \\
    & store_0 = 0 \\
    & reg\_quant_n, over\_quant_n, store_n \geq 0 \quad \forall n = 1, \ldots, N
\end{align}

\subsection*{Explanation}
- Constraint (1) ensures the production using regular hours does not exceed the maximum allowed.
- Constraint (2) ensures the flow balance: production plus previous inventory meets the demand and leaves some inventory for the next month.
- Constraint (3) sets the initial inventory as zero.
- Constraint (4) ensures non-negativity of production and inventory.

\end{document}</MATH_MODEL>
<DATA>
{'demand': [10.0, 20.0, 10.0], 'max_regular_amount': 5.0, 'cost_regular': 10.0, 'cost_overtime': 12.0, 'store_cost': 1.0}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {
    'demand': [10.0, 20.0, 10.0],
    'max_regular_amount': 5.0,
    'cost_regular': 10.0,
    'cost_overtime': 12.0,
    'store_cost': 1.0
}

N = len(data['demand'])

#### Create a linear programming problem
problem = pulp.LpProblem("Minimize_Production_and_Storage_Costs", pulp.LpMinimize)

#### Decision Variables
reg_quant = [pulp.LpVariable(f'reg_quant_{n}', lowBound=0) for n in range(N)]
over_quant = [pulp.LpVariable(f'over_quant_{n}', lowBound=0) for n in range(N)]
store = [pulp.LpVariable(f'store_{n}', lowBound=0) for n in range(N)]

#### Objective Function
problem += pulp.lpSum([
    data['cost_regular'] * reg_quant[n] +
    data['cost_overtime'] * over_quant[n] +
    data['store_cost'] * store[n]
    for n in range(N)
])

#### Constraints
#### Regular production limit
for n in range(N):
    problem += reg_quant[n] <= data['max_regular_amount']

#### Inventory and demand balance
for n in range(N):
    if n == 0:
        problem += reg_quant[n] + over_quant[n] == data['demand'][n] + store[n]
    else:
        problem += reg_quant[n] + over_quant[n] + store[n-1] == data['demand'][n] + store[n]

#### Initial inventory constraint
problem += store[0] == 0

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

