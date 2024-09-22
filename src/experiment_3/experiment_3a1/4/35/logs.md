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

\section*{Mathematical Model for Warehouse Operations}

\subsection*{Parameters}
\begin{itemize}
    \item \( C \): Warehouse capacity
    \item \( H \): Holding cost per unit for one period
    \item \( P_n \): Selling price of the commodity in period \( n \)
    \item \( C_n \): Purchase cost of the commodity in period \( n \)
    \item \( N \): Total number of periods
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( b_n \): Buy quantity in period \( n \)
    \item \( s_n \): Sell quantity in period \( n \)
    \item \( x_n \): Stock quantity at the end of period \( n \)
\end{itemize}

\subsection*{Objective Function}
Maximize total profit over \( N \) periods:

\[
\text{Maximize } Z = \sum_{n=1}^{N} (P_n \cdot s_n - C_n \cdot b_n - H \cdot x_n)
\]

\subsection*{Constraints}
\begin{align*}
    x_1 &= b_1 - s_1 \\
    x_n &= x_{n-1} + b_n - s_n & \text{for } n = 2, \ldots, N \\
    x_n &\leq C & \text{for } n = 1, \ldots, N \\
    s_n &\leq x_n & \text{for } n = 1, \ldots, N \\
    x_N &= 0 \\
    b_n, s_n &\geq 0 & \text{for } n = 1, \ldots, N
\end{align*}

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

\section*{Mathematical Model for Warehouse Operations}

\subsection*{Parameters}
\begin{itemize}
    \item \( C \): Warehouse capacity
    \item \( H \): Holding cost per unit for one period
    \item \( P_n \): Selling price of the commodity in period \( n \)
    \item \( C_n \): Purchase cost of the commodity in period \( n \)
    \item \( N \): Total number of periods
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( b_n \): Buy quantity in period \( n \)
    \item \( s_n \): Sell quantity in period \( n \)
    \item \( x_n \): Stock quantity at the end of period \( n \)
\end{itemize}

\subsection*{Objective Function}
Maximize total profit over \( N \) periods:

\[
\text{Maximize } Z = \sum_{n=1}^{N} (P_n \cdot s_n - C_n \cdot b_n - H \cdot x_n)
\]

\subsection*{Constraints}
\begin{align*}
    x_1 &= b_1 - s_1 \\
    x_n &= x_{n-1} + b_n - s_n & \text{for } n = 2, \ldots, N \\
    x_n &\leq C & \text{for } n = 1, \ldots, N \\
    s_n &\leq x_n & \text{for } n = 1, \ldots, N \\
    x_N &= 0 \\
    b_n, s_n &\geq 0 & \text{for } n = 1, \ldots, N
\end{align*}

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

#### Parameters
C = data['capacity']
H = data['holding_cost']
P = data['price']
C_cost = data['cost']
N = len(P)

#### Create a linear programming problem
problem = pulp.LpProblem("Warehouse_Optimization", pulp.LpMaximize)

#### Decision Variables
b = pulp.LpVariable.dicts("Buy", range(1, N + 1), lowBound=0)  #### Buy quantities
s = pulp.LpVariable.dicts("Sell", range(1, N + 1), lowBound=0)  #### Sell quantities
x = pulp.LpVariable.dicts("Stock", range(1, N + 1), lowBound=0, upBound=C)  #### Stock quantities

#### Objective Function
problem += pulp.lpSum(P[n - 1] * s[n] - C_cost[n - 1] * b[n] - H * x[n] for n in range(1, N + 1)), "Total_Profit"

#### Constraints
problem += x[1] == b[1] - s[1], "Stock_1"
for n in range(2, N + 1):
    problem += x[n] == x[n - 1] + b[n] - s[n], f"Stock_{n}"

for n in range(1, N + 1):
    problem += x[n] <= C, f"Capacity_{n}"
    problem += s[n] <= x[n], f"Sell_Not_Greater_Than_Stock_{n}"

problem += x[N] == 0, "No_Stock_End"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

