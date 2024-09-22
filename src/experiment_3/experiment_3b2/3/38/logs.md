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
To formulate this problem as a linear programming model, we need to define decision variables, an objective function, and the constraints based on the given information. Here's the mathematical model in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Production Scheduling}

\subsection*{Decision Variables}

Let:
\begin{align*}
    \text{reg\_quant}_n & : \text{quantity of products produced using regular production in month } n, \\
    \text{over\_quant}_n & : \text{quantity of products produced using overtime production in month } n, \\
    \text{store\_quant}_n & : \text{inventory at the end of month } n.
\end{align*}

\subsection*{Objective Function}

Minimize the total cost of production and storage:
\[
\text{Minimize } \sum_{n=1}^{N} \left( \text{cost\_regular} \times \text{reg\_quant}_n + \text{cost\_overtime} \times \text{over\_quant}_n + \text{store\_cost} \times \text{store\_quant}_n \right)
\]

\subsection*{Constraints}

\begin{itemize}
    \item Production must satisfy demand and be adjusted for inventory:
    \[
    \text{reg\_quant}_n + \text{over\_quant}_n + \text{store\_quant}_{n-1} - \text{store\_quant}_n = \text{demand}_n \quad \forall n = 1, \ldots, N
    \]
    where \( \text{store\_quant}_0 = 0 \).

    \item Regular production limit:
    \[
    0 \leq \text{reg\_quant}_n \leq \text{max\_regular\_amount} \quad \forall n = 1, \ldots, N
    \]

    \item Non-negativity constraints:
    \[
    \text{reg\_quant}_n \geq 0, \quad \text{over\_quant}_n \geq 0, \quad \text{store\_quant}_n \geq 0 \quad \forall n = 1, \ldots, N
    \]
\end{itemize}

\end{document}
```

This linear programming model captures the production, overtime, and storage decisions for each month, aiming to minimize the total costs while satisfying the monthly demands without shortages.

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

\subsection*{Decision Variables}

Let:
\begin{align*}
    \text{reg\_quant}_n & : \text{quantity of products produced using regular production in month } n, \\
    \text{over\_quant}_n & : \text{quantity of products produced using overtime production in month } n, \\
    \text{store\_quant}_n & : \text{inventory at the end of month } n.
\end{align*}

\subsection*{Objective Function}

Minimize the total cost of production and storage:
\[
\text{Minimize } \sum_{n=1}^{N} \left( \text{cost\_regular} \times \text{reg\_quant}_n + \text{cost\_overtime} \times \text{over\_quant}_n + \text{store\_cost} \times \text{store\_quant}_n \right)
\]

\subsection*{Constraints}

\begin{itemize}
    \item Production must satisfy demand and be adjusted for inventory:
    \[
    \text{reg\_quant}_n + \text{over\_quant}_n + \text{store\_quant}_{n-1} - \text{store\_quant}_n = \text{demand}_n \quad \forall n = 1, \ldots, N
    \]
    where \( \text{store\_quant}_0 = 0 \).

    \item Regular production limit:
    \[
    0 \leq \text{reg\_quant}_n \leq \text{max\_regular\_amount} \quad \forall n = 1, \ldots, N
    \]

    \item Non-negativity constraints:
    \[
    \text{reg\_quant}_n \geq 0, \quad \text{over\_quant}_n \geq 0, \quad \text{store\_quant}_n \geq 0 \quad \forall n = 1, \ldots, N
    \]
\end{itemize}

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

#### Create the linear programming problem
problem = pulp.LpProblem("Production_Scheduling", pulp.LpMinimize)

#### Decision Variables
reg_quant = pulp.LpVariable.dicts("reg_quant", range(N), lowBound=0, upBound=data['max_regular_amount'])
over_quant = pulp.LpVariable.dicts("over_quant", range(N), lowBound=0)
store_quant = pulp.LpVariable.dicts("store_quant", range(N), lowBound=0)

#### Objective Function
problem += pulp.lpSum(data['cost_regular'] * reg_quant[n] + 
                       data['cost_overtime'] * over_quant[n] + 
                       data['store_cost'] * store_quant[n] for n in range(N))

#### Constraints
for n in range(N):
    if n == 0:
        problem += (reg_quant[n] + over_quant[n] - store_quant[n] == data['demand'][n])
    else:
        problem += (reg_quant[n] + over_quant[n] + store_quant[n-1] - store_quant[n] == data['demand'][n])

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

