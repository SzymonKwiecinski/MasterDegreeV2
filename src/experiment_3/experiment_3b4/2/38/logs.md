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
To formulate the given problem as a linear programming model, we will define decision variables, objective function, and constraints as follows:

**Decision Variables:**
- Let \( \text{reg\_quant}_n \) be the number of units produced using regular production in month \( n \).
- Let \( \text{over\_quant}_n \) be the number of units produced using overtime production in month \( n \).
- Let \( \text{store}_n \) be the number of units stored at the end of month \( n \).

**Objective Function:**
We aim to minimize the total cost, which includes the cost of regular production, overtime production, and storage. The objective function is:

\[
\text{Minimize} \quad \sum_{n=1}^{N} \left( \text{cost\_regular} \times \text{reg\_quant}_n + \text{cost\_overtime} \times \text{over\_quant}_n + \text{store\_cost} \times \text{store}_n \right)
\]

**Constraints:**
1. **Demand Satisfaction:**
   \[
   \text{reg\_quant}_n + \text{over\_quant}_n + \text{store}_{n-1} = \text{demand}[n] + \text{store}_n \quad \text{for } n = 1, \ldots, N
   \]
   (Assuming \(\text{store}_0 = 0\)).

2. **Regular Production Limit:**
   \[
   \text{reg\_quant}_n \leq \text{max\_regular\_amount} \quad \text{for } n = 1, \ldots, N
   \]

3. **Non-negativity:**
   \[
   \text{reg\_quant}_n \geq 0, \quad \text{over\_quant}_n \geq 0, \quad \text{store}_n \geq 0 \quad \text{for } n = 1, \ldots, N
   \]

Here is the latex code for the formulated problem:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:}

\[
\text{Minimize} \quad \sum_{n=1}^{N} \left( \text{cost\_regular} \times \text{reg\_quant}_n + \text{cost\_overtime} \times \text{over\_quant}_n + \text{store\_cost} \times \text{store}_n \right)
\]

\textbf{Subject to:}

\begin{align*}
& \text{reg\_quant}_n + \text{over\_quant}_n + \text{store}_{n-1} = \text{demand}[n] + \text{store}_n, \quad n = 1, \ldots, N \\
& \text{reg\_quant}_n \leq \text{max\_regular\_amount}, \quad n = 1, \ldots, N \\
& \text{reg\_quant}_n \geq 0, \quad \text{over\_quant}_n \geq 0, \quad \text{store}_n \geq 0, \quad n = 1, \ldots, N
\end{align*}

Assuming \(\text{store}_0 = 0\).

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

\textbf{Objective:}

\[
\text{Minimize} \quad \sum_{n=1}^{N} \left( \text{cost\_regular} \times \text{reg\_quant}_n + \text{cost\_overtime} \times \text{over\_quant}_n + \text{store\_cost} \times \text{store}_n \right)
\]

\textbf{Subject to:}

\begin{align*}
& \text{reg\_quant}_n + \text{over\_quant}_n + \text{store}_{n-1} = \text{demand}[n] + \text{store}_n, \quad n = 1, \ldots, N \\
& \text{reg\_quant}_n \leq \text{max\_regular\_amount}, \quad n = 1, \ldots, N \\
& \text{reg\_quant}_n \geq 0, \quad \text{over\_quant}_n \geq 0, \quad \text{store}_n \geq 0, \quad n = 1, \ldots, N
\end{align*}

Assuming \(\text{store}_0 = 0\).

\end{document}</MATH_MODEL>
<DATA>
{'demand': [10.0, 20.0, 10.0], 'max_regular_amount': 5.0, 'cost_regular': 10.0, 'cost_overtime': 12.0, 'store_cost': 1.0}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {'demand': [10.0, 20.0, 10.0], 
        'max_regular_amount': 5.0, 
        'cost_regular': 10.0, 
        'cost_overtime': 12.0, 
        'store_cost': 1.0}

demand = data['demand']
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']
N = len(demand)

#### Problem
problem = pulp.LpProblem("Production_Planning", pulp.LpMinimize)

#### Variables
reg_quant = [pulp.LpVariable(f'reg_quant_{n}', lowBound=0) for n in range(N)]
over_quant = [pulp.LpVariable(f'over_quant_{n}', lowBound=0) for n in range(N)]
store = [pulp.LpVariable(f'store_{n}', lowBound=0) for n in range(N)]

#### Objective
problem += pulp.lpSum(
    cost_regular * reg_quant[n] + 
    cost_overtime * over_quant[n] + 
    store_cost * store[n] for n in range(N)
)

#### Constraints
for n in range(N):
    if n == 0:
        problem += reg_quant[n] + over_quant[n] + 0 == demand[n] + store[n]
    else:
        problem += reg_quant[n] + over_quant[n] + store[n-1] == demand[n] + store[n]
    problem += reg_quant[n] <= max_regular_amount

#### Solve
problem.solve()

#### Output Objective Value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

