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
To solve this problem, we need to create a Linear Programming model that maximizes the profit obtained from buying and selling a commodity over multiple periods while considering the capacity and holding costs of the warehouse. Here's the mathematical formulation using the given problem description:

We define the following decision variables for each period \( n \):
- \( \text{buyquantity}_n \): The amount of commodity bought in period \( n \).
- \( \text{sellquantity}_n \): The amount of commodity sold in period \( n \).
- \( \text{stock}_n \): The amount of commodity stock at the end of period \( n \).

We aim to maximize the total profit, which can be formulated as:

\[
\text{Maximize } \sum_{n=1}^{N} \left( \text{price}_n \times \text{sellquantity}_n - \text{cost}_n \times \text{buyquantity}_n - \text{holding\_cost} \times \text{stock}_n \right)
\]

Subject to the following constraints:
1. Stock balance constraint:
   \[
   \text{stock}_n = \text{stock}_{n-1} + \text{buyquantity}_n - \text{sellquantity}_n \quad \text{for } n = 1, \ldots, N
   \]
   with initial stock \( \text{stock}_0 = 0 \).

2. Capacity constraint:
   \[
   0 \leq \text{stock}_n \leq \text{capacity} \quad \text{for } n = 1, \ldots, N
   \]

3. Non-negativity constraints:
   \[
   \text{buyquantity}_n \geq 0, \quad \text{sellquantity}_n \geq 0, \quad \text{stock}_n \geq 0 \quad \text{for } n = 1, \ldots, N
   \]

4. Final period stock must be zero:
   \[
   \text{stock}_N = 0
   \]

Here is the complete mathematical model in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Linear Programming Model:}

\textbf{Objective:} Maximize profit

\begin{equation}
\text{Maximize } \sum_{n=1}^{N} \left( \text{price}_n \times \text{sellquantity}_n - \text{cost}_n \times \text{buyquantity}_n - \text{holding\_cost} \times \text{stock}_n \right)
\end{equation}

\textbf{Subject to:}

\begin{align}
\text{stock}_n &= \text{stock}_{n-1} + \text{buyquantity}_n - \text{sellquantity}_n, \quad \forall n = 1, \ldots, N \\
\text{stock}_0 &= 0 \\
0 &\leq \text{stock}_n \leq \text{capacity}, \quad \forall n = 1, \ldots, N \\
\text{buyquantity}_n &\geq 0, \quad \forall n = 1, \ldots, N \\
\text{sellquantity}_n &\geq 0, \quad \forall n = 1, \ldots, N \\
\text{stock}_N &= 0
\end{align}

\end{document}
```

This model provides a framework to determine the optimal buying and selling strategy to maximize profit, taking into account the fluctuating prices, costs, and storage limitations.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Linear Programming Model:}

\textbf{Objective:} Maximize profit

\begin{equation}
\text{Maximize } \sum_{n=1}^{N} \left( \text{price}_n \times \text{sellquantity}_n - \text{cost}_n \times \text{buyquantity}_n - \text{holding\_cost} \times \text{stock}_n \right)
\end{equation}

\textbf{Subject to:}

\begin{align}
\text{stock}_n &= \text{stock}_{n-1} + \text{buyquantity}_n - \text{sellquantity}_n, \quad \forall n = 1, \ldots, N \\
\text{stock}_0 &= 0 \\
0 &\leq \text{stock}_n \leq \text{capacity}, \quad \forall n = 1, \ldots, N \\
\text{buyquantity}_n &\geq 0, \quad \forall n = 1, \ldots, N \\
\text{sellquantity}_n &\geq 0, \quad \forall n = 1, \ldots, N \\
\text{stock}_N &= 0
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

N = len(data['price'])  #### Number of periods

#### Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
buyquantity = [pulp.LpVariable(f'buyquantity_{n}', lowBound=0, cat='Continuous') for n in range(N)]
sellquantity = [pulp.LpVariable(f'sellquantity_{n}', lowBound=0, cat='Continuous') for n in range(N)]
stock = [pulp.LpVariable(f'stock_{n}', lowBound=0, upBound=data['capacity'], cat='Continuous') for n in range(N)]

#### Objective function
objective = pulp.lpSum([data['price'][n] * sellquantity[n] - data['cost'][n] * buyquantity[n] - data['holding_cost'] * stock[n] for n in range(N)])
problem += objective

#### Constraints
#### Stock balance constraints
problem += stock[0] == buyquantity[0] - sellquantity[0]
for n in range(1, N):
    problem += stock[n] == stock[n-1] + buyquantity[n] - sellquantity[n]

#### Initial stock
problem += stock[0] == 0

#### Capacity constraints
for n in range(N):
    problem += stock[n] <= data['capacity']

#### Ending stock
problem += stock[N-1] == 0

#### Solve the problem
problem.solve()

#### Output
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

