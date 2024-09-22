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

\section*{Warehouse Operation Linear Programming Model}

\textbf{Variables:}
\begin{itemize}
    \item Let \( buyquantity_n \) be the amount of buying in period \( n \).
    \item Let \( sellquantity_n \) be the amount of selling in period \( n \).
    \item Let \( stock_n \) be the amount of stock at the end of period \( n \).
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item \( capacity \): Maximum capacity of the warehouse.
    \item \( holding\_cost \): Cost of holding one unit of stock for one period.
    \item \( price_n \): Selling price of the commodity in period \( n \).
    \item \( cost_n \): Purchase cost of the commodity in period \( n \).
    \item \( N \): Total number of periods.
\end{itemize}

\textbf{Objective Function:}
\[
\text{Maximize } Z = \sum_{n=1}^{N} (price_n \cdot sellquantity_n - cost_n \cdot buyquantity_n - holding\_cost \cdot stock_n)
\]

\textbf{Constraints:}
\begin{align*}
    stock_n & = stock_{n-1} + buyquantity_n - sellquantity_n, \quad \forall n = 1, \ldots, N \\
    stock_n & \leq capacity, \quad \forall n = 1, \ldots, N \\
    stock_n & \geq 0, \quad \forall n = 1, \ldots, N \\
    \sum_{n=1}^{N} sellquantity_n & = \sum_{n=1}^{N} buyquantity_n \\
    stock_N & = 0
\end{align*}

\textbf{Output:}
\begin{itemize}
    \item \( buyquantity \): Amount of buying in each period, represented as \( [buyquantity_1, buyquantity_2, \ldots, buyquantity_N] \).
    \item \( sellquantity \): Amount of selling in each period, represented as \( [sellquantity_1, sellquantity_2, \ldots, sellquantity_N] \).
    \item \( stock \): Amount of stock in each period, represented as \( [stock_1, stock_2, \ldots, stock_N] \).
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

\section*{Warehouse Operation Linear Programming Model}

\textbf{Variables:}
\begin{itemize}
    \item Let \( buyquantity_n \) be the amount of buying in period \( n \).
    \item Let \( sellquantity_n \) be the amount of selling in period \( n \).
    \item Let \( stock_n \) be the amount of stock at the end of period \( n \).
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item \( capacity \): Maximum capacity of the warehouse.
    \item \( holding\_cost \): Cost of holding one unit of stock for one period.
    \item \( price_n \): Selling price of the commodity in period \( n \).
    \item \( cost_n \): Purchase cost of the commodity in period \( n \).
    \item \( N \): Total number of periods.
\end{itemize}

\textbf{Objective Function:}
\[
\text{Maximize } Z = \sum_{n=1}^{N} (price_n \cdot sellquantity_n - cost_n \cdot buyquantity_n - holding\_cost \cdot stock_n)
\]

\textbf{Constraints:}
\begin{align*}
    stock_n & = stock_{n-1} + buyquantity_n - sellquantity_n, \quad \forall n = 1, \ldots, N \\
    stock_n & \leq capacity, \quad \forall n = 1, \ldots, N \\
    stock_n & \geq 0, \quad \forall n = 1, \ldots, N \\
    \sum_{n=1}^{N} sellquantity_n & = \sum_{n=1}^{N} buyquantity_n \\
    stock_N & = 0
\end{align*}

\textbf{Output:}
\begin{itemize}
    \item \( buyquantity \): Amount of buying in each period, represented as \( [buyquantity_1, buyquantity_2, \ldots, buyquantity_N] \).
    \item \( sellquantity \): Amount of selling in each period, represented as \( [sellquantity_1, sellquantity_2, \ldots, sellquantity_N] \).
    \item \( stock \): Amount of stock in each period, represented as \( [stock_1, stock_2, \ldots, stock_N] \).
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the provided JSON
data = {'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}
capacity = data['capacity']
holding_cost = data['holding_cost']
price = data['price']
cost = data['cost']
N = len(price)  #### Total number of periods

#### Create the Linear Programming problem
problem = pulp.LpProblem("Warehouse_Operation", pulp.LpMaximize)

#### Define decision variables
buyquantity = [pulp.LpVariable(f'buyquantity_{n+1}', lowBound=0) for n in range(N)]
sellquantity = [pulp.LpVariable(f'sellquantity_{n+1}', lowBound=0) for n in range(N)]
stock = [pulp.LpVariable(f'stock_{n+1}', lowBound=0, upBound=capacity) for n in range(N)]

#### Objective function
problem += pulp.lpSum(price[n] * sellquantity[n] - cost[n] * buyquantity[n] - holding_cost * stock[n] for n in range(N))

#### Constraints
for n in range(N):
    if n == 0:
        problem += stock[n] == buyquantity[n] - sellquantity[n]  #### First period
    else:
        problem += stock[n] == stock[n-1] + buyquantity[n] - sellquantity[n]  #### Stock balance for subsequent periods

    problem += stock[n] <= capacity  #### Capacity constraint
    problem += stock[n] >= 0  #### Non-negativity of stock

#### Selling equals buying constraint
problem += pulp.lpSum(sellquantity[n] for n in range(N)) == pulp.lpSum(buyquantity[n] for n in range(N))

#### Final stock constraint
problem += stock[N-1] == 0  #### Stock at the end of the last period should be zero

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

