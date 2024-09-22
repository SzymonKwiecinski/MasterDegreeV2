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
To address this problem using Linear Programming, we will formulate a mathematical model to maximize the profit from buying and selling a commodity over several periods while considering the warehouse's constraints. We will use the variables \texttt{buyquantity} and \texttt{sellquantity} to determine how much of the commodity to buy and sell in each period, respectively. The variable \texttt{stock} will denote the amount of commodity held in the warehouse at the end of each period.

Below is the mathematical model represented in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective: } Maximize the profit

\begin{align*}
\text{Maximize } & \sum_{n=1}^{N} (\text{price}_n \times \text{sellquantity}_n - \text{cost}_n \times \text{buyquantity}_n) - \text{holding\_cost} \sum_{n=1}^{N} \text{stock}_n
\end{align*}

\textbf{Subject to:}
\begin{align*}
\text{stock}_0 & = 0 \\
\text{stock}_n & = \text{stock}_{n-1} + \text{buyquantity}_n - \text{sellquantity}_n, \quad \forall n \in \{1, \ldots, N\} \\
\text{sellquantity}_n & \leq \text{stock}_{n-1} + \text{buyquantity}_n, \quad \forall n \in \{1, \ldots, N\} \\
\text{stock}_n & \leq \text{capacity}, \quad \forall n \in \{1, \ldots, N\} \\
\text{stock}_N & = 0 \\
\text{buyquantity}_n, \text{sellquantity}_n, \text{stock}_n & \geq 0, \quad \forall n \in \{1, \ldots, N\}
\end{align*}

\textbf{Variables:}
\begin{itemize}
  \item \text{buyquantity}_n: The amount of commodity bought in period \(n\).
  \item \text{sellquantity}_n: The amount of commodity sold in period \(n\).
  \item \text{stock}_n: The stock at the end of period \(n\).
\end{itemize}

\end{document}
```

This LaTeX code sets up constraints to ensure that the stock does not exceed the warehouse's capacity, that the warehouse begins and ends with zero stock, and that no negative quantities are involved in buying, selling, or holding stock. The objective is to maximize the total profit over all periods.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective: } Maximize the profit

\begin{align*}
\text{Maximize } & \sum_{n=1}^{N} (\text{price}_n \times \text{sellquantity}_n - \text{cost}_n \times \text{buyquantity}_n) - \text{holding\_cost} \sum_{n=1}^{N} \text{stock}_n
\end{align*}

\textbf{Subject to:}
\begin{align*}
\text{stock}_0 & = 0 \\
\text{stock}_n & = \text{stock}_{n-1} + \text{buyquantity}_n - \text{sellquantity}_n, \quad \forall n \in \{1, \ldots, N\} \\
\text{sellquantity}_n & \leq \text{stock}_{n-1} + \text{buyquantity}_n, \quad \forall n \in \{1, \ldots, N\} \\
\text{stock}_n & \leq \text{capacity}, \quad \forall n \in \{1, \ldots, N\} \\
\text{stock}_N & = 0 \\
\text{buyquantity}_n, \text{sellquantity}_n, \text{stock}_n & \geq 0, \quad \forall n \in \{1, \ldots, N\}
\end{align*}

\textbf{Variables:}
\begin{itemize}
  \item \text{buyquantity}_n: The amount of commodity bought in period \(n\).
  \item \text{sellquantity}_n: The amount of commodity sold in period \(n\).
  \item \text{stock}_n: The stock at the end of period \(n\).
\end{itemize}

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
N = len(data['price'])
capacity = data['capacity']
holding_cost = data['holding_cost']
price = data['price']
cost = data['cost']

#### Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Variables
buyquantity = [pulp.LpVariable(f'buyquantity_{n}', lowBound=0) for n in range(N)]
sellquantity = [pulp.LpVariable(f'sellquantity_{n}', lowBound=0) for n in range(N)]
stock = [pulp.LpVariable(f'stock_{n}', lowBound=0) for n in range(N)]

#### Objective function
profit = pulp.lpSum([price[n] * sellquantity[n] - cost[n] * buyquantity[n] for n in range(N)]) \
         - holding_cost * pulp.lpSum([stock[n] for n in range(N)])
problem += profit, "Maximize Profit"

#### Constraints
problem += (stock[0] == 0), "Initial Stock is Zero"
for n in range(N):
    if n > 0:
        problem += (stock[n] == stock[n-1] + buyquantity[n] - sellquantity[n]), f"Stock Balance {n}"
    problem += (sellquantity[n] <= stock[n-1] + buyquantity[n]), f"Sell Quantity Less Than or Equals Available {n}"
    problem += (stock[n] <= capacity), f"Stock Capacity {n}"
problem += (stock[N-1] == 0), "Final Stock is Zero"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

