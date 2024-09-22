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

\section*{Mathematical Model for Warehouse Operations}

\subsection*{Indices}
Let \( n \) be the index for the time periods, where \( n = 1, 2, \ldots, N \).

\subsection*{Parameters}
\begin{align*}
& \text{capacity} \quad \text{(maximum stock capacity)} \\
& \text{holding\_cost} \quad \text{(cost per unit of stock held for one period)} \\
& \text{price}_{n} \quad \text{(selling price of the commodity in period } n\text{)} \\
& \text{cost}_{n} \quad \text{(purchase cost of the commodity in period } n\text{)}
\end{align*}

\subsection*{Decision Variables}
Let:
\begin{align*}
& \text{buyquantity}_{n} \quad \text{(amount of commodity bought in period } n\text{)} \\
& \text{sellquantity}_{n} \quad \text{(amount of commodity sold in period } n\text{)} \\
& \text{stock}_{n} \quad \text{(amount of stock at the end of period } n\text{)}
\end{align*}

\subsection*{Objective Function}
Maximize the total profit over the \( N \) periods:
\[
\text{Maximize } Z = \sum_{n=1}^{N} \left( \text{price}_{n} \cdot \text{sellquantity}_{n} - \text{cost}_{n} \cdot \text{buyquantity}_{n} - \text{holding\_cost} \cdot \text{stock}_{n} \right)
\]

\subsection*{Constraints}
1. Stock balance constraint:
\[
\text{stock}_{n} = \text{stock}_{n-1} + \text{buyquantity}_{n} - \text{sellquantity}_{n}, \quad n = 1, 2, \ldots, N
\]
2. Capacity constraint:
\[
\text{stock}_{n} \leq \text{capacity}, \quad n = 1, 2, \ldots, N
\]
3. Non-negativity constraints:
\[
\text{buyquantity}_{n} \geq 0, \quad \text{sellquantity}_{n} \geq 0, \quad \text{stock}_{n} \geq 0, \quad n = 1, 2, \ldots, N
\]
4. Initial and final stock conditions:
\[
\text{stock}_{0} = 0 \quad \text{and} \quad \text{stock}_{N} = 0
\]

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

\section*{Mathematical Model for Warehouse Operations}

\subsection*{Indices}
Let \( n \) be the index for the time periods, where \( n = 1, 2, \ldots, N \).

\subsection*{Parameters}
\begin{align*}
& \text{capacity} \quad \text{(maximum stock capacity)} \\
& \text{holding\_cost} \quad \text{(cost per unit of stock held for one period)} \\
& \text{price}_{n} \quad \text{(selling price of the commodity in period } n\text{)} \\
& \text{cost}_{n} \quad \text{(purchase cost of the commodity in period } n\text{)}
\end{align*}

\subsection*{Decision Variables}
Let:
\begin{align*}
& \text{buyquantity}_{n} \quad \text{(amount of commodity bought in period } n\text{)} \\
& \text{sellquantity}_{n} \quad \text{(amount of commodity sold in period } n\text{)} \\
& \text{stock}_{n} \quad \text{(amount of stock at the end of period } n\text{)}
\end{align*}

\subsection*{Objective Function}
Maximize the total profit over the \( N \) periods:
\[
\text{Maximize } Z = \sum_{n=1}^{N} \left( \text{price}_{n} \cdot \text{sellquantity}_{n} - \text{cost}_{n} \cdot \text{buyquantity}_{n} - \text{holding\_cost} \cdot \text{stock}_{n} \right)
\]

\subsection*{Constraints}
1. Stock balance constraint:
\[
\text{stock}_{n} = \text{stock}_{n-1} + \text{buyquantity}_{n} - \text{sellquantity}_{n}, \quad n = 1, 2, \ldots, N
\]
2. Capacity constraint:
\[
\text{stock}_{n} \leq \text{capacity}, \quad n = 1, 2, \ldots, N
\]
3. Non-negativity constraints:
\[
\text{buyquantity}_{n} \geq 0, \quad \text{sellquantity}_{n} \geq 0, \quad \text{stock}_{n} \geq 0, \quad n = 1, 2, \ldots, N
\]
4. Initial and final stock conditions:
\[
\text{stock}_{0} = 0 \quad \text{and} \quad \text{stock}_{N} = 0
\]

\end{document}</MATH_MODEL>
<DATA>
{'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data
data = json.loads('{"capacity": 10, "holding_cost": 2, "price": [1, 2, 100], "cost": [100, 1, 100]}')
capacity = data['capacity']
holding_cost = data['holding_cost']
prices = data['price']
costs = data['cost']

#### Number of periods
N = len(prices)

#### Create the problem
problem = pulp.LpProblem("Warehouse_Operations", pulp.LpMaximize)

#### Decision Variables
buyquantity = pulp.LpVariable.dicts("buyquantity", range(1, N + 1), lowBound=0)
sellquantity = pulp.LpVariable.dicts("sellquantity", range(1, N + 1), lowBound=0)
stock = pulp.LpVariable.dicts("stock", range(0, N + 1), lowBound=0)

#### Objective Function
profit = pulp.lpSum(prices[n - 1] * sellquantity[n] - costs[n - 1] * buyquantity[n] - holding_cost * stock[n] for n in range(1, N + 1))
problem += profit

#### Constraints
#### Initial stock
problem += stock[0] == 0

#### Stock balance and capacity constraints
for n in range(1, N + 1):
    if n > 1:
        problem += stock[n] == stock[n - 1] + buyquantity[n] - sellquantity[n]
    problem += stock[n] <= capacity

#### Final stock condition
problem += stock[N] == 0

#### Solve the problem
problem.solve()

#### Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

