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

\textbf{Parameters:}
\begin{itemize}
    \item Let \( C \) be the capacity of the warehouse.
    \item Let \( h \) be the holding cost per unit for one period.
    \item Let \( p_n \) be the selling price of the commodity in period \( n \) for \( n = 1, 2, \ldots, N \).
    \item Let \( c_n \) be the purchase cost of the commodity in period \( n \) for \( n = 1, 2, \ldots, N \).
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item Let \( x_n \) be the amount of buying in period \( n \).
    \item Let \( y_n \) be the amount of selling in period \( n \).
    \item Let \( s_n \) be the stock at the end of period \( n \) (excluding initial stock).
\end{itemize}

\textbf{Objective Function:}
\[
\text{Maximize } Z = \sum_{n=1}^{N} (p_n y_n - c_n x_n - h s_n)
\]

\textbf{Constraints:}
\begin{align*}
    s_n &= s_{n-1} + x_n - y_n, & \text{for } n = 1, 2, \ldots, N \\
    s_n &\leq C, & \text{for } n = 1, 2, \ldots, N \\
    s_N &= 0, & \text{(final stock must be zero)} \\
    x_n &\geq 0, & \text{(buying must be non-negative)} \\
    y_n &\geq 0, & \text{(selling must be non-negative)} \\
\end{align*}

\textbf{Initial Condition:}
\[
s_0 = 0 \quad \text{(the warehouse starts empty)}
\]

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

\textbf{Parameters:}
\begin{itemize}
    \item Let \( C \) be the capacity of the warehouse.
    \item Let \( h \) be the holding cost per unit for one period.
    \item Let \( p_n \) be the selling price of the commodity in period \( n \) for \( n = 1, 2, \ldots, N \).
    \item Let \( c_n \) be the purchase cost of the commodity in period \( n \) for \( n = 1, 2, \ldots, N \).
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item Let \( x_n \) be the amount of buying in period \( n \).
    \item Let \( y_n \) be the amount of selling in period \( n \).
    \item Let \( s_n \) be the stock at the end of period \( n \) (excluding initial stock).
\end{itemize}

\textbf{Objective Function:}
\[
\text{Maximize } Z = \sum_{n=1}^{N} (p_n y_n - c_n x_n - h s_n)
\]

\textbf{Constraints:}
\begin{align*}
    s_n &= s_{n-1} + x_n - y_n, & \text{for } n = 1, 2, \ldots, N \\
    s_n &\leq C, & \text{for } n = 1, 2, \ldots, N \\
    s_N &= 0, & \text{(final stock must be zero)} \\
    x_n &\geq 0, & \text{(buying must be non-negative)} \\
    y_n &\geq 0, & \text{(selling must be non-negative)} \\
\end{align*}

\textbf{Initial Condition:}
\[
s_0 = 0 \quad \text{(the warehouse starts empty)}
\]

\end{document}</MATH_MODEL>
<DATA>
{'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the provided JSON-like structure
data = {
    'capacity': 10,
    'holding_cost': 2,
    'price': [1, 2, 100],
    'cost': [100, 1, 100]
}

#### Parameters
C = data['capacity']           #### Capacity of the warehouse
h = data['holding_cost']       #### Holding cost per unit
p = data['price']              #### Selling price per period
c = data['cost']               #### Purchase cost per period
N = len(p)                     #### Number of periods

#### Create the Linear Program
problem = pulp.LpProblem("Warehouse_Operations", pulp.LpMaximize)

#### Decision Variables
x = pulp.LpVariable.dicts("Buy", range(1, N + 1), lowBound=0)  #### Buying amounts
y = pulp.LpVariable.dicts("Sell", range(1, N + 1), lowBound=0) #### Selling amounts
s = pulp.LpVariable.dicts("Stock", range(1, N + 1), lowBound=0) #### Stock at the end of each period

#### Objective Function
problem += pulp.lpSum(p[n - 1] * y[n] - c[n - 1] * x[n] - h * s[n] for n in range(1, N + 1))

#### Constraints
s[1] = pulp.LpVariable("InitialStock", lowBound=0)  #### Initial stock at period 1
problem += s[1] == 0  #### The warehouse starts empty

for n in range(1, N + 1):
    if n > 1:
        problem += s[n] == s[n - 1] + x[n] - y[n]

    problem += s[n] <= C  #### Stock should not exceed capacity
    if n == N:
        problem += s[n] == 0  #### Final stock must be zero

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

