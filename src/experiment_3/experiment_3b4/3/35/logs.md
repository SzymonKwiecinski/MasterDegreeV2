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
To formulate the given problem as a Linear Programming (LP) model, we need to define the decision variables, the objective function, and the constraints.

Let's denote:
- \( \text{buyquantity}_{n} \) as the amount of commodity bought in period \( n \).
- \( \text{sellquantity}_{n} \) as the amount of commodity sold in period \( n \).
- \( \text{stock}_{n} \) as the amount of stock at the end of period \( n \).

The objective is to maximize the total profit, which is the total revenue from selling minus the total cost of buying and the holding costs over the periods.

Here's the LP formulation in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Warehouse Operation Linear Programming Model}

\subsection*{Objective Function}
Maximize the profit:
\[
\text{Maximize} \quad \sum_{n=1}^{N} \left( \text{price}_n \cdot \text{sellquantity}_n - \text{cost}_n \cdot \text{buyquantity}_n - \text{holding\_cost} \cdot \text{stock}_n \right)
\]

\subsection*{Constraints}
\begin{align}
    \text{stock}_0 & = 0 \\
    \text{stock}_N & = 0 \\
    \text{stock}_n & = \text{stock}_{n-1} + \text{buyquantity}_n - \text{sellquantity}_n \quad \forall n = 1, \ldots, N \\
    \text{stock}_n & \leq \text{capacity} \quad \forall n = 1, \ldots, N \\
    \text{buyquantity}_n, \text{sellquantity}_n, \text{stock}_n & \geq 0 \quad \forall n = 1, \ldots, N
\end{align}

\subsection*{Variables}
- \( \text{buyquantity}_n \): Amount of commodity bought in period \( n \).
- \( \text{sellquantity}_n \): Amount of commodity sold in period \( n \).
- \( \text{stock}_n \): Stock at the end of period \( n \).

\end{document}
```

This LP model captures the following:
- Objective function maximizes the profit considering selling revenue, purchase cost, and holding cost.
- The constraints ensure stock balance, capacity limits, and non-negativity for buying, selling, and stock levels.
- The warehouse starts and ends with zero stock.

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

\subsection*{Objective Function}
Maximize the profit:
\[
\text{Maximize} \quad \sum_{n=1}^{N} \left( \text{price}_n \cdot \text{sellquantity}_n - \text{cost}_n \cdot \text{buyquantity}_n - \text{holding\_cost} \cdot \text{stock}_n \right)
\]

\subsection*{Constraints}
\begin{align}
    \text{stock}_0 & = 0 \\
    \text{stock}_N & = 0 \\
    \text{stock}_n & = \text{stock}_{n-1} + \text{buyquantity}_n - \text{sellquantity}_n \quad \forall n = 1, \ldots, N \\
    \text{stock}_n & \leq \text{capacity} \quad \forall n = 1, \ldots, N \\
    \text{buyquantity}_n, \text{sellquantity}_n, \text{stock}_n & \geq 0 \quad \forall n = 1, \ldots, N
\end{align}

\subsection*{Variables}
- \( \text{buyquantity}_n \): Amount of commodity bought in period \( n \).
- \( \text{sellquantity}_n \): Amount of commodity sold in period \( n \).
- \( \text{stock}_n \): Stock at the end of period \( n \).

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

N = len(data['price'])  #### Number of periods

#### Create a Linear Programming problem
problem = pulp.LpProblem("Warehouse_Operation", pulp.LpMaximize)

#### Define decision variables
buyquantity = [pulp.LpVariable(f"buyquantity_{n}", lowBound=0) for n in range(N)]
sellquantity = [pulp.LpVariable(f"sellquantity_{n}", lowBound=0) for n in range(N)]
stock = [pulp.LpVariable(f"stock_{n}", lowBound=0) for n in range(N + 1)]

#### Objective Function
profit = pulp.lpSum(data['price'][n] * sellquantity[n] -
                    data['cost'][n] * buyquantity[n] -
                    data['holding_cost'] * stock[n] for n in range(N))
problem += profit

#### Constraints
problem += stock[0] == 0  #### Initial stock
problem += stock[N] == 0  #### Final stock

for n in range(1, N + 1):
    problem += stock[n] == stock[n - 1] + buyquantity[n - 1] - sellquantity[n - 1]
    problem += stock[n] <= data['capacity']

#### Solve the problem
problem.solve()

#### Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

