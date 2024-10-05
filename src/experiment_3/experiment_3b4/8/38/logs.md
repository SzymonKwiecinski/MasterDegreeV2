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
To formulate this problem as a Linear Programming model, we need to define decision variables, an objective function, and constraints based on the provided information.

Let:
- \( \text{reg\_quant}_n \) be the regular production quantity in month \( n \)
- \( \text{over\_quant}_n \) be the overtime production quantity in month \( n \)
- \( \text{store}_n \) be the number of units stored at the end of month \( n \)

Objective:
Minimize the total cost, which includes the cost of regular production, overtime production, and storage.

Constraints:
1. Demand satisfaction: The sum of regular production, overtime production, and the inventory carried from the previous month must meet the demand for each month.
2. Production limits: Regular production cannot exceed the maximum regular production capacity.
3. Inventory balance: Inventory should carry over from one month to the next month.
4. Non-negativity: All variables should be non-negative.

Here is the complete linear programming model in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\subsection*{Decision Variables}
\begin{align*}
\text{reg\_quant}_n &: \text{Regular production quantity in month } n \\
\text{over\_quant}_n &: \text{Overtime production quantity in month } n \\
\text{store}_n &: \text{Number of units stored at the end of month } n
\end{align*}

\subsection*{Objective Function}
Minimize the total cost:
\[
\min \sum_{n=1}^{N} \left( \text{cost\_regular} \times \text{reg\_quant}_n + \text{cost\_overtime} \times \text{over\_quant}_n + \text{store\_cost} \times \text{store}_n \right)
\]

\subsection*{Constraints}

\begin{align*}
\text{reg\_quant}_n + \text{over\_quant}_n + \text{store}_{n-1} - \text{store}_n &= \text{demand}_{n}, \quad \forall n = 1, \ldots, N \\
\text{reg\_quant}_n &\leq \text{max\_regular\_amount}, \quad \forall n = 1, \ldots, N \\
\text{reg\_quant}_n, \text{over\_quant}_n, \text{store}_n &\geq 0, \quad \forall n = 1, \ldots, N \\
\text{store}_0 &= 0
\end{align*}

\end{document}
```

This model will help in determining the production schedule that minimizes the total cost, considering regular and overtime production costs as well as storage costs while meeting the demand constraints for each month.

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

\subsection*{Decision Variables}
\begin{align*}
\text{reg\_quant}_n &: \text{Regular production quantity in month } n \\
\text{over\_quant}_n &: \text{Overtime production quantity in month } n \\
\text{store}_n &: \text{Number of units stored at the end of month } n
\end{align*}

\subsection*{Objective Function}
Minimize the total cost:
\[
\min \sum_{n=1}^{N} \left( \text{cost\_regular} \times \text{reg\_quant}_n + \text{cost\_overtime} \times \text{over\_quant}_n + \text{store\_cost} \times \text{store}_n \right)
\]

\subsection*{Constraints}

\begin{align*}
\text{reg\_quant}_n + \text{over\_quant}_n + \text{store}_{n-1} - \text{store}_n &= \text{demand}_{n}, \quad \forall n = 1, \ldots, N \\
\text{reg\_quant}_n &\leq \text{max\_regular\_amount}, \quad \forall n = 1, \ldots, N \\
\text{reg\_quant}_n, \text{over\_quant}_n, \text{store}_n &\geq 0, \quad \forall n = 1, \ldots, N \\
\text{store}_0 &= 0
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'demand': [10.0, 20.0, 10.0], 'max_regular_amount': 5.0, 'cost_regular': 10.0, 'cost_overtime': 12.0, 'store_cost': 1.0}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data provided
data = {
    'demand': [10.0, 20.0, 10.0],
    'max_regular_amount': 5.0,
    'cost_regular': 10.0,
    'cost_overtime': 12.0,
    'store_cost': 1.0
}

#### Number of periods
N = len(data['demand'])

#### Create a Linear Programming problem
problem = pulp.LpProblem("Production_Planning", pulp.LpMinimize)

#### Define decision variables
reg_quant = [pulp.LpVariable(f'reg_quant_{n}', lowBound=0, cat='Continuous') for n in range(N)]
over_quant = [pulp.LpVariable(f'over_quant_{n}', lowBound=0, cat='Continuous') for n in range(N)]
store = [pulp.LpVariable(f'store_{n}', lowBound=0, cat='Continuous') for n in range(N)]

#### Objective Function
total_cost = pulp.lpSum(
    data['cost_regular'] * reg_quant[n] + 
    data['cost_overtime'] * over_quant[n] +
    data['store_cost'] * store[n] 
    for n in range(N)
)

problem += total_cost

#### Constraints
#### Storage initial condition
problem += store[0] == 0

#### Demand and production constraints
for n in range(N):
    problem += reg_quant[n] <= data['max_regular_amount']
    if n == 0:
        problem += reg_quant[n] + over_quant[n] - store[n] == data['demand'][n]
    else:
        problem += reg_quant[n] + over_quant[n] + store[n-1] - store[n] == data['demand'][n]

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```


