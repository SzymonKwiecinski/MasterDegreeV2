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

\section*{Linear Programming Model for Production Schedule}

\textbf{Indices:}
\begin{itemize}
    \item $n$: month index, where $n = 1, 2, \ldots, N$.
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item $demand_{n}$: demand in month $n$.
    \item $max\_regular\_amount$: maximum units that can be produced using regular production in a month.
    \item $cost\_regular$: cost per unit of regular production.
    \item $cost\_overtime$: cost per unit of overtime production.
    \item $store\_cost$: cost per unit of storage per month.
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $reg\_quant_{n}$: quantity produced using regular production in month $n$.
    \item $over\_quant_{n}$: quantity produced using overtime production in month $n$.
    \item $inventory_{n}$: inventory carried over from month $n$ to $n+1$.
\end{itemize}

\textbf{Objective Function:}
\begin{equation}
\text{Minimize } Z = \sum_{n=1}^{N} \left( cost\_regular \cdot reg\_quant_{n} + cost\_overtime \cdot over\_quant_{n} + store\_cost \cdot inventory_{n} \right)
\end{equation}

\textbf{Constraints:}
\begin{itemize}
    \item Demand fulfillment: 
    \begin{equation}
    reg\_quant_{n} + over\_quant_{n} + inventory_{n-1} \geq demand_{n} \quad \forall n = 1, 2, \ldots, N
    \end{equation}
    
    \item Regular production capacity:
    \begin{equation}
    reg\_quant_{n} \leq max\_regular\_amount \quad \forall n = 1, 2, \ldots, N
    \end{equation}
    
    \item Inventory balance:
    \begin{equation}
    inventory_{n} = inventory_{n-1} + reg\_quant_{n} + over\_quant_{n} - demand_{n} \quad \forall n = 1, 2, \ldots, N
    \end{equation}
    
    \item Non-negativity:
    \begin{equation}
    reg\_quant_{n} \geq 0, \quad over\_quant_{n} \geq 0, \quad inventory_{n} \geq 0 \quad \forall n = 1, 2, \ldots, N
    \end{equation}
\end{itemize}

\textbf{Output:}
\begin{itemize}
    \item $reg\_quant = [reg\_quant_{1}, reg\_quant_{2}, \ldots, reg\_quant_{N}]$
    \item $over\_quant = [over\_quant_{1}, over\_quant_{2}, \ldots, over\_quant_{N}]$
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

\section*{Linear Programming Model for Production Schedule}

\textbf{Indices:}
\begin{itemize}
    \item $n$: month index, where $n = 1, 2, \ldots, N$.
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item $demand_{n}$: demand in month $n$.
    \item $max\_regular\_amount$: maximum units that can be produced using regular production in a month.
    \item $cost\_regular$: cost per unit of regular production.
    \item $cost\_overtime$: cost per unit of overtime production.
    \item $store\_cost$: cost per unit of storage per month.
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $reg\_quant_{n}$: quantity produced using regular production in month $n$.
    \item $over\_quant_{n}$: quantity produced using overtime production in month $n$.
    \item $inventory_{n}$: inventory carried over from month $n$ to $n+1$.
\end{itemize}

\textbf{Objective Function:}
\begin{equation}
\text{Minimize } Z = \sum_{n=1}^{N} \left( cost\_regular \cdot reg\_quant_{n} + cost\_overtime \cdot over\_quant_{n} + store\_cost \cdot inventory_{n} \right)
\end{equation}

\textbf{Constraints:}
\begin{itemize}
    \item Demand fulfillment: 
    \begin{equation}
    reg\_quant_{n} + over\_quant_{n} + inventory_{n-1} \geq demand_{n} \quad \forall n = 1, 2, \ldots, N
    \end{equation}
    
    \item Regular production capacity:
    \begin{equation}
    reg\_quant_{n} \leq max\_regular\_amount \quad \forall n = 1, 2, \ldots, N
    \end{equation}
    
    \item Inventory balance:
    \begin{equation}
    inventory_{n} = inventory_{n-1} + reg\_quant_{n} + over\_quant_{n} - demand_{n} \quad \forall n = 1, 2, \ldots, N
    \end{equation}
    
    \item Non-negativity:
    \begin{equation}
    reg\_quant_{n} \geq 0, \quad over\_quant_{n} \geq 0, \quad inventory_{n} \geq 0 \quad \forall n = 1, 2, \ldots, N
    \end{equation}
\end{itemize}

\textbf{Output:}
\begin{itemize}
    \item $reg\_quant = [reg\_quant_{1}, reg\_quant_{2}, \ldots, reg\_quant_{N}]$
    \item $over\_quant = [over\_quant_{1}, over\_quant_{2}, \ldots, over\_quant_{N}]$
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

#### Define the problem
problem = pulp.LpProblem("Production_Scheduling", pulp.LpMinimize)

#### Number of months
N = len(data['demand'])

#### Decision Variables
reg_quant = [pulp.LpVariable(f'reg_quant_{n}', lowBound=0) for n in range(N)]
over_quant = [pulp.LpVariable(f'over_quant_{n}', lowBound=0) for n in range(N)]
inventory = [pulp.LpVariable(f'inventory_{n}', lowBound=0) for n in range(N)]

#### Objective Function
problem += pulp.lpSum([
    data['cost_regular'] * reg_quant[n] +
    data['cost_overtime'] * over_quant[n] +
    data['store_cost'] * inventory[n] for n in range(N)
]), "Total_Cost"

#### Constraints
for n in range(N):
    #### Demand fulfillment
    if n == 0:
        problem += (reg_quant[n] + over_quant[n] >= data['demand'][n]), f"Demand_Fulfillment_{n+1}"
    else:
        problem += (reg_quant[n] + over_quant[n] + inventory[n-1] >= data['demand'][n]), f"Demand_Fulfillment_{n+1}"

    #### Regular production capacity
    problem += (reg_quant[n] <= data['max_regular_amount']), f"Regular_Production_Capacity_{n+1}"

    #### Inventory balance
    if n > 0:
        problem += (inventory[n] == inventory[n-1] + reg_quant[n] + over_quant[n] - data['demand'][n]), f"Inventory_Balance_{n+1}"
    else:
        problem += (inventory[n] == reg_quant[n] + over_quant[n] - data['demand'][n]), f"Inventory_Balance_{n+1}"

#### Solve the problem
problem.solve()

#### Output results
reg_quant_values = [pulp.value(var) for var in reg_quant]
over_quant_values = [pulp.value(var) for var in over_quant]

print(f'Regular Production Quantities: {reg_quant_values}')
print(f'Overtime Production Quantities: {over_quant_values}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

