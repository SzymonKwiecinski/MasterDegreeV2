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
To formulate the given problem as a linear programming model in LaTeX, we define decision variables, constraints, and the objective function. The decision variables include the quantity of products produced using regular and overtime production in each future month, as well as the inventory levels at the end of each month.

Let's denote:
- \( reg\_quant_n \) as the quantity produced in month \( n \) using regular production.
- \( over\_quant_n \) as the quantity produced in month \( n \) using overtime production.
- \( inv_n \) as the inventory at the end of month \( n \).

The objective is to minimize the total production and storage costs over \( N \) months.

```latex
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\section*{Linear Programming Model}

\textbf{Objective:}
\[
\text{Minimize } \sum_{n=1}^{N} \left( cost\_regular \times reg\_quant_n + cost\_overtime \times over\_quant_n + store\_cost \times inv_n \right)
\]

\textbf{Subject to:}
\[
reg\_quant_n \leq max\_regular\_amount, \quad \forall n = 1, \ldots, N
\]

\[
reg\_quant_n + over\_quant_n + inv_{n-1} = demand_n + inv_n, \quad \forall n = 1, \ldots, N
\]

\[
reg\_quant_n \geq 0, \quad over\_quant_n \geq 0, \quad inv_n \geq 0, \quad \forall n = 1, \ldots, N
\]

\textbf{Initial inventory:}
\[
inv_0 = 0
\]

\end{document}
```

- The objective function represents the total cost, which includes the costs of regular production, overtime production, and storing inventory.
- The constraints ensure that the production in any month does not exceed the regular production capacity, that demand is met by production plus beginning inventory, and that all variables are non-negative.
- The initial inventory is set to zero, assuming no initial stock is available.

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

\textbf{Objective:}
\[
\text{Minimize } \sum_{n=1}^{N} \left( cost\_regular \times reg\_quant_n + cost\_overtime \times over\_quant_n + store\_cost \times inv_n \right)
\]

\textbf{Subject to:}
\[
reg\_quant_n \leq max\_regular\_amount, \quad \forall n = 1, \ldots, N
\]

\[
reg\_quant_n + over\_quant_n + inv_{n-1} = demand_n + inv_n, \quad \forall n = 1, \ldots, N
\]

\[
reg\_quant_n \geq 0, \quad over\_quant_n \geq 0, \quad inv_n \geq 0, \quad \forall n = 1, \ldots, N
\]

\textbf{Initial inventory:}
\[
inv_0 = 0
\]

\end{document}</MATH_MODEL>
<DATA>
{'demand': [10.0, 20.0, 10.0], 'max_regular_amount': 5.0, 'cost_regular': 10.0, 'cost_overtime': 12.0, 'store_cost': 1.0}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Load data from JSON format
data = json.loads('{"demand": [10.0, 20.0, 10.0], "max_regular_amount": 5.0, "cost_regular": 10.0, "cost_overtime": 12.0, "store_cost": 1.0}')

#### Problem parameters
demand = data['demand']
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']
N = len(demand)

#### Create the problem
problem = pulp.LpProblem("Production_Planning", pulp.LpMinimize)

#### Define decision variables
reg_quant = [pulp.LpVariable(f'reg_quant_{n}', lowBound=0) for n in range(N)]
over_quant = [pulp.LpVariable(f'over_quant_{n}', lowBound=0) for n in range(N)]
inv = [pulp.LpVariable(f'inv_{n}', lowBound=0) for n in range(N)]

#### Objective function
problem += pulp.lpSum(cost_regular * reg_quant[n] + cost_overtime * over_quant[n] + store_cost * inv[n] for n in range(N))

#### Constraints
#### Regular quantity constraint
for n in range(N):
    problem += reg_quant[n] <= max_regular_amount

#### Inventory balance constraint
for n in range(N):
    if n == 0:
        problem += reg_quant[n] + over_quant[n] == demand[n] + inv[n]
    else:
        problem += reg_quant[n] + over_quant[n] + inv[n-1] == demand[n] + inv[n]

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

