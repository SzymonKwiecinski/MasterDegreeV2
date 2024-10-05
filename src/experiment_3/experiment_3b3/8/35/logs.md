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

\section*{Linear Programming Model for Warehouse Operations}

\subsection*{Notation}
\begin{itemize}
    \item $N$: Total number of periods
    \item $capacity$: Fixed capacity of the warehouse
    \item $holding\_cost$: Cost per unit for holding stock for one period
    \item $price_n$: Selling price of the commodity in period $n$, for $n = 1, \ldots, N$
    \item $cost_n$: Cost of the commodity in period $n$, for $n = 1, \ldots, N$
    \item $buyquantity_n$: Amount of buying in period $n$, for $n = 1, \ldots, N$
    \item $sellquantity_n$: Amount of selling in period $n$, for $n = 1, \ldots, N$
    \item $stock_n$: Stock at the end of period $n$, for $n = 1, \ldots, N$
\end{itemize}

\subsection*{Variables}
\begin{itemize}
    \item $buyquantity_n \geq 0$ for all $n$
    \item $sellquantity_n \geq 0$ for all $n$
    \item $stock_n \geq 0$ for all $n$
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:
\[
Z = \sum_{n=1}^{N} \left( price_n \cdot sellquantity_n - cost_n \cdot buyquantity_n - holding\_cost \cdot stock_n \right)
\]

\subsection*{Constraints}
\begin{align}
    stock_1 & = buyquantity_1 - sellquantity_1 \\
    stock_n & = stock_{n-1} + buyquantity_n - sellquantity_n \quad \text{for } n = 2, \ldots, N \\
    stock_n & \leq capacity \quad \text{for } n = 1, \ldots, N \\
    sellquantity_n & \leq stock_n \quad \text{for } n = 1, \ldots, N \\
    stock_N & = 0
\end{align}

\subsection*{Output Variables}
The output will consist of:
\begin{itemize}
    \item buyquantity: $[buyquantity_1, buyquantity_2, \ldots, buyquantity_N]$
    \item sellquantity: $[sellquantity_1, sellquantity_2, \ldots, sellquantity_N]$
    \item stock: $[stock_1, stock_2, \ldots, stock_N]$
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

\section*{Linear Programming Model for Warehouse Operations}

\subsection*{Notation}
\begin{itemize}
    \item $N$: Total number of periods
    \item $capacity$: Fixed capacity of the warehouse
    \item $holding\_cost$: Cost per unit for holding stock for one period
    \item $price_n$: Selling price of the commodity in period $n$, for $n = 1, \ldots, N$
    \item $cost_n$: Cost of the commodity in period $n$, for $n = 1, \ldots, N$
    \item $buyquantity_n$: Amount of buying in period $n$, for $n = 1, \ldots, N$
    \item $sellquantity_n$: Amount of selling in period $n$, for $n = 1, \ldots, N$
    \item $stock_n$: Stock at the end of period $n$, for $n = 1, \ldots, N$
\end{itemize}

\subsection*{Variables}
\begin{itemize}
    \item $buyquantity_n \geq 0$ for all $n$
    \item $sellquantity_n \geq 0$ for all $n$
    \item $stock_n \geq 0$ for all $n$
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:
\[
Z = \sum_{n=1}^{N} \left( price_n \cdot sellquantity_n - cost_n \cdot buyquantity_n - holding\_cost \cdot stock_n \right)
\]

\subsection*{Constraints}
\begin{align}
    stock_1 & = buyquantity_1 - sellquantity_1 \\
    stock_n & = stock_{n-1} + buyquantity_n - sellquantity_n \quad \text{for } n = 2, \ldots, N \\
    stock_n & \leq capacity \quad \text{for } n = 1, \ldots, N \\
    sellquantity_n & \leq stock_n \quad \text{for } n = 1, \ldots, N \\
    stock_N & = 0
\end{align}

\subsection*{Output Variables}
The output will consist of:
\begin{itemize}
    \item buyquantity: $[buyquantity_1, buyquantity_2, \ldots, buyquantity_N]$
    \item sellquantity: $[sellquantity_1, sellquantity_2, \ldots, sellquantity_N]$
    \item stock: $[stock_1, stock_2, \ldots, stock_N]$
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON
data = {'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}
N = len(data['price'])
capacity = data['capacity']
holding_cost = data['holding_cost']
price = data['price']
cost = data['cost']

#### Problem definition
problem = pulp.LpProblem("Warehouse_Operations", pulp.LpMaximize)

#### Variables
buyquantity = [pulp.LpVariable(f'buyquantity_{n}', lowBound=0, cat='Continuous') for n in range(1, N+1)]
sellquantity = [pulp.LpVariable(f'sellquantity_{n}', lowBound=0, cat='Continuous') for n in range(1, N+1)]
stock = [pulp.LpVariable(f'stock_{n}', lowBound=0, cat='Continuous') for n in range(1, N+1)]

#### Objective function
profit = pulp.lpSum([price[n] * sellquantity[n] - cost[n] * buyquantity[n] - holding_cost * stock[n] for n in range(N)])
problem += profit

#### Constraints

#### Initial stock
problem += stock[0] == buyquantity[0] - sellquantity[0]

#### Stock balance equation for rest of periods
for n in range(1, N):
    problem += stock[n] == stock[n-1] + buyquantity[n] - sellquantity[n]

#### Capacity constraints
for n in range(N):
    problem += stock[n] <= capacity

#### Sell quantity cannot exceed stock
for n in range(N):
    problem += sellquantity[n] <= stock[n]

#### Final stock is zero
problem += stock[N-1] == 0

#### Solve the problem
problem.solve()

#### Output the results
print(f'Buy Quantities: {[pulp.value(bq) for bq in buyquantity]}')
print(f'Sell Quantities: {[pulp.value(sq) for sq in sellquantity]}')
print(f'Stock Levels: {[pulp.value(st) for st in stock]}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

