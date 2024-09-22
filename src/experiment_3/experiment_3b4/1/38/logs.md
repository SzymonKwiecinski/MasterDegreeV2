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
To formulate the problem of determining the production schedule that minimizes the cost, we will create a linear programming model. The objective is to minimize the total production and storage cost over the N months while meeting the demand each month.

######### Objective Function:
We aim to minimize the total cost, which includes:
- Regular production cost
- Overtime production cost
- Storage cost

######### Constraints:
1. Regular production should not exceed the maximum regular production capacity.
2. The demand for each month must be met by the sum of regular production, overtime production, and any stored units from the previous month.
3. Non-negativity constraints: Regular production, overtime production, and storage must be non-negative.

Below is the mathematical model in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model}

\subsection*{Given Parameters:}
\begin{itemize}
    \item $N$: Number of months
    \item $\text{demand}_n$: Demand in month $n$, for $n = 1, \ldots, N$
    \item $\text{max\_regular\_amount}$: Maximum regular production capacity per month
    \item $\text{cost\_regular}$: Cost per unit in regular production
    \item $\text{cost\_overtime}$: Cost per unit in overtime production
    \item $\text{store\_cost}$: Storage cost per unit per month
\end{itemize}

\subsection*{Decision Variables:}
\begin{itemize}
    \item $\text{reg\_quant}_n$: Quantity produced using regular production in month $n$
    \item $\text{over\_quant}_n$: Quantity produced using overtime production in month $n$
    \item $\text{store}_n$: Number of units stored at the end of month $n$
\end{itemize}

\subsection*{Objective Function:}
Minimize the total cost:
\[
\text{Minimize } \sum_{n=1}^{N} \left( \text{cost\_regular} \times \text{reg\_quant}_n + \text{cost\_overtime} \times \text{over\_quant}_n + \text{store\_cost} \times \text{store}_n \right)
\]

\subsection*{Constraints:}
\begin{align}
    & \text{reg\_quant}_n \leq \text{max\_regular\_amount}, \quad n = 1, \ldots, N \\
    & \text{reg\_quant}_n + \text{over\_quant}_n + \text{store}_{n-1} = \text{demand}_n + \text{store}_n, \quad n = 1, \ldots, N \\
    & \text{store}_0 = 0 \\
    & \text{reg\_quant}_n \geq 0, \quad n = 1, \ldots, N \\
    & \text{over\_quant}_n \geq 0, \quad n = 1, \ldots, N \\
    & \text{store}_n \geq 0, \quad n = 1, \ldots, N
\end{align}

\end{document}
```

This linear program will determine the optimal quantities `reg_quant_n`, `over_quant_n`, and `store_n` for each month to minimize the overall cost while satisfying all constraints.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model}

\subsection*{Given Parameters:}
\begin{itemize}
    \item $N$: Number of months
    \item $\text{demand}_n$: Demand in month $n$, for $n = 1, \ldots, N$
    \item $\text{max\_regular\_amount}$: Maximum regular production capacity per month
    \item $\text{cost\_regular}$: Cost per unit in regular production
    \item $\text{cost\_overtime}$: Cost per unit in overtime production
    \item $\text{store\_cost}$: Storage cost per unit per month
\end{itemize}

\subsection*{Decision Variables:}
\begin{itemize}
    \item $\text{reg\_quant}_n$: Quantity produced using regular production in month $n$
    \item $\text{over\_quant}_n$: Quantity produced using overtime production in month $n$
    \item $\text{store}_n$: Number of units stored at the end of month $n$
\end{itemize}

\subsection*{Objective Function:}
Minimize the total cost:
\[
\text{Minimize } \sum_{n=1}^{N} \left( \text{cost\_regular} \times \text{reg\_quant}_n + \text{cost\_overtime} \times \text{over\_quant}_n + \text{store\_cost} \times \text{store}_n \right)
\]

\subsection*{Constraints:}
\begin{align}
    & \text{reg\_quant}_n \leq \text{max\_regular\_amount}, \quad n = 1, \ldots, N \\
    & \text{reg\_quant}_n + \text{over\_quant}_n + \text{store}_{n-1} = \text{demand}_n + \text{store}_n, \quad n = 1, \ldots, N \\
    & \text{store}_0 = 0 \\
    & \text{reg\_quant}_n \geq 0, \quad n = 1, \ldots, N \\
    & \text{over\_quant}_n \geq 0, \quad n = 1, \ldots, N \\
    & \text{store}_n \geq 0, \quad n = 1, \ldots, N
\end{align}

\end{document}</MATH_MODEL>
<DATA>
{'demand': [10.0, 20.0, 10.0], 'max_regular_amount': 5.0, 'cost_regular': 10.0, 'cost_overtime': 12.0, 'store_cost': 1.0}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON
data = {
    'demand': [10.0, 20.0, 10.0],
    'max_regular_amount': 5.0,
    'cost_regular': 10.0,
    'cost_overtime': 12.0,
    'store_cost': 1.0
}

#### Parameters
N = len(data['demand'])
demand = data['demand']
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']

#### Problem
problem = pulp.LpProblem("ProductionPlanning", pulp.LpMinimize)

#### Decision Variables
reg_quant = pulp.LpVariable.dicts("reg_quant", range(N), lowBound=0, cat='Continuous')
over_quant = pulp.LpVariable.dicts("over_quant", range(N), lowBound=0, cat='Continuous')
store = pulp.LpVariable.dicts("store", range(N), lowBound=0, cat='Continuous')

#### Objective Function
problem += pulp.lpSum([
    cost_regular * reg_quant[n] + 
    cost_overtime * over_quant[n] + 
    store_cost * store[n] 
    for n in range(N)
])

#### Constraints
for n in range(N):
    problem += reg_quant[n] <= max_regular_amount
    if n == 0:
        problem += reg_quant[n] + over_quant[n] == demand[n] + store[n]
    else:
        problem += reg_quant[n] + over_quant[n] + store[n-1] == demand[n] + store[n]

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

