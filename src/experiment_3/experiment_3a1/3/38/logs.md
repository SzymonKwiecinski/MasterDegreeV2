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

\textbf{Variables:}
\begin{itemize}
    \item Let \( \text{reg\_quant}_{n} \) be the quantity of products produced using regular production in month \( n \).
    \item Let \( \text{over\_quant}_{n} \) be the quantity of products produced using overtime production in month \( n \).
    \item Let \( \text{inventory}_{n} \) be the quantity of products stored in inventory at the end of month \( n \).
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item \( \text{demand}_{n} \): Demand in month \( n \).
    \item \( \text{max\_regular\_amount} \): Maximum quantity that can be produced using regular production in a month.
    \item \( \text{cost\_regular} \): Cost per unit for regular production.
    \item \( \text{cost\_overtime} \): Cost per unit for overtime production.
    \item \( \text{store\_cost} \): Cost per unit for storing inventory per month.
\end{itemize}

\textbf{Objective Function:}
\[
\text{Minimize } Z = \sum_{n=1}^{N} \left( \text{cost\_regular} \cdot \text{reg\_quant}_{n} + \text{cost\_overtime} \cdot \text{over\_quant}_{n} + \text{store\_cost} \cdot \text{inventory}_{n} \right)
\]

\textbf{Constraints:}
\begin{align*}
\text{1. Demand Satisfaction:} & \quad \text{reg\_quant}_{n} + \text{over\_quant}_{n} + \text{inventory}_{n-1} \geq \text{demand}_{n} \quad \forall n \in \{1, \ldots, N\} \\
\text{2. Regular Production Limit:} & \quad \text{reg\_quant}_{n} \leq \text{max\_regular\_amount} \quad \forall n \in \{1, \ldots, N\} \\
\text{3. Inventory Balance:} & \quad \text{inventory}_{n} = \text{inventory}_{n-1} + \text{reg\_quant}_{n} + \text{over\_quant}_{n} - \text{demand}_{n} \quad \forall n \in \{1, \ldots, N\} \\
\text{4. Non-negativity:} & \quad \text{reg\_quant}_{n} \geq 0, \quad \text{over\_quant}_{n} \geq 0, \quad \text{inventory}_{n} \geq 0 \quad \forall n \in \{1, \ldots, N\}
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

\textbf{Variables:}
\begin{itemize}
    \item Let \( \text{reg\_quant}_{n} \) be the quantity of products produced using regular production in month \( n \).
    \item Let \( \text{over\_quant}_{n} \) be the quantity of products produced using overtime production in month \( n \).
    \item Let \( \text{inventory}_{n} \) be the quantity of products stored in inventory at the end of month \( n \).
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item \( \text{demand}_{n} \): Demand in month \( n \).
    \item \( \text{max\_regular\_amount} \): Maximum quantity that can be produced using regular production in a month.
    \item \( \text{cost\_regular} \): Cost per unit for regular production.
    \item \( \text{cost\_overtime} \): Cost per unit for overtime production.
    \item \( \text{store\_cost} \): Cost per unit for storing inventory per month.
\end{itemize}

\textbf{Objective Function:}
\[
\text{Minimize } Z = \sum_{n=1}^{N} \left( \text{cost\_regular} \cdot \text{reg\_quant}_{n} + \text{cost\_overtime} \cdot \text{over\_quant}_{n} + \text{store\_cost} \cdot \text{inventory}_{n} \right)
\]

\textbf{Constraints:}
\begin{align*}
\text{1. Demand Satisfaction:} & \quad \text{reg\_quant}_{n} + \text{over\_quant}_{n} + \text{inventory}_{n-1} \geq \text{demand}_{n} \quad \forall n \in \{1, \ldots, N\} \\
\text{2. Regular Production Limit:} & \quad \text{reg\_quant}_{n} \leq \text{max\_regular\_amount} \quad \forall n \in \{1, \ldots, N\} \\
\text{3. Inventory Balance:} & \quad \text{inventory}_{n} = \text{inventory}_{n-1} + \text{reg\_quant}_{n} + \text{over\_quant}_{n} - \text{demand}_{n} \quad \forall n \in \{1, \ldots, N\} \\
\text{4. Non-negativity:} & \quad \text{reg\_quant}_{n} \geq 0, \quad \text{over\_quant}_{n} \geq 0, \quad \text{inventory}_{n} \geq 0 \quad \forall n \in \{1, \ldots, N\}
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'demand': [10.0, 20.0, 10.0], 'max_regular_amount': 5.0, 'cost_regular': 10.0, 'cost_overtime': 12.0, 'store_cost': 1.0}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the provided JSON
data = {
    'demand': [10.0, 20.0, 10.0],
    'max_regular_amount': 5.0,
    'cost_regular': 10.0,
    'cost_overtime': 12.0,
    'store_cost': 1.0
}

#### Create a linear programming problem
problem = pulp.LpProblem("ProductionScheduling", pulp.LpMinimize)

#### Define variables
N = len(data['demand'])
reg_quant = [pulp.LpVariable(f'reg_quant_{n}', lowBound=0) for n in range(N)]
over_quant = [pulp.LpVariable(f'over_quant_{n}', lowBound=0) for n in range(N)]
inventory = [pulp.LpVariable(f'inventory_{n}', lowBound=0) for n in range(N)]

#### Objective function
problem += pulp.lpSum(
    data['cost_regular'] * reg_quant[n] + 
    data['cost_overtime'] * over_quant[n] + 
    data['store_cost'] * inventory[n] 
    for n in range(N)
)

#### Constraints
for n in range(N):
    #### Demand Satisfaction
    if n == 0:
        problem += reg_quant[n] + over_quant[n] >= data['demand'][n]
    else:
        problem += reg_quant[n] + over_quant[n] + inventory[n-1] >= data['demand'][n]

    #### Regular Production Limit
    problem += reg_quant[n] <= data['max_regular_amount']

    #### Inventory Balance
    if n == 0:
        problem += inventory[n] == reg_quant[n] + over_quant[n] - data['demand'][n]
    else:
        problem += inventory[n] == inventory[n-1] + reg_quant[n] + over_quant[n] - data['demand'][n]

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

