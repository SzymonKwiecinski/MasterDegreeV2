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
To model the given problem of operating a warehouse to maximize profit, we define the decision variables and constraints necessary to formulate a linear program. Here is the mathematical model in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Warehouse Management}

\subsection*{Decision Variables:}
\begin{itemize}
    \item \( \text{buyquantity}_n \): Quantity of commodity bought in period \( n \), for \( n = 1, \ldots, N \).
    \item \( \text{sellquantity}_n \): Quantity of commodity sold in period \( n \), for \( n = 1, \ldots, N \).
    \item \( \text{stock}_n \): Stock of commodity at the end of period \( n \), for \( n = 1, \ldots, N \).
\end{itemize}

\subsection*{Parameters:}
\begin{itemize}
    \item \text{capacity}: Maximum capacity of the warehouse.
    \item \text{holding\_cost}: Cost per unit for holding stock for one period.
    \item \text{price}_n: Selling price of the commodity in period \( n \).
    \item \text{cost}_n: Purchase cost of the commodity in period \( n \).
\end{itemize}

\subsection*{Objective Function:}
Maximize the profit over the periods:
\[
\text{Maximize} \quad \sum_{n=1}^{N} (\text{price}_n \times \text{sellquantity}_n - \text{cost}_n \times \text{buyquantity}_n - \text{holding\_cost} \times \text{stock}_n)
\]

\subsection*{Constraints:}
\begin{align*}
\text{Stock Balance:} & \quad \text{stock}_n = \text{stock}_{n-1} + \text{buyquantity}_n - \text{sellquantity}_n, \quad \forall n = 1, \ldots, N \\
\text{Capacity Constraint:} & \quad \text{stock}_n \leq \text{capacity}, \quad \forall n = 1, \ldots, N \\
\text{Non-negativity:} & \quad \text{buyquantity}_n \geq 0, \quad \text{sellquantity}_n \geq 0, \quad \text{stock}_n \geq 0, \quad \forall n = 1, \ldots, N \\
\text{Initial Condition:} & \quad \text{stock}_0 = 0 \\
\text{Final Condition:} & \quad \text{stock}_N = 0
\end{align*}

\end{document}
```

This linear programming model can be used to determine the optimal buying and selling strategy over the given time periods to maximize the profit while adhering to the warehouse capacity and holding cost constraints. Each decision variable and parameter is clearly defined, and the constraints ensure that the operational rules are followed.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Warehouse Management}

\subsection*{Decision Variables:}
\begin{itemize}
    \item \( \text{buyquantity}_n \): Quantity of commodity bought in period \( n \), for \( n = 1, \ldots, N \).
    \item \( \text{sellquantity}_n \): Quantity of commodity sold in period \( n \), for \( n = 1, \ldots, N \).
    \item \( \text{stock}_n \): Stock of commodity at the end of period \( n \), for \( n = 1, \ldots, N \).
\end{itemize}

\subsection*{Parameters:}
\begin{itemize}
    \item \text{capacity}: Maximum capacity of the warehouse.
    \item \text{holding\_cost}: Cost per unit for holding stock for one period.
    \item \text{price}_n: Selling price of the commodity in period \( n \).
    \item \text{cost}_n: Purchase cost of the commodity in period \( n \).
\end{itemize}

\subsection*{Objective Function:}
Maximize the profit over the periods:
\[
\text{Maximize} \quad \sum_{n=1}^{N} (\text{price}_n \times \text{sellquantity}_n - \text{cost}_n \times \text{buyquantity}_n - \text{holding\_cost} \times \text{stock}_n)
\]

\subsection*{Constraints:}
\begin{align*}
\text{Stock Balance:} & \quad \text{stock}_n = \text{stock}_{n-1} + \text{buyquantity}_n - \text{sellquantity}_n, \quad \forall n = 1, \ldots, N \\
\text{Capacity Constraint:} & \quad \text{stock}_n \leq \text{capacity}, \quad \forall n = 1, \ldots, N \\
\text{Non-negativity:} & \quad \text{buyquantity}_n \geq 0, \quad \text{sellquantity}_n \geq 0, \quad \text{stock}_n \geq 0, \quad \forall n = 1, \ldots, N \\
\text{Initial Condition:} & \quad \text{stock}_0 = 0 \\
\text{Final Condition:} & \quad \text{stock}_N = 0
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the provided JSON format
data = {
    'capacity': 10,
    'holding_cost': 2,
    'price': [1, 2, 100],
    'cost': [100, 1, 100]
}

N = len(data['price'])  #### Number of periods

#### Create a linear programming problem
problem = pulp.LpProblem("WarehouseManagement", pulp.LpMaximize)

#### Decision Variables
buyquantity = pulp.LpVariable.dicts("buyquantity", range(N), lowBound=0)  #### Quantity bought
sellquantity = pulp.LpVariable.dicts("sellquantity", range(N), lowBound=0)  #### Quantity sold
stock = pulp.LpVariable.dicts("stock", range(N + 1), lowBound=0)  #### Stock levels

#### Initial stock condition
problem += (stock[0] == 0)

#### Objective Function
problem += pulp.lpSum(data['price'][n] * sellquantity[n] - data['cost'][n] * buyquantity[n] - data['holding_cost'] * stock[n] for n in range(N))

#### Constraints
for n in range(N):
    #### Stock balance constraint
    problem += (stock[n + 1] == stock[n] + buyquantity[n] - sellquantity[n])
    
    #### Capacity constraint
    problem += (stock[n + 1] <= data['capacity'])

#### Final stock condition
problem += (stock[N] == 0)

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

