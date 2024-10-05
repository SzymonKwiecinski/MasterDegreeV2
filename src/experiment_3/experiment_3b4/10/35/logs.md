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
To model this problem, we need to define the decision variables, constraints, and the objective function. Our primary goal is to maximize the profit from warehouse operations, considering buying, selling, and holding costs over a series of time periods.

Given:
- \( N \): Number of periods
- \( \text{capacity} \): Maximum stock the warehouse can hold at any time
- \( \text{holding\_cost} \): Cost per unit for holding stock for one period
- \( \text{price}_n \): Selling price in period \( n \)
- \( \text{cost}_n \): Purchase cost in period \( n \)

######### Decision Variables:
- \( \text{buyquantity}_n \): Quantity bought in period \( n \)
- \( \text{sellquantity}_n \): Quantity sold in period \( n \)
- \( \text{stock}_n \): Stock level at the end of period \( n \)

######### Objective Function:
Maximize total profit, considering revenue from sales, cost of purchases, and holding costs.

\[
\text{Maximize} \quad \sum_{n=1}^{N} \left( \text{price}_n \cdot \text{sellquantity}_n - \text{cost}_n \cdot \text{buyquantity}_n - \text{holding\_cost} \cdot \text{stock}_n \right)
\]

######### Constraints:
1. Stock balance constraint for each period:
   \[
   \text{stock}_n = \text{stock}_{n-1} + \text{buyquantity}_n - \text{sellquantity}_n \quad \text{for} \; n=1,2,...,N
   \]
   With initial condition: \(\text{stock}_0 = 0\)

2. Capacity constraint:
   \[
   0 \leq \text{stock}_n \leq \text{capacity} \quad \text{for} \; n=1,2,...,N
   \]

3. Non-negativity constraints for buying and selling:
   \[
   \text{buyquantity}_n \geq 0, \quad \text{sellquantity}_n \geq 0 \quad \text{for} \; n=1,2,...,N
   \]

4. Final condition:
   \[
   \text{stock}_N = 0
   \]

Here's the complete Linear Programming model in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\textbf{Linear Programming Model for Warehouse Operations}

\[
\begin{aligned}
& \text{Maximize} \quad && \sum_{n=1}^{N} \left( \text{price}_n \cdot \text{sellquantity}_n - \text{cost}_n \cdot \text{buyquantity}_n - \text{holding\_cost} \cdot \text{stock}_n \right) \\
& \text{subject to} \quad && \\
& \text{stock}_n = \text{stock}_{n-1} + \text{buyquantity}_n - \text{sellquantity}_n, && \text{for} \; n=1,2,...,N \\
& \text{with initial condition} \quad && \text{stock}_0 = 0 \\
& 0 \leq \text{stock}_n \leq \text{capacity}, && \text{for} \; n=1,2,...,N \\
& \text{buyquantity}_n \geq 0, \quad \text{sellquantity}_n \geq 0, && \text{for} \; n=1,2,...,N \\
& \text{stock}_N = 0
\end{aligned}
\]

\end{document}
```

This model ensures appropriate buying, selling, and maintaining stock levels to maximize the overall profit, considering all relevant constraints and costs.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\textbf{Linear Programming Model for Warehouse Operations}

\[
\begin{aligned}
& \text{Maximize} \quad && \sum_{n=1}^{N} \left( \text{price}_n \cdot \text{sellquantity}_n - \text{cost}_n \cdot \text{buyquantity}_n - \text{holding\_cost} \cdot \text{stock}_n \right) \\
& \text{subject to} \quad && \\
& \text{stock}_n = \text{stock}_{n-1} + \text{buyquantity}_n - \text{sellquantity}_n, && \text{for} \; n=1,2,...,N \\
& \text{with initial condition} \quad && \text{stock}_0 = 0 \\
& 0 \leq \text{stock}_n \leq \text{capacity}, && \text{for} \; n=1,2,...,N \\
& \text{buyquantity}_n \geq 0, \quad \text{sellquantity}_n \geq 0, && \text{for} \; n=1,2,...,N \\
& \text{stock}_N = 0
\end{aligned}
\]

\end{document}</MATH_MODEL>
<DATA>
{'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON
data = {
    'capacity': 10,
    'holding_cost': 2,
    'price': [1, 2, 100],
    'cost': [100, 1, 100]
}

N = len(data['price'])

#### Define the LP problem
problem = pulp.LpProblem("Warehouse_Operations", pulp.LpMaximize)

#### Variables
buyquantity = [pulp.LpVariable(f'buyquantity_{n}', lowBound=0) for n in range(N)]
sellquantity = [pulp.LpVariable(f'sellquantity_{n}', lowBound=0) for n in range(N)]
stock = [pulp.LpVariable(f'stock_{n}', lowBound=0, upBound=data['capacity']) for n in range(N)]

#### Objective function
problem += pulp.lpSum(
    (data['price'][n] * sellquantity[n] - data['cost'][n] * buyquantity[n] - data['holding_cost'] * stock[n]) 
    for n in range(N)
)

#### Constraints
problem += stock[0] == 0  #### Initial stock condition
for n in range(1, N):
    problem += stock[n] == stock[n-1] + buyquantity[n] - sellquantity[n]

problem += stock[N-1] == stock[0]  #### stock_N = 0

#### Solve the problem
problem.solve()

#### Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

