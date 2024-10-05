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
To formulate the given problem as a Linear Programming (LP) model, we need to make decisions on the regular and overtime production quantities for each month to minimize the overall cost. Here's the LP formulation in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\section*{Linear Programming Model for Production Scheduling}

\subsection*{Sets and Parameters}
\begin{itemize}
    \item Let \( n = 1, 2, \ldots, N \) be the index for months.
    \item \text{demand}_{n}: The forecasted demand for month \( n \).
    \item \text{max\_regular\_amount}: The maximum units that can be produced using regular production in any month.
    \item \text{cost\_regular}: Cost per unit for regular production.
    \item \text{cost\_overtime}: Cost per unit for overtime production.
    \item \text{store\_cost}: Cost per unit for storing items from one month to the next.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( \text{reg\_quant}_{n} \): Quantity produced using regular production in month \( n \).
    \item \( \text{over\_quant}_{n} \): Quantity produced using overtime production in month \( n \).
    \item \( \text{store}_{n} \): Quantity stored at the end of month \( n \).
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost:
\[
\min \sum_{n=1}^{N} \left( \text{cost\_regular} \times \text{reg\_quant}_{n} + \text{cost\_overtime} \times \text{over\_quant}_{n} + \text{store\_cost} \times \text{store}_{n} \right)
\]

\subsection*{Constraints}
\begin{itemize}
    \item Demand satisfaction for each month \( n \):
    \[
    \text{reg\_quant}_{n} + \text{over\_quant}_{n} + \text{store}_{n-1} = \text{demand}_{n} + \text{store}_{n}, \quad n = 1, 2, \ldots, N
    \]
    where \( \text{store}_{0} = 0 \).

    \item Regular production limit for each month \( n \):
    \[
    \text{reg\_quant}_{n} \leq \text{max\_regular\_amount}, \quad n = 1, 2, \ldots, N
    \]

    \item Non-negativity constraints:
    \[
    \text{reg\_quant}_{n} \geq 0, \quad \text{over\_quant}_{n} \geq 0, \quad \text{store}_{n} \geq 0, \quad n = 1, 2, \ldots, N
    \]
\end{itemize}

\subsection*{Output}
The solution will provide the optimal values for:
\begin{itemize}
    \item \( \text{reg\_quant}_{n} \), the regular production quantity for each month.
    \item \( \text{over\_quant}_{n} \), the overtime production quantity for each month.
\end{itemize}

\end{document}
```

This LP model addresses the production scheduling problem by determining the optimal regular and overtime production quantities while considering storage and the associated costs to satisfy monthly demands.

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

\subsection*{Sets and Parameters}
\begin{itemize}
    \item Let \( n = 1, 2, \ldots, N \) be the index for months.
    \item \text{demand}_{n}: The forecasted demand for month \( n \).
    \item \text{max\_regular\_amount}: The maximum units that can be produced using regular production in any month.
    \item \text{cost\_regular}: Cost per unit for regular production.
    \item \text{cost\_overtime}: Cost per unit for overtime production.
    \item \text{store\_cost}: Cost per unit for storing items from one month to the next.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( \text{reg\_quant}_{n} \): Quantity produced using regular production in month \( n \).
    \item \( \text{over\_quant}_{n} \): Quantity produced using overtime production in month \( n \).
    \item \( \text{store}_{n} \): Quantity stored at the end of month \( n \).
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost:
\[
\min \sum_{n=1}^{N} \left( \text{cost\_regular} \times \text{reg\_quant}_{n} + \text{cost\_overtime} \times \text{over\_quant}_{n} + \text{store\_cost} \times \text{store}_{n} \right)
\]

\subsection*{Constraints}
\begin{itemize}
    \item Demand satisfaction for each month \( n \):
    \[
    \text{reg\_quant}_{n} + \text{over\_quant}_{n} + \text{store}_{n-1} = \text{demand}_{n} + \text{store}_{n}, \quad n = 1, 2, \ldots, N
    \]
    where \( \text{store}_{0} = 0 \).

    \item Regular production limit for each month \( n \):
    \[
    \text{reg\_quant}_{n} \leq \text{max\_regular\_amount}, \quad n = 1, 2, \ldots, N
    \]

    \item Non-negativity constraints:
    \[
    \text{reg\_quant}_{n} \geq 0, \quad \text{over\_quant}_{n} \geq 0, \quad \text{store}_{n} \geq 0, \quad n = 1, 2, \ldots, N
    \]
\end{itemize}

\subsection*{Output}
The solution will provide the optimal values for:
\begin{itemize}
    \item \( \text{reg\_quant}_{n} \), the regular production quantity for each month.
    \item \( \text{over\_quant}_{n} \), the overtime production quantity for each month.
\end{itemize}

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

N = len(data['demand'])
demand = data['demand']
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']

#### Create the linear programming problem
problem = pulp.LpProblem("Production_Scheduling", pulp.LpMinimize)

#### Decision Variables
reg_quant = [pulp.LpVariable(f'reg_quant_{n}', lowBound=0) for n in range(N)]
over_quant = [pulp.LpVariable(f'over_quant_{n}', lowBound=0) for n in range(N)]
store = [pulp.LpVariable(f'store_{n}', lowBound=0) for n in range(N)]

#### Objective Function
problem += pulp.lpSum(cost_regular * reg_quant[n] + cost_overtime * over_quant[n] + store_cost * store[n] for n in range(N))

#### Constraints
store_previous = 0
for n in range(N):
    #### Demand satisfaction constraint
    problem += reg_quant[n] + over_quant[n] + store_previous == demand[n] + store[n], f'Demand_Constraint_{n}'
    
    #### Regular production limit constraint
    problem += reg_quant[n] <= max_regular_amount, f'Regular_Production_Limit_{n}'
    
    #### Update for the next month's storage
    store_previous = store[n]

#### Solve the problem
problem.solve()

#### Output the results
for n in range(N):
    print(f'Regular production for month {n + 1}: {reg_quant[n].varValue}')
    print(f'Overtime production for month {n + 1}: {over_quant[n].varValue}')
    
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

