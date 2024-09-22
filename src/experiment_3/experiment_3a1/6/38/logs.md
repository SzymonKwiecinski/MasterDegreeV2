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

\section*{Linear Programming Model for Production Scheduling}

\textbf{Parameters:}
\begin{itemize}
    \item $N$: Total number of months
    \item $demand_{n}$: Demand in month $n$, for $n = 1, 2, \ldots, N$
    \item $max\_regular\_amount$: Maximum regular production capacity per month
    \item $cost\_regular$: Cost of producing one unit using regular production
    \item $cost\_overtime$: Cost of producing one unit using overtime production
    \item $store\_cost$: Cost of storing one unit for one month
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $reg\_quant_{n}$: Quantity produced using regular production in month $n$
    \item $over\_quant_{n}$: Quantity produced using overtime production in month $n$
    \item $inventory_{n}$: Inventory carried over to month $n$
\end{itemize}

\textbf{Objective Function:}
\[
\text{Minimize } Z = \sum_{n=1}^{N} \left( cost\_regular \cdot reg\_quant_{n} + cost\_overtime \cdot over\_quant_{n} + store\_cost \cdot inventory_{n} \right)
\]

\textbf{Subject to:}
\begin{itemize}
    \item Production Constraints:
    \[
    reg\_quant_{n} + over\_quant_{n} + inventory_{n-1} \geq demand_{n} \quad \forall n = 1, \ldots, N
    \]
    
    \item Regular Production Capacity:
    \[
    reg\_quant_{n} \leq max\_regular\_amount \quad \forall n = 1, \ldots, N
    \]

    \item Inventory Balance:
    \[
    inventory_{n} = inventory_{n-1} + reg\_quant_{n} + over\_quant_{n} - demand_{n} \quad \forall n = 1, \ldots, N
    \]
    
    \item Non-negativity Constraints:
    \[
    reg\_quant_{n} \geq 0, \quad over\_quant_{n} \geq 0, \quad inventory_{n} \geq 0 \quad \forall n = 1, \ldots, N
    \]
\end{itemize}

\textbf{Output:}
The solution will yield the quantities of products produced using regular and overtime production for each month:
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

\section*{Linear Programming Model for Production Scheduling}

\textbf{Parameters:}
\begin{itemize}
    \item $N$: Total number of months
    \item $demand_{n}$: Demand in month $n$, for $n = 1, 2, \ldots, N$
    \item $max\_regular\_amount$: Maximum regular production capacity per month
    \item $cost\_regular$: Cost of producing one unit using regular production
    \item $cost\_overtime$: Cost of producing one unit using overtime production
    \item $store\_cost$: Cost of storing one unit for one month
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $reg\_quant_{n}$: Quantity produced using regular production in month $n$
    \item $over\_quant_{n}$: Quantity produced using overtime production in month $n$
    \item $inventory_{n}$: Inventory carried over to month $n$
\end{itemize}

\textbf{Objective Function:}
\[
\text{Minimize } Z = \sum_{n=1}^{N} \left( cost\_regular \cdot reg\_quant_{n} + cost\_overtime \cdot over\_quant_{n} + store\_cost \cdot inventory_{n} \right)
\]

\textbf{Subject to:}
\begin{itemize}
    \item Production Constraints:
    \[
    reg\_quant_{n} + over\_quant_{n} + inventory_{n-1} \geq demand_{n} \quad \forall n = 1, \ldots, N
    \]
    
    \item Regular Production Capacity:
    \[
    reg\_quant_{n} \leq max\_regular\_amount \quad \forall n = 1, \ldots, N
    \]

    \item Inventory Balance:
    \[
    inventory_{n} = inventory_{n-1} + reg\_quant_{n} + over\_quant_{n} - demand_{n} \quad \forall n = 1, \ldots, N
    \]
    
    \item Non-negativity Constraints:
    \[
    reg\_quant_{n} \geq 0, \quad over\_quant_{n} \geq 0, \quad inventory_{n} \geq 0 \quad \forall n = 1, \ldots, N
    \]
\end{itemize}

\textbf{Output:}
The solution will yield the quantities of products produced using regular and overtime production for each month:
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

#### Data from the given JSON format
data = {'demand': [10.0, 20.0, 10.0], 'max_regular_amount': 5.0, 'cost_regular': 10.0, 'cost_overtime': 12.0, 'store_cost': 1.0}
N = len(data['demand'])
demand = data['demand']
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']

#### Create the problem variable
problem = pulp.LpProblem("Production_Scheduling", pulp.LpMinimize)

#### Decision Variables
reg_quant = pulp.LpVariable.dicts("reg_quant", range(N), lowBound=0)
over_quant = pulp.LpVariable.dicts("over_quant", range(N), lowBound=0)
inventory = pulp.LpVariable.dicts("inventory", range(N), lowBound=0)

#### Objective Function
problem += pulp.lpSum(cost_regular * reg_quant[n] + cost_overtime * over_quant[n] + store_cost * inventory[n] for n in range(N))

#### Production Constraints
for n in range(N):
    if n == 0:
        problem += reg_quant[n] + over_quant[n] >= demand[n], f"Demand_Constraint_{n+1}"
    else:
        problem += reg_quant[n] + over_quant[n] + inventory[n-1] >= demand[n], f"Demand_Constraint_{n+1}"

#### Regular Production Capacity Constraint
for n in range(N):
    problem += reg_quant[n] <= max_regular_amount, f"Regular_Capacity_Constraint_{n+1}"

#### Inventory Balance Constraint
for n in range(N):
    if n == 0:
        problem += inventory[n] == reg_quant[n] + over_quant[n] - demand[n], f"Inventory_Balance_Constraint_{n+1}"
    else:
        problem += inventory[n] == inventory[n-1] + reg_quant[n] + over_quant[n] - demand[n], f"Inventory_Balance_Constraint_{n+1}"

#### Solve the problem
problem.solve()

#### Output the results
reg_quant_values = [reg_quant[n].varValue for n in range(N)]
over_quant_values = [over_quant[n].varValue for n in range(N)]

print(f'Regular production quantities: {reg_quant_values}')
print(f'Overtime production quantities: {over_quant_values}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

