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
To formulate the given problem as a Linear Programming (LP) model, we need to define the decision variables, objective function, and constraints in mathematical form. Let's denote:

- \( \text{reg\_quant}_n \): the quantity of products produced using regular production in month \( n \).
- \( \text{over\_quant}_n \): the quantity of products produced using overtime production in month \( n \).
- \( \text{store\_quant}_n \): the inventory (store) at the end of month \( n \).

We aim to minimize the total cost, which includes the regular production cost, overtime production cost, and storage cost.

Here's the formulation in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective: Minimize Total Cost}

\[
\begin{align*}
\text{Minimize } Z = & \sum_{n=1}^{N} \left( \text{cost\_regular} \cdot \text{reg\_quant}_n + \text{cost\_overtime} \cdot \text{over\_quant}_n + \text{store\_cost} \cdot \text{store\_quant}_n \right)
\end{align*}
\]

\textbf{Subject to constraints:}

1. \textbf{Demand Satisfaction:}
\[
\forall n: \quad \text{reg\_quant}_n + \text{over\_quant}_n + \text{store\_quant}_{n-1} = \text{demand}_n + \text{store\_quant}_n
\]

Where \(\text{store\_quant}_0 = 0\).

2. \textbf{Regular Production Limit:}
\[
\forall n: \quad \text{reg\_quant}_n \leq \text{max\_regular\_amount}
\]

3. \textbf{Non-negativity:}
\[
\forall n: \quad \text{reg\_quant}_n \geq 0, \quad \text{over\_quant}_n \geq 0, \quad \text{store\_quant}_n \geq 0
\]

\end{document}
```

This LP model finds the optimal monthly production numbers under the given constraints to minimize the overall cost. The constraints ensure that demand is completely satisfied without backorders, while respecting the production limits and inventory management.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective: Minimize Total Cost}

\[
\begin{align*}
\text{Minimize } Z = & \sum_{n=1}^{N} \left( \text{cost\_regular} \cdot \text{reg\_quant}_n + \text{cost\_overtime} \cdot \text{over\_quant}_n + \text{store\_cost} \cdot \text{store\_quant}_n \right)
\end{align*}
\]

\textbf{Subject to constraints:}

1. \textbf{Demand Satisfaction:}
\[
\forall n: \quad \text{reg\_quant}_n + \text{over\_quant}_n + \text{store\_quant}_{n-1} = \text{demand}_n + \text{store\_quant}_n
\]

Where \(\text{store\_quant}_0 = 0\).

2. \textbf{Regular Production Limit:}
\[
\forall n: \quad \text{reg\_quant}_n \leq \text{max\_regular\_amount}
\]

3. \textbf{Non-negativity:}
\[
\forall n: \quad \text{reg\_quant}_n \geq 0, \quad \text{over\_quant}_n \geq 0, \quad \text{store\_quant}_n \geq 0
\]

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

#### Variables
N = len(data['demand'])
demand = data['demand']
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']

#### Problem
problem = pulp.LpProblem("Minimize_Total_Cost", pulp.LpMinimize)

#### Decision Variables
reg_quant = pulp.LpVariable.dicts("Regular_Quantity", range(N), lowBound=0, cat='Continuous')
over_quant = pulp.LpVariable.dicts("Overtime_Quantity", range(N), lowBound=0, cat='Continuous')
store_quant = pulp.LpVariable.dicts("Storage_Quantity", range(N), lowBound=0, cat='Continuous')

#### Objective
problem += pulp.lpSum([
    cost_regular * reg_quant[n] + 
    cost_overtime * over_quant[n] + 
    store_cost * store_quant[n] for n in range(N)
])

#### Constraints
for n in range(N):
    if n == 0:
        store_quant_prev = 0
    else:
        store_quant_prev = store_quant[n-1]
    
    #### Demand Satisfaction
    problem += reg_quant[n] + over_quant[n] + store_quant_prev == demand[n] + store_quant[n]
    
    #### Regular Production Limit
    problem += reg_quant[n] <= max_regular_amount

#### Solve
problem.solve()

#### Output
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

