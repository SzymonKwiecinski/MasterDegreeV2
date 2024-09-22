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

\section*{Mathematical Model for Warehouse Operation}

\textbf{Parameters:}
\begin{itemize}
    \item $C$: Capacity of the warehouse
    \item $h$: Holding cost per unit per period
    \item $p_n$: Selling price of the commodity in period $n$ for $n = 1, \ldots, N$
    \item $c_n$: Cost to purchase the commodity in period $n$ for $n = 1, \ldots, N$
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $b_n$: Buy quantity in period $n$ for $n = 1, \ldots, N$
    \item $s_n$: Sell quantity in period $n$ for $n = 1, \ldots, N$
    \item $x_n$: Stock in period $n$ for $n = 1, \ldots, N$
\end{itemize}

\textbf{Objective Function:}
Maximize profit over all periods:
\[
\text{Maximize } Z = \sum_{n=1}^{N} (p_n s_n - c_n b_n - h x_n)
\]

\textbf{Constraints:}
\begin{align*}
    x_1 & = b_1 - s_1 \\
    x_n & = x_{n-1} + b_n - s_n, \quad n = 2, \ldots, N \\
    x_n & \leq C, \quad n = 1, \ldots, N \\
    s_n & \leq x_n, \quad n = 1, \ldots, N \\
    x_N & = 0 \\
    b_n, s_n & \geq 0, \quad n = 1, \ldots, N
\end{align*}

\textbf{Output Variables:}
The solution should provide:
\begin{itemize}
    \item $buyquantity = [b_1, b_2, \ldots, b_N]$
    \item $sellquantity = [s_1, s_2, \ldots, s_N]$
    \item $stock = [x_1, x_2, \ldots, x_N]$
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

\section*{Mathematical Model for Warehouse Operation}

\textbf{Parameters:}
\begin{itemize}
    \item $C$: Capacity of the warehouse
    \item $h$: Holding cost per unit per period
    \item $p_n$: Selling price of the commodity in period $n$ for $n = 1, \ldots, N$
    \item $c_n$: Cost to purchase the commodity in period $n$ for $n = 1, \ldots, N$
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $b_n$: Buy quantity in period $n$ for $n = 1, \ldots, N$
    \item $s_n$: Sell quantity in period $n$ for $n = 1, \ldots, N$
    \item $x_n$: Stock in period $n$ for $n = 1, \ldots, N$
\end{itemize}

\textbf{Objective Function:}
Maximize profit over all periods:
\[
\text{Maximize } Z = \sum_{n=1}^{N} (p_n s_n - c_n b_n - h x_n)
\]

\textbf{Constraints:}
\begin{align*}
    x_1 & = b_1 - s_1 \\
    x_n & = x_{n-1} + b_n - s_n, \quad n = 2, \ldots, N \\
    x_n & \leq C, \quad n = 1, \ldots, N \\
    s_n & \leq x_n, \quad n = 1, \ldots, N \\
    x_N & = 0 \\
    b_n, s_n & \geq 0, \quad n = 1, \ldots, N
\end{align*}

\textbf{Output Variables:}
The solution should provide:
\begin{itemize}
    \item $buyquantity = [b_1, b_2, \ldots, b_N]$
    \item $sellquantity = [s_1, s_2, \ldots, s_N]$
    \item $stock = [x_1, x_2, \ldots, x_N]$
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON format
data = {'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}
C = data['capacity']
h = data['holding_cost']
p = data['price']
c = data['cost']
N = len(p)

#### Create a linear programming problem
problem = pulp.LpProblem("WarehouseOperation", pulp.LpMaximize)

#### Decision Variables
b = pulp.LpVariable.dicts("BuyQuantity", range(1, N + 1), lowBound=0)  #### b_n
s = pulp.LpVariable.dicts("SellQuantity", range(1, N + 1), lowBound=0)  #### s_n
x = pulp.LpVariable.dicts("Stock", range(1, N + 1), lowBound=0, upBound=C)  #### x_n

#### Objective function: Maximize profit
problem += pulp.lpSum(p[n - 1] * s[n] - c[n - 1] * b[n] - h * x[n] for n in range(1, N + 1))

#### Constraints
problem += (x[1] == b[1] - s[1])  #### x_1 = b_1 - s_1
for n in range(2, N + 1):
    problem += (x[n] == x[n - 1] + b[n] - s[n])  #### x_n = x_{n-1} + b_n - s_n

for n in range(1, N + 1):
    problem += (x[n] <= C)  #### x_n <= C
    problem += (s[n] <= x[n])  #### s_n <= x_n

problem += (x[N] == 0)  #### x_N = 0

#### Solve the problem
problem.solve()

#### Output results
buyquantity = [b[n].varValue for n in range(1, N + 1)]
sellquantity = [s[n].varValue for n in range(1, N + 1)]
stock = [x[n].varValue for n in range(1, N + 1)]

print(f'Buy Quantity: {buyquantity}')
print(f'Sell Quantity: {sellquantity}')
print(f'Stock: {stock}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

