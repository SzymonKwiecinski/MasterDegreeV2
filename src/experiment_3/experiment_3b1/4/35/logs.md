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

\subsection*{Parameters}
\begin{itemize}
    \item $C$: warehouse capacity
    \item $h$: holding cost per unit per period
    \item $p_n$: selling price of the commodity in period $n$ for $n = 1, \ldots, N$
    \item $c_n$: buying cost of the commodity in period $n$ for $n = 1, \ldots, N$
    \item $b_n$: buy quantity in period $n$ for $n = 1, \ldots, N$
    \item $s_n$: sell quantity in period $n$ for $n = 1, \ldots, N$
    \item $x_n$: stock at the end of period $n$ for $n = 1, \ldots, N$
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $b_n$: amount bought in period $n$ 
    \item $s_n$: amount sold in period $n$ 
    \item $x_n$: stock remaining at the end of period $n$
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit over $N$ periods:
\[
\text{Maximize } Z = \sum_{n=1}^{N} \left( p_n s_n - c_n b_n - h x_n \right)
\]

\subsection*{Constraints}
\begin{align*}
    x_0 & = 0 \quad \text{(initial stock is zero)} \\
    x_n & = x_{n-1} + b_n - s_n \quad \forall n = 1, \ldots, N \\
    x_n & \leq C \quad \forall n = 1, \ldots, N \\
    x_N & = 0 \quad \text{(final stock must be zero)} \\
    b_n & \geq 0 \quad \forall n = 1, \ldots, N \\
    s_n & \geq 0 \quad \forall n = 1, \ldots, N \\
\end{align*}

\subsection*{Output Format}
\begin{itemize}
    \item \texttt{buyquantity}: $[b_n \text{ for } n = 1,\ldots,N]$
    \item \texttt{sellquantity}: $[s_n \text{ for } n = 1,\ldots,N]$
    \item \texttt{stock}: $[x_n \text{ for } n = 1,\ldots,N]$
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

\subsection*{Parameters}
\begin{itemize}
    \item $C$: warehouse capacity
    \item $h$: holding cost per unit per period
    \item $p_n$: selling price of the commodity in period $n$ for $n = 1, \ldots, N$
    \item $c_n$: buying cost of the commodity in period $n$ for $n = 1, \ldots, N$
    \item $b_n$: buy quantity in period $n$ for $n = 1, \ldots, N$
    \item $s_n$: sell quantity in period $n$ for $n = 1, \ldots, N$
    \item $x_n$: stock at the end of period $n$ for $n = 1, \ldots, N$
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $b_n$: amount bought in period $n$ 
    \item $s_n$: amount sold in period $n$ 
    \item $x_n$: stock remaining at the end of period $n$
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit over $N$ periods:
\[
\text{Maximize } Z = \sum_{n=1}^{N} \left( p_n s_n - c_n b_n - h x_n \right)
\]

\subsection*{Constraints}
\begin{align*}
    x_0 & = 0 \quad \text{(initial stock is zero)} \\
    x_n & = x_{n-1} + b_n - s_n \quad \forall n = 1, \ldots, N \\
    x_n & \leq C \quad \forall n = 1, \ldots, N \\
    x_N & = 0 \quad \text{(final stock must be zero)} \\
    b_n & \geq 0 \quad \forall n = 1, \ldots, N \\
    s_n & \geq 0 \quad \forall n = 1, \ldots, N \\
\end{align*}

\subsection*{Output Format}
\begin{itemize}
    \item \texttt{buyquantity}: $[b_n \text{ for } n = 1,\ldots,N]$
    \item \texttt{sellquantity}: $[s_n \text{ for } n = 1,\ldots,N]$
    \item \texttt{stock}: $[x_n \text{ for } n = 1,\ldots,N]$
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data from the input
data = json.loads('{"capacity": 10, "holding_cost": 2, "price": [1, 2, 100], "cost": [100, 1, 100]}')

#### Parameters
C = data['capacity']
h = data['holding_cost']
p = data['price']
c = data['cost']
N = len(p)

#### Create the problem
problem = pulp.LpProblem("Warehouse_Operation", pulp.LpMaximize)

#### Decision Variables
b = pulp.LpVariable.dicts("buy_quantity", range(N), lowBound=0, cat='Continuous')
s = pulp.LpVariable.dicts("sell_quantity", range(N), lowBound=0, cat='Continuous')
x = pulp.LpVariable.dicts("stock", range(N), lowBound=0, upBound=C, cat='Continuous')

#### Objective function
problem += pulp.lpSum(p[n] * s[n] - c[n] * b[n] - h * x[n] for n in range(N))

#### Constraints
problem += (x[0] == 0, "Initial_Stock_Zero")

for n in range(1, N):
    problem += (x[n] == x[n-1] + b[n-1] - s[n-1], f"Stock_Balance_{n}")

for n in range(N):
    problem += (x[n] <= C, f"Capacity_Constraint_{n}")

problem += (x[N-1] == 0, "Final_Stock_Zero")

#### Solve the problem
problem.solve()

#### Output results
buyquantity = [b[n].varValue for n in range(N)]
sellquantity = [s[n].varValue for n in range(N)]
stock = [x[n].varValue for n in range(N)]

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(f'Buy Quantity: {buyquantity}')
print(f'Sell Quantity: {sellquantity}')
print(f'Stock: {stock}')
```

