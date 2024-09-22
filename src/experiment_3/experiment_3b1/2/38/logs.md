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

\section*{Linear Programming Formulation}

Given the input parameters:

\begin{itemize}
    \item Demand for each month: \(demand_n\) for \(n = 1, \ldots, N\)
    \item Maximum regular production per month: \(max\_regular\_amount\)
    \item Cost of regular production per unit: \(cost\_regular\)
    \item Cost of overtime production per unit: \(cost\_overtime\)
    \item Storage cost per unit per month: \(store\_cost\)
\end{itemize}

Let:
\begin{itemize}
    \item \(reg\_quant_n\) = quantity produced using regular production in month \(n\)
    \item \(over\_quant_n\) = quantity produced using overtime production in month \(n\)
    \item \(inventory_n\) = inventory at the end of month \(n\)
\end{itemize}

The objective is to minimize the total cost given by:

\[
\text{Minimize: } Z = \sum_{n=1}^{N} \left( cost\_regular \cdot reg\_quant_n + cost\_overtime \cdot over\_quant_n + store\_cost \cdot inventory_n \right)
\]

Subject to the following constraints:

1. **Demand Satisfaction** (for each month):
\[
reg\_quant_n + over\_quant_n + inventory_{n-1} \geq demand_n \quad \forall n = 1, \ldots, N
\]

2. **Regular Production Limits**:
\[
reg\_quant_n \leq max\_regular\_amount \quad \forall n = 1, \ldots, N
\]

3. **Inventory Balance** (for each month):
\[
inventory_n = inventory_{n-1} + reg\_quant_n + over\_quant_n - demand_n \quad \forall n = 1, \ldots, N
\]

4. **Non-negativity**:
\[
reg\_quant_n \geq 0, \quad over\_quant_n \geq 0, \quad inventory_n \geq 0 \quad \forall n = 1, \ldots, N
\]

The output will yield the quantities produced each month:

\begin{itemize}
    \item \texttt{"reg\_quant": } [\(reg\_quant_1, reg\_quant_2, \ldots, reg\_quant_N\)]
    \item \texttt{"over\_quant": } [\(over\_quant_1, over\_quant_2, \ldots, over\_quant_N\)]
\end{itemize}

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

\section*{Linear Programming Formulation}

Given the input parameters:

\begin{itemize}
    \item Demand for each month: \(demand_n\) for \(n = 1, \ldots, N\)
    \item Maximum regular production per month: \(max\_regular\_amount\)
    \item Cost of regular production per unit: \(cost\_regular\)
    \item Cost of overtime production per unit: \(cost\_overtime\)
    \item Storage cost per unit per month: \(store\_cost\)
\end{itemize}

Let:
\begin{itemize}
    \item \(reg\_quant_n\) = quantity produced using regular production in month \(n\)
    \item \(over\_quant_n\) = quantity produced using overtime production in month \(n\)
    \item \(inventory_n\) = inventory at the end of month \(n\)
\end{itemize}

The objective is to minimize the total cost given by:

\[
\text{Minimize: } Z = \sum_{n=1}^{N} \left( cost\_regular \cdot reg\_quant_n + cost\_overtime \cdot over\_quant_n + store\_cost \cdot inventory_n \right)
\]

Subject to the following constraints:

1. **Demand Satisfaction** (for each month):
\[
reg\_quant_n + over\_quant_n + inventory_{n-1} \geq demand_n \quad \forall n = 1, \ldots, N
\]

2. **Regular Production Limits**:
\[
reg\_quant_n \leq max\_regular\_amount \quad \forall n = 1, \ldots, N
\]

3. **Inventory Balance** (for each month):
\[
inventory_n = inventory_{n-1} + reg\_quant_n + over\_quant_n - demand_n \quad \forall n = 1, \ldots, N
\]

4. **Non-negativity**:
\[
reg\_quant_n \geq 0, \quad over\_quant_n \geq 0, \quad inventory_n \geq 0 \quad \forall n = 1, \ldots, N
\]

The output will yield the quantities produced each month:

\begin{itemize}
    \item \texttt{"reg\_quant": } [\(reg\_quant_1, reg\_quant_2, \ldots, reg\_quant_N\)]
    \item \texttt{"over\_quant": } [\(over\_quant_1, over\_quant_2, \ldots, over\_quant_N\)]
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'demand': [10.0, 20.0, 10.0], 'max_regular_amount': 5.0, 'cost_regular': 10.0, 'cost_overtime': 12.0, 'store_cost': 1.0}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the provided JSON format
data = {
    'demand': [10.0, 20.0, 10.0],
    'max_regular_amount': 5.0,
    'cost_regular': 10.0,
    'cost_overtime': 12.0,
    'store_cost': 1.0
}

N = len(data['demand'])  #### Number of months
demand = data['demand']
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']

#### Create the linear programming problem
problem = pulp.LpProblem("Production_Cost_Minimization", pulp.LpMinimize)

#### Define decision variables
reg_quant = pulp.LpVariable.dicts("reg_quant", range(N), lowBound=0)
over_quant = pulp.LpVariable.dicts("over_quant", range(N), lowBound=0)
inventory = pulp.LpVariable.dicts("inventory", range(N), lowBound=0)

#### Objective function
problem += pulp.lpSum(cost_regular * reg_quant[n] + cost_overtime * over_quant[n] + store_cost * inventory[n] for n in range(N))

#### Constraints

#### Demand satisfaction and inventory balance
for n in range(N):
    if n == 0:
        problem += reg_quant[n] + over_quant[n] >= demand[n], f"Demand_Satisfaction_{n}"
        problem += inventory[n] == reg_quant[n] + over_quant[n] - demand[n], f"Inventory_Balance_{n}"
    else:
        problem += reg_quant[n] + over_quant[n] + inventory[n-1] >= demand[n], f"Demand_Satisfaction_{n}"
        problem += inventory[n] == inventory[n-1] + reg_quant[n] + over_quant[n] - demand[n], f"Inventory_Balance_{n}"
    
    #### Regular production limits
    problem += reg_quant[n] <= max_regular_amount, f"Regular_Production_Limit_{n}"

#### Solve the problem
problem.solve()

#### Output the results
reg_quant_values = [reg_quant[n].varValue for n in range(N)]
over_quant_values = [over_quant[n].varValue for n in range(N)]

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(f'Regular production quantities: {reg_quant_values}')
print(f'Overtime production quantities: {over_quant_values}')
```

