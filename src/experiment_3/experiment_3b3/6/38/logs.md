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

\title{Linear Programming Model for Production Scheduling}
\author{}
\date{}
\maketitle

\section*{Problem Formulation}

Given the input parameters:
\begin{itemize}
    \item Demand over \textit{n}-th month: \(demand_n\) for \(n = 1, \ldots, N\)
    \item Maximum regular production capacity per month: \(max\_regular\_amount\)
    \item Cost of regular production per unit: \(cost\_regular\)
    \item Cost of overtime production per unit: \(cost\_overtime\)
    \item Storage cost per unit per month: \(store\_cost\)
\end{itemize}

\subsection*{Variables}

Let:
\begin{itemize}
    \item \(reg\_quant_n\): Quantity of products produced using regular production in month \(n\)
    \item \(over\_quant_n\): Quantity of products produced using overtime production in month \(n\)
    \item \(inventory_n\): Inventory at the end of month \(n\)
\end{itemize}

\subsection*{Objective Function}

The objective is to minimize the total cost, which includes regular production costs, overtime production costs, and storage costs:

\[
\text{Minimize } Z = \sum_{n=1}^{N} (cost\_regular \cdot reg\_quant_n + cost\_overtime \cdot over\_quant_n + store\_cost \cdot inventory_n)
\]

\subsection*{Constraints}

The constraints for the problem are:

1. **Demand Satisfaction:**
   \[
   inventory_{n-1} + reg\_quant_n + over\_quant_n \geq demand_n \quad \forall n = 1, \ldots, N
   \]

2. **Regular Production Limit:**
   \[
   reg\_quant_n \leq max\_regular\_amount \quad \forall n = 1, \ldots, N
   \]

3. **Inventory Balance:**
   \[
   inventory_n = inventory_{n-1} + reg\_quant_n + over\_quant_n - demand_n \quad \forall n = 1, \ldots, N
   \]

4. **Non-negativity:**
   \[
   reg\_quant_n \geq 0, \quad over\_quant_n \geq 0, \quad inventory_n \geq 0 \quad \forall n = 1, \ldots, N
   \]

5. **Initial Inventory:**
   \[
   inventory_0 = 0
\end{itemize}

\subsection*{Output}

The output is in the following format:
\begin{verbatim}
{
    "reg_quant": [reg_quant_{n} for n in 1,...,N],
    "over_quant": [over_quant_{n} for n in 1,...,N]
}
\end{verbatim}

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

\title{Linear Programming Model for Production Scheduling}
\author{}
\date{}
\maketitle

\section*{Problem Formulation}

Given the input parameters:
\begin{itemize}
    \item Demand over \textit{n}-th month: \(demand_n\) for \(n = 1, \ldots, N\)
    \item Maximum regular production capacity per month: \(max\_regular\_amount\)
    \item Cost of regular production per unit: \(cost\_regular\)
    \item Cost of overtime production per unit: \(cost\_overtime\)
    \item Storage cost per unit per month: \(store\_cost\)
\end{itemize}

\subsection*{Variables}

Let:
\begin{itemize}
    \item \(reg\_quant_n\): Quantity of products produced using regular production in month \(n\)
    \item \(over\_quant_n\): Quantity of products produced using overtime production in month \(n\)
    \item \(inventory_n\): Inventory at the end of month \(n\)
\end{itemize}

\subsection*{Objective Function}

The objective is to minimize the total cost, which includes regular production costs, overtime production costs, and storage costs:

\[
\text{Minimize } Z = \sum_{n=1}^{N} (cost\_regular \cdot reg\_quant_n + cost\_overtime \cdot over\_quant_n + store\_cost \cdot inventory_n)
\]

\subsection*{Constraints}

The constraints for the problem are:

1. **Demand Satisfaction:**
   \[
   inventory_{n-1} + reg\_quant_n + over\_quant_n \geq demand_n \quad \forall n = 1, \ldots, N
   \]

2. **Regular Production Limit:**
   \[
   reg\_quant_n \leq max\_regular\_amount \quad \forall n = 1, \ldots, N
   \]

3. **Inventory Balance:**
   \[
   inventory_n = inventory_{n-1} + reg\_quant_n + over\_quant_n - demand_n \quad \forall n = 1, \ldots, N
   \]

4. **Non-negativity:**
   \[
   reg\_quant_n \geq 0, \quad over\_quant_n \geq 0, \quad inventory_n \geq 0 \quad \forall n = 1, \ldots, N
   \]

5. **Initial Inventory:**
   \[
   inventory_0 = 0
\end{itemize}

\subsection*{Output}

The output is in the following format:
\begin{verbatim}
{
    "reg_quant": [reg_quant_{n} for n in 1,...,N],
    "over_quant": [over_quant_{n} for n in 1,...,N]
}
\end{verbatim}

\end{document}</MATH_MODEL>
<DATA>
{'demand': [10.0, 20.0, 10.0], 'max_regular_amount': 5.0, 'cost_regular': 10.0, 'cost_overtime': 12.0, 'store_cost': 1.0}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Input data
data = {
    'demand': [10.0, 20.0, 10.0],
    'max_regular_amount': 5.0,
    'cost_regular': 10.0,
    'cost_overtime': 12.0,
    'store_cost': 1.0
}

#### Parameters
demand = data['demand']
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']
N = len(demand)

#### Problem
problem = pulp.LpProblem("Production_Scheduling", pulp.LpMinimize)

#### Variables
reg_quant = [pulp.LpVariable(f"reg_quant_{n}", lowBound=0) for n in range(N)]
over_quant = [pulp.LpVariable(f"over_quant_{n}", lowBound=0) for n in range(N)]
inventory = [pulp.LpVariable(f"inventory_{n}", lowBound=0) for n in range(N)]

#### Objective Function
problem += pulp.lpSum(
    cost_regular * reg_quant[n] +
    cost_overtime * over_quant[n] +
    store_cost * inventory[n]
    for n in range(N)
), "Total Cost"

#### Constraints
#### Initial Inventory
problem += inventory[0] == 0, "Initial Inventory"

#### Demand satisfaction and inventory balance
for n in range(N):
    if n == 0:
        prev_inventory = 0
    else:
        prev_inventory = inventory[n-1]
    
    problem += prev_inventory + reg_quant[n] + over_quant[n] >= demand[n], f"Demand Satisfaction Month {n+1}"
    problem += inventory[n] == prev_inventory + reg_quant[n] + over_quant[n] - demand[n], f"Inventory Balance Month {n+1}"

#### Regular Production Limit
for n in range(N):
    problem += reg_quant[n] <= max_regular_amount, f"Regular Production Limit Month {n+1}"

#### Solve the problem
problem.solve()

#### Output results
output = {
    "reg_quant": [pulp.value(reg_quant[n]) for n in range(N)],
    "over_quant": [pulp.value(over_quant[n]) for n in range(N)]
}

print("Output:", output)
print(f" (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")
```

