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

\subsection*{Variables}
\begin{itemize}
    \item $buyquantity_n$: Amount of commodity bought in period $n$.
    \item $sellquantity_n$: Amount of commodity sold in period $n$.
    \item $stock_n$: Amount of stock held at the end of period $n$.
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item $capacity$: Maximum capacity of the warehouse.
    \item $holding\_cost$: Cost of holding one unit of stock for one period.
    \item $price_n$: Selling price of the commodity in period $n$ (for $n = 1, \ldots, N$).
    \item $cost_n$: Purchase cost of the commodity in period $n$ (for $n = 1, \ldots, N$).
    \item $N$: Total number of periods.
\end{itemize}

\subsection*{Objective Function}
Maximize total profit over $N$ periods:
\[
\text{Maximize} \quad Z = \sum_{n=1}^{N} (price_n \cdot sellquantity_n - cost_n \cdot buyquantity_n - holding\_cost \cdot stock_n)
\]

\subsection*{Constraints}
\begin{align*}
    & \text{Stock Balance:} \\
    & stock_n = stock_{n-1} + buyquantity_n - sellquantity_n, \quad \forall n = 1, \ldots, N \\
    & \text{Initial Condition:} \quad stock_0 = 0 \\
    & \text{Capacity Constraint:} \\
    & stock_n \leq capacity, \quad \forall n = 1, \ldots, N \\
    & \text{Non-negativity Constraints:} \\
    & buyquantity_n \geq 0, \quad sellquantity_n \geq 0, \quad stock_n \geq 0, \quad \forall n = 1, \ldots, N \\
    & \text{Final Condition:} \\
    & stock_N = 0
\end{align*}

\subsection*{Output Format}
The solution to this model will provide the following output:
\begin{itemize}
    \item $buyquantity$: Array of amounts bought in each period: $[buyquantity_1, buyquantity_2, \ldots, buyquantity_N]$
    \item $sellquantity$: Array of amounts sold in each period: $[sellquantity_1, sellquantity_2, \ldots, sellquantity_N]$
    \item $stock$: Array of stock levels at the end of each period: $[stock_1, stock_2, \ldots, stock_N]$
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

\section*{Linear Programming Model for Warehouse Operation}

\subsection*{Variables}
\begin{itemize}
    \item $buyquantity_n$: Amount of commodity bought in period $n$.
    \item $sellquantity_n$: Amount of commodity sold in period $n$.
    \item $stock_n$: Amount of stock held at the end of period $n$.
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item $capacity$: Maximum capacity of the warehouse.
    \item $holding\_cost$: Cost of holding one unit of stock for one period.
    \item $price_n$: Selling price of the commodity in period $n$ (for $n = 1, \ldots, N$).
    \item $cost_n$: Purchase cost of the commodity in period $n$ (for $n = 1, \ldots, N$).
    \item $N$: Total number of periods.
\end{itemize}

\subsection*{Objective Function}
Maximize total profit over $N$ periods:
\[
\text{Maximize} \quad Z = \sum_{n=1}^{N} (price_n \cdot sellquantity_n - cost_n \cdot buyquantity_n - holding\_cost \cdot stock_n)
\]

\subsection*{Constraints}
\begin{align*}
    & \text{Stock Balance:} \\
    & stock_n = stock_{n-1} + buyquantity_n - sellquantity_n, \quad \forall n = 1, \ldots, N \\
    & \text{Initial Condition:} \quad stock_0 = 0 \\
    & \text{Capacity Constraint:} \\
    & stock_n \leq capacity, \quad \forall n = 1, \ldots, N \\
    & \text{Non-negativity Constraints:} \\
    & buyquantity_n \geq 0, \quad sellquantity_n \geq 0, \quad stock_n \geq 0, \quad \forall n = 1, \ldots, N \\
    & \text{Final Condition:} \\
    & stock_N = 0
\end{align*}

\subsection*{Output Format}
The solution to this model will provide the following output:
\begin{itemize}
    \item $buyquantity$: Array of amounts bought in each period: $[buyquantity_1, buyquantity_2, \ldots, buyquantity_N]$
    \item $sellquantity$: Array of amounts sold in each period: $[sellquantity_1, sellquantity_2, \ldots, sellquantity_N]$
    \item $stock$: Array of stock levels at the end of each period: $[stock_1, stock_2, \ldots, stock_N]$
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data provided in JSON format
data_json = '{"capacity": 10, "holding_cost": 2, "price": [1, 2, 100], "cost": [100, 1, 100]}'
data = json.loads(data_json)

#### Parameters
N = len(data['price'])
capacity = data['capacity']
holding_cost = data['holding_cost']
prices = data['price']
costs = data['cost']

#### Create problem
problem = pulp.LpProblem("Warehouse_Operation", pulp.LpMaximize)

#### Variables
buyquantity = pulp.LpVariable.dicts("buyquantity", range(N), lowBound=0)
sellquantity = pulp.LpVariable.dicts("sellquantity", range(N), lowBound=0)
stock = pulp.LpVariable.dicts("stock", range(N), lowBound=0)

#### Objective Function
problem += pulp.lpSum([prices[n] * sellquantity[n] - costs[n] * buyquantity[n] - holding_cost * stock[n] for n in range(N)])

#### Constraints
problem += (stock[0] == 0)  #### Initial condition

for n in range(N):
    if n > 0:
        problem += (stock[n] == stock[n-1] + buyquantity[n] - sellquantity[n])  #### Stock balance
    problem += (stock[n] <= capacity)  #### Capacity constraint
    problem += (buyquantity[n] >= 0)  #### Non-negativity constraint for buy quantity
    problem += (sellquantity[n] >= 0)  #### Non-negativity constraint for sell quantity
    problem += (stock[n] >= 0)  #### Non-negativity constraint for stock

problem += (stock[N-1] == 0)  #### Final condition

#### Solve the problem
problem.solve()

#### Output results
buyquantity_result = [buyquantity[n].varValue for n in range(N)]
sellquantity_result = [sellquantity[n].varValue for n in range(N)]
stock_result = [stock[n].varValue for n in range(N)]

print(f'Buy Quantity: {buyquantity_result}')
print(f'Sell Quantity: {sellquantity_result}')
print(f'Stock: {stock_result}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

