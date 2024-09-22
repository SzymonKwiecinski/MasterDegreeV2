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

\section*{Warehouse Operation Linear Programming Model}

\subsection*{Parameters}
\begin{itemize}
    \item Let \( C \) be the warehouse capacity.
    \item Let \( h \) be the holding cost per unit for one period.
    \item Let \( p_n \) be the selling price of the commodity in period \( n \).
    \item Let \( c_n \) be the purchase cost of the commodity in period \( n \).
    \item Let \( N \) be the total number of periods.
\end{itemize}

\subsection*{Variables}
\begin{itemize}
    \item Let \( b_n \) be the amount bought in period \( n \).
    \item Let \( s_n \) be the amount sold in period \( n \).
    \item Let \( x_n \) be the stock in the warehouse at the end of period \( n \).
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit over the periods:
\[
\text{Maximize } Z = \sum_{n=1}^{N} (p_n s_n - c_n b_n - h x_n)
\]

\subsection*{Constraints}
\begin{align*}
    1. & \quad x_n = x_{n-1} + b_n - s_n, \quad \forall n = 1, \ldots, N \\
    2. & \quad x_n \leq C, \quad \forall n = 1, \ldots, N \\
    3. & \quad x_N = 0 \\
    4. & \quad b_n \geq 0, \quad \forall n = 1, \ldots, N \\
    5. & \quad s_n \geq 0, \quad \forall n = 1, \ldots, N \\
\end{align*}

\subsection*{Output Variables}
The solution will provide:
\begin{itemize}
    \item \( b_n \): Amount of buying in each period \( n \).
    \item \( s_n \): Amount of selling in each period \( n \).
    \item \( x_n \): Stock in each period \( n \).
\end{itemize}

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

\section*{Warehouse Operation Linear Programming Model}

\subsection*{Parameters}
\begin{itemize}
    \item Let \( C \) be the warehouse capacity.
    \item Let \( h \) be the holding cost per unit for one period.
    \item Let \( p_n \) be the selling price of the commodity in period \( n \).
    \item Let \( c_n \) be the purchase cost of the commodity in period \( n \).
    \item Let \( N \) be the total number of periods.
\end{itemize}

\subsection*{Variables}
\begin{itemize}
    \item Let \( b_n \) be the amount bought in period \( n \).
    \item Let \( s_n \) be the amount sold in period \( n \).
    \item Let \( x_n \) be the stock in the warehouse at the end of period \( n \).
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit over the periods:
\[
\text{Maximize } Z = \sum_{n=1}^{N} (p_n s_n - c_n b_n - h x_n)
\]

\subsection*{Constraints}
\begin{align*}
    1. & \quad x_n = x_{n-1} + b_n - s_n, \quad \forall n = 1, \ldots, N \\
    2. & \quad x_n \leq C, \quad \forall n = 1, \ldots, N \\
    3. & \quad x_N = 0 \\
    4. & \quad b_n \geq 0, \quad \forall n = 1, \ldots, N \\
    5. & \quad s_n \geq 0, \quad \forall n = 1, \ldots, N \\
\end{align*}

\subsection*{Output Variables}
The solution will provide:
\begin{itemize}
    \item \( b_n \): Amount of buying in each period \( n \).
    \item \( s_n \): Amount of selling in each period \( n \).
    \item \( x_n \): Stock in each period \( n \).
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON
data = {'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}

#### Extracting parameters
C = data['capacity']
h = data['holding_cost']
p = data['price']
c = data['cost']
N = len(p)

#### Define the LP problem
problem = pulp.LpProblem("WarehouseOperation", pulp.LpMaximize)

#### Define variables
b = [pulp.LpVariable(f'b_{n}', lowBound=0, cat='Continuous') for n in range(N)]
s = [pulp.LpVariable(f's_{n}', lowBound=0, cat='Continuous') for n in range(N)]
x = [pulp.LpVariable(f'x_{n}', lowBound=0, cat='Continuous') for n in range(N)]

#### Objective function
problem += pulp.lpSum([p[n] * s[n] - c[n] * b[n] - h * x[n] for n in range(N)])

#### Constraints
#### Initial stock is assumed zero
problem += (x[0] == b[0] - s[0], "InitialStockConstraint")

#### Inventory balance constraints
for n in range(1, N):
    problem += (x[n] == x[n-1] + b[n] - s[n], f"StockBalanceConstraint_{n}")

#### Capacity constraints
for n in range(N):
    problem += (x[n] <= C, f"CapacityConstraint_{n}")

#### Final stock constraint
problem += (x[N-1] == 0, "FinalStockConstraint")

#### Solve the problem
problem.solve()

#### Output the solution
for n in range(N):
    print(f"Period {n+1}: Buy = {pulp.value(b[n])}, Sell = {pulp.value(s[n])}, Stock = {pulp.value(x[n])}")

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

