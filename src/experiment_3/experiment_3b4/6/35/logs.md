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
To model the warehouse operating problem as a linear programming problem, we can define the following variables and constraints:

Given:
- Capacity of the warehouse: \( \text{capacity} \)
- Holding cost per unit: \( \text{holding\_cost} \)
- Selling prices: \( \text{price}_n \) for \( n = 1, \ldots, N \)
- Purchase costs: \( \text{cost}_n \) for \( n = 1, \ldots, N \)

Decision Variables:
- \( \text{buyquantity}_n \): Amount of buying in period \( n \)
- \( \text{sellquantity}_n \): Amount of selling in period \( n \)
- \( \text{stock}_n \): Stock at the end of period \( n \)

Objective Function:
- Maximize the total profit over \( N \) periods.

Constraints:
1. Stock constraint: Ensuring the stock does not exceed the capacity.
2. Flow constraint: Balancing stock, purchases, and sales.
3. Non-negativity constraint: Ensuring all variables are non-negative.
4. Initial and final stock constraints: Warehouse starts and ends empty.

The linear programming model in LaTeX format is given below:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:}
\[
\max \sum_{n=1}^{N} \left( \text{price}_n \cdot \text{sellquantity}_n - \text{cost}_n \cdot \text{buyquantity}_n - \text{holding\_cost} \cdot \text{stock}_n \right)
\]

\textbf{Subject to:}
\begin{align*}
& \text{stock}_0 = 0 \\
& \text{stock}_N = 0 \\
& \text{stock}_n = \text{stock}_{n-1} + \text{buyquantity}_n - \text{sellquantity}_n, \quad n = 1, \ldots, N \\
& \text{stock}_n \leq \text{capacity}, \quad n = 1, \ldots, N \\
& \text{buyquantity}_n \geq 0, \quad n = 1, \ldots, N \\
& \text{sellquantity}_n \geq 0, \quad n = 1, \ldots, N \\
& \text{stock}_n \geq 0, \quad n = 1, \ldots, N \\
\end{align*}

\end{document}
```

This model represents a multi-period decision-making process that aligns with the LP formulation to maximize profit by optimally planning purchase, sales, and stock levels of a commodity, given the constraints and costs associated with holding and trading the commodity over a series of periods.

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
\[
\max \sum_{n=1}^{N} \left( \text{price}_n \cdot \text{sellquantity}_n - \text{cost}_n \cdot \text{buyquantity}_n - \text{holding\_cost} \cdot \text{stock}_n \right)
\]

\textbf{Subject to:}
\begin{align*}
& \text{stock}_0 = 0 \\
& \text{stock}_N = 0 \\
& \text{stock}_n = \text{stock}_{n-1} + \text{buyquantity}_n - \text{sellquantity}_n, \quad n = 1, \ldots, N \\
& \text{stock}_n \leq \text{capacity}, \quad n = 1, \ldots, N \\
& \text{buyquantity}_n \geq 0, \quad n = 1, \ldots, N \\
& \text{sellquantity}_n \geq 0, \quad n = 1, \ldots, N \\
& \text{stock}_n \geq 0, \quad n = 1, \ldots, N \\
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}
N = len(data['price'])

#### Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
buyquantity = pulp.LpVariable.dicts("BuyQuantity", range(N), lowBound=0, cat='Continuous')
sellquantity = pulp.LpVariable.dicts("SellQuantity", range(N), lowBound=0, cat='Continuous')
stock = pulp.LpVariable.dicts("Stock", range(N+1), lowBound=0, cat='Continuous')

#### Objective Function
problem += pulp.lpSum(data['price'][n] * sellquantity[n] - 
                      data['cost'][n] * buyquantity[n] - 
                      data['holding_cost'] * stock[n] for n in range(N))

#### Constraints
problem += stock[0] == 0  #### Initial stock
problem += stock[N] == 0  #### Ending stock

for n in range(1, N+1):
    problem += stock[n] == stock[n-1] + buyquantity[n-1] - sellquantity[n-1]  #### Stock balance

for n in range(N):
    problem += stock[n] <= data['capacity']  #### Capacity constraint

#### Solve
problem.solve()

#### Output result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

