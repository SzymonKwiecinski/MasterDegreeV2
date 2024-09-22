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

\section*{Linear Programming Model}

\textbf{Variables:}
\begin{itemize}
    \item $\text{reg\_quant}_n$: Quantity of products produced using regular production in month $n$
    \item $\text{over\_quant}_n$: Quantity of products produced using overtime production in month $n$
    \item $I_n$: Inventory at the end of month $n$
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item $demand_n$: Forecasted demand in month $n$
    \item $max\_regular\_amount$: Maximum units that can be produced using regular production in any month
    \item $cost\_regular$: Cost per unit using regular production
    \item $cost\_overtime$: Cost per unit using overtime production
    \item $store\_cost$: Cost per unit stored per month
    \item $N$: Total number of months
\end{itemize}

\textbf{Objective:}
\begin{align*}
\text{Minimize } Z &= \sum_{n=1}^{N} \left( cost\_regular \cdot \text{reg\_quant}_n + cost\_overtime \cdot \text{over\_quant}_n + store\_cost \cdot I_n \right)
\end{align*}

\textbf{Subject to:}
\begin{align*}
I_0 &= 0 \quad \text{(Initial inventory)}\\
I_n &= I_{n-1} + \text{reg\_quant}_n + \text{over\_quant}_n - demand_n \quad \forall n \in \{1, 2, \ldots, N\}\\
I_n &\geq 0 \quad \forall n \in \{1, 2, \ldots, N\}\\
\text{reg\_quant}_n &\leq max\_regular\_amount \quad \forall n \in \{1, 2, \ldots, N\}\\
\text{reg\_quant}_n, \text{over\_quant}_n &\geq 0 \quad \forall n \in \{1, 2, \ldots, N\}
\end{align*}

\textbf{Output:}
\begin{itemize}
    \item $\text{reg\_quant} = [\text{reg\_quant}_1, \text{reg\_quant}_2, \ldots, \text{reg\_quant}_N]$
    \item $\text{over\_quant} = [\text{over\_quant}_1, \text{over\_quant}_2, \ldots, \text{over\_quant}_N]$
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

\section*{Linear Programming Model}

\textbf{Variables:}
\begin{itemize}
    \item $\text{reg\_quant}_n$: Quantity of products produced using regular production in month $n$
    \item $\text{over\_quant}_n$: Quantity of products produced using overtime production in month $n$
    \item $I_n$: Inventory at the end of month $n$
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item $demand_n$: Forecasted demand in month $n$
    \item $max\_regular\_amount$: Maximum units that can be produced using regular production in any month
    \item $cost\_regular$: Cost per unit using regular production
    \item $cost\_overtime$: Cost per unit using overtime production
    \item $store\_cost$: Cost per unit stored per month
    \item $N$: Total number of months
\end{itemize}

\textbf{Objective:}
\begin{align*}
\text{Minimize } Z &= \sum_{n=1}^{N} \left( cost\_regular \cdot \text{reg\_quant}_n + cost\_overtime \cdot \text{over\_quant}_n + store\_cost \cdot I_n \right)
\end{align*}

\textbf{Subject to:}
\begin{align*}
I_0 &= 0 \quad \text{(Initial inventory)}\\
I_n &= I_{n-1} + \text{reg\_quant}_n + \text{over\_quant}_n - demand_n \quad \forall n \in \{1, 2, \ldots, N\}\\
I_n &\geq 0 \quad \forall n \in \{1, 2, \ldots, N\}\\
\text{reg\_quant}_n &\leq max\_regular\_amount \quad \forall n \in \{1, 2, \ldots, N\}\\
\text{reg\_quant}_n, \text{over\_quant}_n &\geq 0 \quad \forall n \in \{1, 2, \ldots, N\}
\end{align*}

\textbf{Output:}
\begin{itemize}
    \item $\text{reg\_quant} = [\text{reg\_quant}_1, \text{reg\_quant}_2, \ldots, \text{reg\_quant}_N]$
    \item $\text{over\_quant} = [\text{over\_quant}_1, \text{over\_quant}_2, \ldots, \text{over\_quant}_N]$
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'demand': [10.0, 20.0, 10.0], 'max_regular_amount': 5.0, 'cost_regular': 10.0, 'cost_overtime': 12.0, 'store_cost': 1.0}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data provided in JSON format
data = {
    'demand': [10.0, 20.0, 10.0],
    'max_regular_amount': 5.0,
    'cost_regular': 10.0,
    'cost_overtime': 12.0,
    'store_cost': 1.0
}

#### Parameters
demand = data['demand']
N = len(demand)
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']

#### Create the problem
problem = pulp.LpProblem("Production_Cost_Minimization", pulp.LpMinimize)

#### Decision variables
reg_quant = pulp.LpVariable.dicts("reg_quant", range(N), lowBound=0)
over_quant = pulp.LpVariable.dicts("over_quant", range(N), lowBound=0)
inventory = pulp.LpVariable.dicts("inventory", range(N), lowBound=0)

#### Objective function
problem += pulp.lpSum(cost_regular * reg_quant[n] + cost_overtime * over_quant[n] + store_cost * inventory[n] for n in range(N))

#### Constraints
problem += (inventory[0] == 0, "Initial_Inventory")

for n in range(1, N):
    problem += (inventory[n] == inventory[n - 1] + reg_quant[n] + over_quant[n] - demand[n], f"Inventory_Balance_{n}")

for n in range(N):
    problem += (inventory[n] >= 0, f"Non_Negative_Inventory_{n}")
    problem += (reg_quant[n] <= max_regular_amount, f"Max_Regular_Amount_{n}")

#### Solve the problem
problem.solve()

#### Output the results
reg_quant_values = [reg_quant[n].varValue for n in range(N)]
over_quant_values = [over_quant[n].varValue for n in range(N)]

print(f'Regular Production Quantities: {reg_quant_values}')
print(f'Overtime Production Quantities: {over_quant_values}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

