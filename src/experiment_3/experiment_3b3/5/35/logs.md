# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP
PROBLEM INFO:

- Consider the problem of operating a warehouse, by buying and selling the stock of a certain commodity, in order to maximize profit over a certain length of time, say several periods.
- The warehouse has a fixed capacity \var{capacity}, and there is a cost \var{holding_cost} per unit for holding stock for one period.
- The selling price, \var{price_{n}}$, of the commodity is known to fluctuate over a number of time periods. 
- In any period \var{n} the price holding for purchase is \var{cost_{n}}.
- The warehouse is originally empty and is required to be empty at the end of the last period.

INPUT FORMAT:

{
	"capacity": capacity,
	"holding_cost": holding_cost,
	"price", [price_{n} for n in 1,...,N],
	"cost": [cost_{n} for n in 1,...,N]
}


OBJECTIVE: Determine the amount of buying and selling in each period to maximize the profit over the months

OUTPUT INFO:

- \var{buyquantity} represents the amount of buying in each period
- \var{sellquantity} represents the amount of selling in each period
- \var{stock} represents the stock in each period, excluding the intial stock

OUTPUT FORMAT:

{
	"buyquantity": [buyquantity_{n} for n in 1,...,N],
	"sellquantity": [sellquantity_{n} for n in 1,...,N],
	"stock": [stock_{n} for n in 1,...,N]
}
</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Warehouse Operation}

\subsection*{Indices}
\begin{itemize}
    \item $n$: Index for time periods, where $n = 1, 2, \ldots, N$.
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item $capacity$: Maximum capacity of the warehouse.
    \item $holding\_cost$: Cost per unit of holding stock for one period.
    \item $price_n$: Selling price of the commodity in period $n$.
    \item $cost_n$: Cost price for purchasing the commodity in period $n$.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $buyquantity_n$: Amount of commodity bought in period $n$.
    \item $sellquantity_n$: Amount of commodity sold in period $n$.
    \item $stock_n$: Amount of stock held in the warehouse at the end of period $n$.
\end{itemize}

\subsection*{Objective Function}
Maximize total profit over all periods:
\[
\text{Maximize } Z = \sum_{n=1}^{N} (price_n \cdot sellquantity_n - cost_n \cdot buyquantity_n - holding\_cost \cdot stock_n)
\]

\subsection*{Constraints}
\begin{align}
    & \text{Stock balance constraint:} \\
    & stock_n = stock_{n-1} + buyquantity_n - sellquantity_n, \quad \forall n = 1, \ldots, N \\
    & \text{Initial stock: } stock_0 = 0 \\
    & \text{Final stock must be zero: } stock_N = 0 \\
    & \text{Capacity constraint:} \\
    & buyquantity_n + stock_{n-1} - sellquantity_n \leq capacity, \quad \forall n = 1, \ldots, N \\
    & \text{Non-negativity constraints:} \\
    & buyquantity_n \geq 0, \quad sellquantity_n \geq 0, \quad stock_n \geq 0, \quad \forall n = 1, \ldots, N
\end{align}

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

\section*{Linear Programming Model for Warehouse Operation}

\subsection*{Indices}
\begin{itemize}
    \item $n$: Index for time periods, where $n = 1, 2, \ldots, N$.
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item $capacity$: Maximum capacity of the warehouse.
    \item $holding\_cost$: Cost per unit of holding stock for one period.
    \item $price_n$: Selling price of the commodity in period $n$.
    \item $cost_n$: Cost price for purchasing the commodity in period $n$.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $buyquantity_n$: Amount of commodity bought in period $n$.
    \item $sellquantity_n$: Amount of commodity sold in period $n$.
    \item $stock_n$: Amount of stock held in the warehouse at the end of period $n$.
\end{itemize}

\subsection*{Objective Function}
Maximize total profit over all periods:
\[
\text{Maximize } Z = \sum_{n=1}^{N} (price_n \cdot sellquantity_n - cost_n \cdot buyquantity_n - holding\_cost \cdot stock_n)
\]

\subsection*{Constraints}
\begin{align}
    & \text{Stock balance constraint:} \\
    & stock_n = stock_{n-1} + buyquantity_n - sellquantity_n, \quad \forall n = 1, \ldots, N \\
    & \text{Initial stock: } stock_0 = 0 \\
    & \text{Final stock must be zero: } stock_N = 0 \\
    & \text{Capacity constraint:} \\
    & buyquantity_n + stock_{n-1} - sellquantity_n \leq capacity, \quad \forall n = 1, \ldots, N \\
    & \text{Non-negativity constraints:} \\
    & buyquantity_n \geq 0, \quad sellquantity_n \geq 0, \quad stock_n \geq 0, \quad \forall n = 1, \ldots, N
\end{align}

\end{document}</MATH_MODEL>
<DATA>
{'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {
    'capacity': 10,
    'holding_cost': 2,
    'price': [1, 2, 100],
    'cost': [100, 1, 100]
}

#### Extract data
capacity = data['capacity']
holding_cost = data['holding_cost']
price = data['price']
cost = data['cost']
N = len(price)

#### Initialize the problem
problem = pulp.LpProblem("Warehouse_Operation", pulp.LpMaximize)

#### Decision Variables
buyquantity = [pulp.LpVariable(f'buyquantity_{n}', lowBound=0, cat='Continuous') for n in range(N)]
sellquantity = [pulp.LpVariable(f'sellquantity_{n}', lowBound=0, cat='Continuous') for n in range(N)]
stock = [pulp.LpVariable(f'stock_{n}', lowBound=0, cat='Continuous') for n in range(N + 1)]

#### Objective Function
profit_expr = [
    price[n] * sellquantity[n] - cost[n] * buyquantity[n] - holding_cost * stock[n]
    for n in range(N)
]
problem += pulp.lpSum(profit_expr)

#### Initial and final stock constraints
problem += stock[0] == 0
problem += stock[N] == 0

#### Constraints
for n in range(N):
    #### Stock balance constraint
    problem += stock[n] == stock[n - 1] + buyquantity[n] - sellquantity[n]
    #### Capacity constraint
    problem += buyquantity[n] + stock[n - 1] - sellquantity[n] <= capacity

#### Solve
problem.solve()

#### Print objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

