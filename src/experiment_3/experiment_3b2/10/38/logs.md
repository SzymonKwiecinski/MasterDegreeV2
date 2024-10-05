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
To formulate the given problem as a Linear Programming model, we will define decision variables, an objective function to minimize the total cost, and constraints to ensure the demand is satisfied and the production limits are not exceeded.

Let's denote:
- \( x_n \) as the number of units produced using regular production in month \( n \).
- \( y_n \) as the number of units produced using overtime production in month \( n \).
- \( s_n \) as the number of units stored at the end of month \( n \).

Here is the linear programming formulation:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( x_n \): Number of units produced using regular production in month \( n \).
    \item \( y_n \): Number of units produced using overtime production in month \( n \).
    \item \( s_n \): Number of units stored at the end of month \( n \).
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost:
\[
\text{Minimize} \quad \sum_{n=1}^{N} \left( \text{cost\_regular} \cdot x_n + \text{cost\_overtime} \cdot y_n + \text{store\_cost} \cdot s_n \right)
\]

\subsection*{Constraints}
\begin{align*}
    & x_n + y_n + s_{n-1} = \text{demand}_n + s_n, \quad \forall n = 1, \ldots, N \\
    & x_n \leq \text{max\_regular\_amount}, \quad \forall n = 1, \ldots, N \\
    & x_n \geq 0, \, y_n \geq 0, \, s_n \geq 0, \quad \forall n = 1, \ldots, N \\
    & s_0 = 0
\end{align*}

\subsection*{Explanation}
\begin{itemize}
    \item The first constraint ensures that the production plus the inventory from the previous month meets the demand in the current month while updating the inventory for the next month.
    \item The second constraint limits the regular production to the maximum allowed quantity.
    \item The non-negativity constraints ensure that production and storage quantities are not negative.
\end{itemize}

\end{document}
```

This formulation minimizes the total production and inventory costs while ensuring that the production and storage strategy meets the demand in each month without exceeding the regular production limits.

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
\begin{itemize}
    \item \( x_n \): Number of units produced using regular production in month \( n \).
    \item \( y_n \): Number of units produced using overtime production in month \( n \).
    \item \( s_n \): Number of units stored at the end of month \( n \).
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost:
\[
\text{Minimize} \quad \sum_{n=1}^{N} \left( \text{cost\_regular} \cdot x_n + \text{cost\_overtime} \cdot y_n + \text{store\_cost} \cdot s_n \right)
\]

\subsection*{Constraints}
\begin{align*}
    & x_n + y_n + s_{n-1} = \text{demand}_n + s_n, \quad \forall n = 1, \ldots, N \\
    & x_n \leq \text{max\_regular\_amount}, \quad \forall n = 1, \ldots, N \\
    & x_n \geq 0, \, y_n \geq 0, \, s_n \geq 0, \quad \forall n = 1, \ldots, N \\
    & s_0 = 0
\end{align*}

\subsection*{Explanation}
\begin{itemize}
    \item The first constraint ensures that the production plus the inventory from the previous month meets the demand in the current month while updating the inventory for the next month.
    \item The second constraint limits the regular production to the maximum allowed quantity.
    \item The non-negativity constraints ensure that production and storage quantities are not negative.
\end{itemize}

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

#### Extracting data from the loaded json
demand = data['demand']
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']
N = len(demand)

#### Define the problem
problem = pulp.LpProblem("Minimize_Production_Costs", pulp.LpMinimize)

#### Define decision variables
x = pulp.LpVariable.dicts("Regular_Production", range(N), lowBound=0)
y = pulp.LpVariable.dicts("Overtime_Production", range(N), lowBound=0)
s = pulp.LpVariable.dicts("Stored_Units", range(N), lowBound=0)

#### Objective function
problem += pulp.lpSum(cost_regular * x[n] + cost_overtime * y[n] + store_cost * s[n] for n in range(N))

#### Constraints
problem += s[0] == 0  #### Starting inventory is 0

for n in range(N):
    problem += x[n] + y[n] + (s[n-1] if n > 0 else 0) == demand[n] + s[n]
    problem += x[n] <= max_regular_amount  #### Maximum regular production constraint

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

