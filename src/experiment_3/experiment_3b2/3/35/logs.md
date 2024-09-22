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
To formulate the given problem as a Linear Programming (LP) model, we need to define the decision variables, the objective function, and the constraints. Let's denote:

- \( \text{buyquantity}_n \): The amount of the commodity bought in period \( n \).
- \( \text{sellquantity}_n \): The amount of the commodity sold in period \( n \).
- \( \text{stock}_n \): The stock of the commodity held at the end of period \( n \).

The objective is to maximize the profit, which is calculated as the revenue from selling minus the cost of purchasing and holding the stock.

Here's how you can set up the LP model:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Warehouse Operation}

\subsection*{Parameters}
\begin{align*}
    \text{capacity} &: \text{Warehouse capacity} \\
    \text{holding\_cost} &: \text{Holding cost per unit per period} \\
    \text{price}_n &: \text{Selling price in period } n \\
    \text{cost}_n &: \text{Purchase cost in period } n \\
    N &: \text{Total number of periods}
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
    \text{buyquantity}_n &: \text{Amount of commodity bought in period } n \\
    \text{sellquantity}_n &: \text{Amount of commodity sold in period } n \\
    \text{stock}_n &: \text{Stock level at the end of period } n
\end{align*}

\subsection*{Objective Function}
Maximize the profit over the periods:
\[
\max \sum_{n=1}^{N} \left( \text{price}_n \times \text{sellquantity}_n - \text{cost}_n \times \text{buyquantity}_n - \text{holding\_cost} \times \text{stock}_n \right)
\]

\subsection*{Constraints}
\begin{align*}
    \text{Initial Condition:} & \quad \text{stock}_0 = 0 \\
    \text{Stock Balance:} & \quad \text{stock}_n = \text{stock}_{n-1} + \text{buyquantity}_n - \text{sellquantity}_n, \quad \forall n = 1, \ldots, N \\
    \text{Capacity Constraint:} & \quad 0 \leq \text{stock}_n \leq \text{capacity}, \quad \forall n = 1, \ldots, N \\
    \text{Non-negativity:} & \quad \text{buyquantity}_n \geq 0, \quad \text{sellquantity}_n \geq 0, \quad \forall n = 1, \ldots, N \\
    \text{End Condition:} & \quad \text{stock}_N = 0
\end{align*}

\end{document}
```

This LP formulation maximizes the profit by controlling the buying and selling activities, ensuring that the warehouse capacity is not exceeded and that it starts and ends with no stock. The constraints enforce the stock balance across periods, maintain non-negativity, and ensure that the warehouse is empty at the last period. Adjust the input parameters as required to reflect the actual problem data.

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

\subsection*{Parameters}
\begin{align*}
    \text{capacity} &: \text{Warehouse capacity} \\
    \text{holding\_cost} &: \text{Holding cost per unit per period} \\
    \text{price}_n &: \text{Selling price in period } n \\
    \text{cost}_n &: \text{Purchase cost in period } n \\
    N &: \text{Total number of periods}
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
    \text{buyquantity}_n &: \text{Amount of commodity bought in period } n \\
    \text{sellquantity}_n &: \text{Amount of commodity sold in period } n \\
    \text{stock}_n &: \text{Stock level at the end of period } n
\end{align*}

\subsection*{Objective Function}
Maximize the profit over the periods:
\[
\max \sum_{n=1}^{N} \left( \text{price}_n \times \text{sellquantity}_n - \text{cost}_n \times \text{buyquantity}_n - \text{holding\_cost} \times \text{stock}_n \right)
\]

\subsection*{Constraints}
\begin{align*}
    \text{Initial Condition:} & \quad \text{stock}_0 = 0 \\
    \text{Stock Balance:} & \quad \text{stock}_n = \text{stock}_{n-1} + \text{buyquantity}_n - \text{sellquantity}_n, \quad \forall n = 1, \ldots, N \\
    \text{Capacity Constraint:} & \quad 0 \leq \text{stock}_n \leq \text{capacity}, \quad \forall n = 1, \ldots, N \\
    \text{Non-negativity:} & \quad \text{buyquantity}_n \geq 0, \quad \text{sellquantity}_n \geq 0, \quad \forall n = 1, \ldots, N \\
    \text{End Condition:} & \quad \text{stock}_N = 0
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data in JSON format
data = json.loads('{"capacity": 10, "holding_cost": 2, "price": [1, 2, 100], "cost": [100, 1, 100]}')

#### Extracting data
capacity = data['capacity']
holding_cost = data['holding_cost']
price = data['price']
cost = data['cost']
N = len(price)

#### Create a Linear Programming problem
problem = pulp.LpProblem("Warehouse_Operation", pulp.LpMaximize)

#### Decision Variables
buyquantity = pulp.LpVariable.dicts("buyquantity", range(N), lowBound=0)
sellquantity = pulp.LpVariable.dicts("sellquantity", range(N), lowBound=0)
stock = pulp.LpVariable.dicts("stock", range(N+1), lowBound=0, upBound=capacity)

#### Objective Function
profit = pulp.lpSum(price[n] * sellquantity[n] - cost[n] * buyquantity[n] - holding_cost * stock[n] for n in range(N))
problem += profit

#### Constraints
problem += (stock[0] == 0)  #### Initial Condition

for n in range(1, N + 1):
    problem += (stock[n] == stock[n-1] + buyquantity[n-1] - sellquantity[n-1])  #### Stock Balance
    problem += (stock[n] <= capacity)  #### Capacity Constraint

problem += (stock[N] == 0)  #### End Condition

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

