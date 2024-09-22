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

\section*{Linear Programming Model for Warehouse Operation}

\subsection*{Parameters}
\begin{itemize}
    \item Let $\text{capacity}$ be the maximum stock capacity of the warehouse.
    \item Let $\text{holding\_cost}$ be the cost per unit of holding stock for one period.
    \item Let $\text{price}_n$ be the selling price of the commodity at period $n$, for $n = 1, \ldots, N$.
    \item Let $\text{cost}_n$ be the purchase cost of the commodity at period $n$, for $n = 1, \ldots, N$.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item Let $b_n$ be the buy quantity in period $n$, for $n = 1, \ldots, N$.
    \item Let $s_n$ be the sell quantity in period $n$, for $n = 1, \ldots, N$.
    \item Let $x_n$ be the stock in period $n$, for $n = 1, \ldots, N$.
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit over the $N$ periods:
\[
\text{Maximize } Z = \sum_{n=1}^{N} \left( (price_n - cost_n) s_n - holding\_cost \cdot x_n \right)
\]

\subsection*{Constraints}
1. \text{Stock Balance Equation:}
\[
x_n = x_{n-1} + b_n - s_n, \quad \forall n = 1, \ldots, N
\]
where $x_0 = 0$ (initial stock is empty).

2. \text{Stock Capacity Constraint:}
\[
x_n \leq capacity, \quad \forall n = 1, \ldots, N
\]

3. \text{Non-negativity Constraints:}
\[
b_n \geq 0, \quad s_n \geq 0, \quad x_n \geq 0, \quad \forall n = 1, \ldots, N
\]

4. \text{Final Stock Constraint:}
\[
x_N = 0
\]

\subsection*{Output Format}
The solution will yield:
\begin{itemize}
    \item $b_n$ representing the buy quantity in each period.
    \item $s_n$ representing the sell quantity in each period.
    \item $x_n$ representing the stock in each period.
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

\section*{Linear Programming Model for Warehouse Operation}

\subsection*{Parameters}
\begin{itemize}
    \item Let $\text{capacity}$ be the maximum stock capacity of the warehouse.
    \item Let $\text{holding\_cost}$ be the cost per unit of holding stock for one period.
    \item Let $\text{price}_n$ be the selling price of the commodity at period $n$, for $n = 1, \ldots, N$.
    \item Let $\text{cost}_n$ be the purchase cost of the commodity at period $n$, for $n = 1, \ldots, N$.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item Let $b_n$ be the buy quantity in period $n$, for $n = 1, \ldots, N$.
    \item Let $s_n$ be the sell quantity in period $n$, for $n = 1, \ldots, N$.
    \item Let $x_n$ be the stock in period $n$, for $n = 1, \ldots, N$.
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit over the $N$ periods:
\[
\text{Maximize } Z = \sum_{n=1}^{N} \left( (price_n - cost_n) s_n - holding\_cost \cdot x_n \right)
\]

\subsection*{Constraints}
1. \text{Stock Balance Equation:}
\[
x_n = x_{n-1} + b_n - s_n, \quad \forall n = 1, \ldots, N
\]
where $x_0 = 0$ (initial stock is empty).

2. \text{Stock Capacity Constraint:}
\[
x_n \leq capacity, \quad \forall n = 1, \ldots, N
\]

3. \text{Non-negativity Constraints:}
\[
b_n \geq 0, \quad s_n \geq 0, \quad x_n \geq 0, \quad \forall n = 1, \ldots, N
\]

4. \text{Final Stock Constraint:}
\[
x_N = 0
\]

\subsection*{Output Format}
The solution will yield:
\begin{itemize}
    \item $b_n$ representing the buy quantity in each period.
    \item $s_n$ representing the sell quantity in each period.
    \item $x_n$ representing the stock in each period.
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data input
data = json.loads('{"capacity": 10, "holding_cost": 2, "price": [1, 2, 100], "cost": [100, 1, 100]}')
capacity = data['capacity']
holding_cost = data['holding_cost']
price = data['price']
cost = data['cost']
N = len(price)

#### Create the linear programming problem
problem = pulp.LpProblem("Warehouse_Operation", pulp.LpMaximize)

#### Decision Variables
b = pulp.LpVariable.dicts("buy_quantity", range(N), lowBound=0)  #### Buy quantities
s = pulp.LpVariable.dicts("sell_quantity", range(N), lowBound=0)  #### Sell quantities
x = pulp.LpVariable.dicts("stock", range(N), lowBound=0, upBound=capacity)  #### Stock levels

#### Objective Function
problem += pulp.lpSum((price[n] - cost[n]) * s[n] - holding_cost * x[n] for n in range(N)), "Total_Profit"

#### Constraints
#### Stock Balance Equation
for n in range(N):
    if n == 0:
        problem += x[n] == b[n] - s[n], f"Stock_Balance_{n+1}"
    else:
        problem += x[n] == x[n-1] + b[n] - s[n], f"Stock_Balance_{n+1}"

#### Final Stock Constraint
problem += x[N-1] == 0, "Final_Stock_Constraint"

#### Solve the problem
problem.solve()

#### Print the results
for n in range(N):
    print(f"Buy quantity in period {n+1}: {b[n].varValue}")
    print(f"Sell quantity in period {n+1}: {s[n].varValue}")
    print(f"Stock in period {n+1}: {x[n].varValue}")

#### Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

