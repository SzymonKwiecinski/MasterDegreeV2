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
To solve this linear programming problem, we need to determine the optimal amounts to buy and sell in each period to maximize profit, subject to the constraints of warehouse capacity and holding costs. The mathematical model in LaTeX format is as follows:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:}

Maximize the total profit over $N$ periods:

\[
\text{Maximize} \quad \sum_{n=1}^{N} \left( \text{price}_n \times \text{sellquantity}_n - \text{cost}_n \times \text{buyquantity}_n \right) - \sum_{n=1}^{N} \text{holding\_cost} \times \text{stock}_n
\]

\textbf{Subject to the constraints:}

1. Stock balance equation for each period $n$:

\[
\text{stock}_n = \text{stock}_{n-1} + \text{buyquantity}_n - \text{sellquantity}_n, \quad \forall n \in \{1, 2, ..., N\}
\]

2. Warehouse capacity constraint:

\[
0 \leq \text{stock}_n \leq \text{capacity}, \quad \forall n \in \{1, 2, ..., N\}
\]

3. Non-negativity constraints:

\[
\text{buyquantity}_n \geq 0, \quad \text{sellquantity}_n \geq 0, \quad \forall n \in \{1, 2, ..., N\}
\]

4. Initial and final stock conditions:

\[
\text{stock}_0 = 0, \quad \text{stock}_N = 0
\]

\textbf{Variables:}

- $\text{buyquantity}_n$: Amount of commodity bought in period $n$.
- $\text{sellquantity}_n$: Amount of commodity sold in period $n$.
- $\text{stock}_n$: Amount of commodity in stock at the end of period $n$.

Given the input parameters:

- \text{capacity}: Maximum warehouse capacity (units).
- \text{holding\_cost}: Cost per unit for holding stock for one period.
- \text{price}_n: Selling price of the commodity in period $n$.
- \text{cost}_n: Purchase price of the commodity in period $n$.

\end{document}
```

This formulation helps to determine the optimal buying and selling amounts for each period to maximize profitability, taking into account the constraints related to stock levels and warehouse capacity.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:}

Maximize the total profit over $N$ periods:

\[
\text{Maximize} \quad \sum_{n=1}^{N} \left( \text{price}_n \times \text{sellquantity}_n - \text{cost}_n \times \text{buyquantity}_n \right) - \sum_{n=1}^{N} \text{holding\_cost} \times \text{stock}_n
\]

\textbf{Subject to the constraints:}

1. Stock balance equation for each period $n$:

\[
\text{stock}_n = \text{stock}_{n-1} + \text{buyquantity}_n - \text{sellquantity}_n, \quad \forall n \in \{1, 2, ..., N\}
\]

2. Warehouse capacity constraint:

\[
0 \leq \text{stock}_n \leq \text{capacity}, \quad \forall n \in \{1, 2, ..., N\}
\]

3. Non-negativity constraints:

\[
\text{buyquantity}_n \geq 0, \quad \text{sellquantity}_n \geq 0, \quad \forall n \in \{1, 2, ..., N\}
\]

4. Initial and final stock conditions:

\[
\text{stock}_0 = 0, \quad \text{stock}_N = 0
\]

\textbf{Variables:}

- $\text{buyquantity}_n$: Amount of commodity bought in period $n$.
- $\text{sellquantity}_n$: Amount of commodity sold in period $n$.
- $\text{stock}_n$: Amount of commodity in stock at the end of period $n$.

Given the input parameters:

- \text{capacity}: Maximum warehouse capacity (units).
- \text{holding\_cost}: Cost per unit for holding stock for one period.
- \text{price}_n: Selling price of the commodity in period $n$.
- \text{cost}_n: Purchase price of the commodity in period $n$.

\end{document}</MATH_MODEL>
<DATA>
{'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Given data in JSON format
data_json = '{"capacity": 10, "holding_cost": 2, "price": [1, 2, 100], "cost": [100, 1, 100]}'
data = json.loads(data_json)

#### Problem setup
N = len(data['price'])
capacity = data['capacity']
holding_cost = data['holding_cost']
prices = data['price']
costs = data['cost']

#### Create a linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
buyquantities = [pulp.LpVariable(f'buyquantity_{n}', lowBound=0) for n in range(N)]
sellquantities = [pulp.LpVariable(f'sellquantity_{n}', lowBound=0) for n in range(N)]
stocks = [pulp.LpVariable(f'stock_{n}', lowBound=0, upBound=capacity) for n in range(N)]

#### Objective function
profit_expr = pulp.lpSum(prices[n] * sellquantities[n] - costs[n] * buyquantities[n] for n in range(N)) - \
              pulp.lpSum(holding_cost * stocks[n] for n in range(N))
problem += profit_expr

#### Constraints
#### Initial stock condition
problem += (stocks[0] == 0)

#### Stock balance equation and warehouse capacity constraints
for n in range(1, N):
    problem += (stocks[n] == stocks[n - 1] + buyquantities[n] - sellquantities[n])

#### Final stock condition
problem += (stocks[N-1] == 0)

#### Non-negativity and stock capacity constraints
for n in range(N):
    problem += (stocks[n] >= 0)
    problem += (stocks[n] <= capacity)

#### Solve the problem
problem.solve()

#### Output the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

