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
To formulate this problem as a Linear Programming (LP) model, we need to determine the quantities of regular production, overtime production, and inventory storage for each month to minimize the total cost. Let's use the following notation:

- \(N\): Total number of months
- \(demand_n\): Demand in month \(n\)
- \(max\_regular\_amount\): Maximum regular production per month
- \(cost\_regular\): Cost per unit for regular production
- \(cost\_overtime\): Cost per unit for overtime production
- \(store\_cost\): Cost to store one unit for one month

Variables:
- \(reg\_quant_n\): Quantity produced using regular production in month \(n\)
- \(over\_quant_n\): Quantity produced using overtime production in month \(n\)
- \(inv_n\): Inventory at the end of month \(n\)

Objective:
Minimize the total cost which includes the cost of regular production, overtime production, and inventory storage over the \(N\) months:
\[
\text{Minimize} \quad \sum_{n=1}^{N} \left( cost\_regular \cdot reg\_quant_n + cost\_overtime \cdot over\_quant_n + store\_cost \cdot inv_n \right)
\]

Constraints:
1. Demand satisfaction for each month:
   \[
   reg\_quant_n + over\_quant_n + inv_{n-1} = demand_n + inv_n, \quad \forall n = 1, \ldots, N
   \]
   (Assume \(inv_0 = 0\) as initial inventory)

2. Regular production limit:
   \[
   reg\_quant_n \leq max\_regular\_amount, \quad \forall n = 1, \ldots, N
   \]

3. Non-negativity constraints:
   \[
   reg\_quant_n, over\_quant_n, inv_n \geq 0, \quad \forall n = 1, \ldots, N
   \]

The following is the complete mathematical model in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Production Scheduling}

\textbf{Objective:}

\[
\text{Minimize} \quad Z = \sum_{n=1}^{N} \left( cost\_regular \cdot reg\_quant_n + cost\_overtime \cdot over\_quant_n + store\_cost \cdot inv_n \right)
\]

\textbf{Subject to:}

\begin{align*}
& reg\_quant_n + over\_quant_n + inv_{n-1} = demand_n + inv_n, \quad \forall n = 1, \ldots, N \\
& reg\_quant_n \leq max\_regular\_amount, \quad \forall n = 1, \ldots, N \\
& reg\_quant_n \geq 0, \quad \forall n = 1, \ldots, N \\
& over\_quant_n \geq 0, \quad \forall n = 1, \ldots, N \\
& inv_n \geq 0, \quad \forall n = 1, \ldots, N \\
& inv_0 = 0
\end{align*}

\end{document}
```

This formulation ensures that all demands are met while minimizing the costs associated with production and storage. Adjust the number of months \(N\) and the specific values in the input format to apply this model to your specific problem scenario.

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

\textbf{Objective:}

\[
\text{Minimize} \quad Z = \sum_{n=1}^{N} \left( cost\_regular \cdot reg\_quant_n + cost\_overtime \cdot over\_quant_n + store\_cost \cdot inv_n \right)
\]

\textbf{Subject to:}

\begin{align*}
& reg\_quant_n + over\_quant_n + inv_{n-1} = demand_n + inv_n, \quad \forall n = 1, \ldots, N \\
& reg\_quant_n \leq max\_regular\_amount, \quad \forall n = 1, \ldots, N \\
& reg\_quant_n \geq 0, \quad \forall n = 1, \ldots, N \\
& over\_quant_n \geq 0, \quad \forall n = 1, \ldots, N \\
& inv_n \geq 0, \quad \forall n = 1, \ldots, N \\
& inv_0 = 0
\end{align*}

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

demand = data['demand']
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']
N = len(demand)

#### Problem
problem = pulp.LpProblem("Production_Scheduling", pulp.LpMinimize)

#### Variables
reg_quant = [pulp.LpVariable(f'reg_quant_{n}', lowBound=0) for n in range(N)]
over_quant = [pulp.LpVariable(f'over_quant_{n}', lowBound=0) for n in range(N)]
inv = [pulp.LpVariable(f'inv_{n}', lowBound=0) for n in range(N)]

#### Objective Function
problem += pulp.lpSum([cost_regular * reg_quant[n] + cost_overtime * over_quant[n] + store_cost * inv[n] for n in range(N)])

#### Constraints
inv_0 = 0
for n in range(N):
    inv_prev = inv_0 if n == 0 else inv[n-1]
    problem += (reg_quant[n] + over_quant[n] + inv_prev == demand[n] + inv[n], f'Balance_{n}')
    problem += (reg_quant[n] <= max_regular_amount, f'Max_Regular_{n}')

#### Solve
problem.solve()

#### Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

