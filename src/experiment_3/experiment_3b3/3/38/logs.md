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

\section*{Production Scheduling Problem}

Let:
\begin{itemize}
    \item $N$ be the number of months,
    \item $demand_n$ be the demand in month $n$,
    \item $max\_regular\_amount$ be the maximum units produced using regular production per month,
    \item $cost\_regular$ be the cost of regular production per unit,
    \item $cost\_overtime$ be the cost of overtime production per unit,
    \item $store\_cost$ be the storage cost per unit per month.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $reg\_quant_n$: quantity produced using regular production in month $n$,
    \item $over\_quant_n$: quantity produced using overtime production in month $n$,
    \item $inventory_n$: inventory at the end of month $n$.
\end{itemize}

\subsection*{Objective Function}
The objective is to minimize the total cost, which includes production and storage costs:
\[
\text{Minimize } Z = \sum_{n=1}^{N} \left( cost\_regular \cdot reg\_quant_n + cost\_overtime \cdot over\_quant_n + store\_cost \cdot inventory_n \right)
\]

\subsection*{Constraints}

1. **Demand Satisfaction:**
   For each month $n$, the sum of regular and overtime production plus the inventory from the previous month must satisfy the demand:
   \[
   reg\_quant_n + over\_quant_n + inventory_{n-1} - inventory_n = demand_n, \quad n = 1, 2, \ldots, N
   \]
   (where $inventory_0 = 0$)

2. **Regular Production Limit:**
   The quantity produced using regular production must not exceed the maximum regular amount:
   \[
   reg\_quant_n \leq max\_regular\_amount, \quad n = 1, 2, \ldots, N
   \]

3. **Non-negativity:**
   All quantities must be non-negative:
   \[
   reg\_quant_n \geq 0, \quad over\_quant_n \geq 0, \quad inventory_n \geq 0, \quad n = 1, 2, \ldots, N
   \]

\subsection*{Output}
\textit{The output will include the quantities produced using regular and overtime production for each month:}
\begin{align*}
    \text{Output:} \\
    \{ \\
    \quad "reg\_quant": [reg\_quant_1, reg\_quant_2, \ldots, reg\_quant_N], \\
    \quad "over\_quant": [over\_quant_1, over\_quant_2, \ldots, over\_quant_N] \\
    \}
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

\section*{Production Scheduling Problem}

Let:
\begin{itemize}
    \item $N$ be the number of months,
    \item $demand_n$ be the demand in month $n$,
    \item $max\_regular\_amount$ be the maximum units produced using regular production per month,
    \item $cost\_regular$ be the cost of regular production per unit,
    \item $cost\_overtime$ be the cost of overtime production per unit,
    \item $store\_cost$ be the storage cost per unit per month.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $reg\_quant_n$: quantity produced using regular production in month $n$,
    \item $over\_quant_n$: quantity produced using overtime production in month $n$,
    \item $inventory_n$: inventory at the end of month $n$.
\end{itemize}

\subsection*{Objective Function}
The objective is to minimize the total cost, which includes production and storage costs:
\[
\text{Minimize } Z = \sum_{n=1}^{N} \left( cost\_regular \cdot reg\_quant_n + cost\_overtime \cdot over\_quant_n + store\_cost \cdot inventory_n \right)
\]

\subsection*{Constraints}

1. **Demand Satisfaction:**
   For each month $n$, the sum of regular and overtime production plus the inventory from the previous month must satisfy the demand:
   \[
   reg\_quant_n + over\_quant_n + inventory_{n-1} - inventory_n = demand_n, \quad n = 1, 2, \ldots, N
   \]
   (where $inventory_0 = 0$)

2. **Regular Production Limit:**
   The quantity produced using regular production must not exceed the maximum regular amount:
   \[
   reg\_quant_n \leq max\_regular\_amount, \quad n = 1, 2, \ldots, N
   \]

3. **Non-negativity:**
   All quantities must be non-negative:
   \[
   reg\_quant_n \geq 0, \quad over\_quant_n \geq 0, \quad inventory_n \geq 0, \quad n = 1, 2, \ldots, N
   \]

\subsection*{Output}
\textit{The output will include the quantities produced using regular and overtime production for each month:}
\begin{align*}
    \text{Output:} \\
    \{ \\
    \quad "reg\_quant": [reg\_quant_1, reg\_quant_2, \ldots, reg\_quant_N], \\
    \quad "over\_quant": [over\_quant_1, over\_quant_2, \ldots, over\_quant_N] \\
    \}
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'demand': [10.0, 20.0, 10.0], 'max_regular_amount': 5.0, 'cost_regular': 10.0, 'cost_overtime': 12.0, 'store_cost': 1.0}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Extract data from the provided JSON structure
data = {
    'demand': [10.0, 20.0, 10.0],
    'max_regular_amount': 5.0,
    'cost_regular': 10.0,
    'cost_overtime': 12.0,
    'store_cost': 1.0
}

#### Define problem
problem = pulp.LpProblem("Production_Scheduling_Problem", pulp.LpMinimize)

#### Number of months
N = len(data['demand'])

#### Decision Variables
reg_quant = [pulp.LpVariable(f"reg_quant_{n+1}", lowBound=0, cat='Continuous') for n in range(N)]
over_quant = [pulp.LpVariable(f"over_quant_{n+1}", lowBound=0, cat='Continuous') for n in range(N)]
inventory = [pulp.LpVariable(f"inventory_{n+1}", lowBound=0, cat='Continuous') for n in range(N)]

#### Objective Function
problem += pulp.lpSum([
    data['cost_regular'] * reg_quant[n] +
    data['cost_overtime'] * over_quant[n] +
    data['store_cost'] * inventory[n]
    for n in range(N)
])

#### Constraints

#### Initial inventory
inventory_0 = 0

#### Demand Satisfaction Constraint
for n in range(N):
    if n == 0:
        inventory_prev = inventory_0
    else:
        inventory_prev = inventory[n-1]

    problem += (reg_quant[n] + over_quant[n] + inventory_prev - inventory[n] == data['demand'][n])

#### Regular Production Limit Constraint
for n in range(N):
    problem += (reg_quant[n] <= data['max_regular_amount'])

#### Solve the problem
problem.solve()

#### Output Results
reg_result = [pulp.value(reg_quant[n]) for n in range(N)]
over_result = [pulp.value(over_quant[n]) for n in range(N)]

output = {
    "reg_quant": reg_result,
    "over_quant": over_result
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

