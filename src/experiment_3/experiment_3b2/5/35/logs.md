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
To build a linear programming model for the given problem of managing warehouse operations for profit maximization over several periods, let's define the decision variables and the constraints based on the given input.

We denote:
- \( \text{buyquantity}_n \): the amount of the commodity purchased in period \( n \).
- \( \text{sellquantity}_n \): the amount of the commodity sold in period \( n \).
- \( \text{stock}_n \): the stock level at the end of period \( n \).

The aim is to maximize profit over \( N \) periods. The profit for each period can be calculated as revenue from selling minus cost of buying minus holding costs.

Now, let's create the linear programming model in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\title{Warehouse Operations Linear Programming Model}
\maketitle

\section*{Model Formulation}

\subsection*{Given Parameters}
\begin{itemize}
    \item Capacity of the warehouse: \( \text{capacity} \)
    \item Holding cost per unit per period: \( \text{holding\_cost} \)
    \item Selling price in period \( n \): \( \text{price}_n \)
    \item Cost price in period \( n \): \( \text{cost}_n \)
\end{itemize}

\subsection*{Decision Variables}
\begin{align*}
    \text{buyquantity}_n & : \text{Amount purchased in period } n \\
    \text{sellquantity}_n & : \text{Amount sold in period } n \\
    \text{stock}_n & : \text{Stock level at the end of period } n \\
\end{align*}

\subsection*{Objective Function}
Maximize total profit over \( N \) periods:
\[
\max \sum_{n=1}^{N} \left( \text{price}_n \cdot \text{sellquantity}_n - \text{cost}_n \cdot \text{buyquantity}_n - \text{holding\_cost} \cdot \text{stock}_n \right)
\]

\subsection*{Constraints}
\begin{align*}
    \text{stock}_0 & = 0 \quad \text{(Initial stock is empty)} \\
    \text{stock}_N & = 0 \quad \text{(Final stock must be empty)} \\
    \text{stock}_n & = \text{stock}_{n-1} + \text{buyquantity}_n - \text{sellquantity}_n, \quad \forall n = 1, \ldots, N \quad \text{(Stock balance)} \\
    0 & \leq \text{stock}_n \leq \text{capacity}, \quad \forall n = 1, \ldots, N \quad \text{(Capacity constraint)} \\
    \text{buyquantity}_n & \geq 0, \quad \text{sellquantity}_n \geq 0, \quad \forall n = 1, \ldots, N \quad \text{(Non-negativity)}
\end{align*}

\end{document}
```

This model captures the essence of the problem: determining optimal buying, selling, and stock levels over the given periods to maximize profit while adhering to capacity constraints and ensuring the warehouse is empty at the start and end of the planning horizon.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\title{Warehouse Operations Linear Programming Model}
\maketitle

\section*{Model Formulation}

\subsection*{Given Parameters}
\begin{itemize}
    \item Capacity of the warehouse: \( \text{capacity} \)
    \item Holding cost per unit per period: \( \text{holding\_cost} \)
    \item Selling price in period \( n \): \( \text{price}_n \)
    \item Cost price in period \( n \): \( \text{cost}_n \)
\end{itemize}

\subsection*{Decision Variables}
\begin{align*}
    \text{buyquantity}_n & : \text{Amount purchased in period } n \\
    \text{sellquantity}_n & : \text{Amount sold in period } n \\
    \text{stock}_n & : \text{Stock level at the end of period } n \\
\end{align*}

\subsection*{Objective Function}
Maximize total profit over \( N \) periods:
\[
\max \sum_{n=1}^{N} \left( \text{price}_n \cdot \text{sellquantity}_n - \text{cost}_n \cdot \text{buyquantity}_n - \text{holding\_cost} \cdot \text{stock}_n \right)
\]

\subsection*{Constraints}
\begin{align*}
    \text{stock}_0 & = 0 \quad \text{(Initial stock is empty)} \\
    \text{stock}_N & = 0 \quad \text{(Final stock must be empty)} \\
    \text{stock}_n & = \text{stock}_{n-1} + \text{buyquantity}_n - \text{sellquantity}_n, \quad \forall n = 1, \ldots, N \quad \text{(Stock balance)} \\
    0 & \leq \text{stock}_n \leq \text{capacity}, \quad \forall n = 1, \ldots, N \quad \text{(Capacity constraint)} \\
    \text{buyquantity}_n & \geq 0, \quad \text{sellquantity}_n \geq 0, \quad \forall n = 1, \ldots, N \quad \text{(Non-negativity)}
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

data = json.loads('{"capacity": 10, "holding_cost": 2, "price": [1, 2, 100], "cost": [100, 1, 100]}')

#### Extracting parameters from the data
capacity = data['capacity']
holding_cost = data['holding_cost']
prices = data['price']
costs = data['cost']
N = len(prices)

#### Create the linear programming problem
problem = pulp.LpProblem("Warehouse_Operations", pulp.LpMaximize)

#### Decision Variables
buyquantity = pulp.LpVariable.dicts("buyquantity", range(1, N + 1), lowBound=0)
sellquantity = pulp.LpVariable.dicts("sellquantity", range(1, N + 1), lowBound=0)
stock = pulp.LpVariable.dicts("stock", range(1, N + 1), lowBound=0, upBound=capacity)

#### Objective Function
problem += pulp.lpSum(prices[n - 1] * sellquantity[n] - costs[n - 1] * buyquantity[n] - holding_cost * stock[n] for n in range(1, N + 1))

#### Constraints
problem += (stock[1] == buyquantity[1] - sellquantity[1], "Initial_Stock_Condition")

for n in range(2, N + 1):
    problem += (stock[n] == stock[n - 1] + buyquantity[n] - sellquantity[n], f"Stock_Balance_{n}")

problem += (stock[N] == 0, "Final_Stock_Condition")

for n in range(1, N + 1):
    problem += (stock[n] >= 0, f"Non_Negative_Stock_{n}")
    problem += (stock[n] <= capacity, f"Capacity_Constraint_{n}")

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

