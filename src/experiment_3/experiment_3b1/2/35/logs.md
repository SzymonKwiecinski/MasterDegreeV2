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

\section*{Warehouse Operations Linear Programming Model}

\subsection*{Parameters}
\begin{itemize}
    \item $C$: Capacity of the warehouse
    \item $H$: Holding cost per unit for one period
    \item $P_n$: Selling price of the commodity in period $n$, for $n = 1, \ldots, N$
    \item $C_n$: Cost of purchasing the commodity in period $n$, for $n = 1, \ldots, N$
\end{itemize}

\subsection*{Variables}
\begin{itemize}
    \item $b_n$: Buy quantity in period $n$, for $n = 1, \ldots, N$
    \item $s_n$: Sell quantity in period $n$, for $n = 1, \ldots, N$
    \item $x_n$: Stock at the end of period $n$, for $n = 1, \ldots, N$
\end{itemize}

\subsection*{Objective Function}
Maximize total profit over the periods:
\[
\text{Maximize } Z = \sum_{n=1}^{N} \left( P_n s_n - C_n b_n - H x_n \right)
\]

\subsection*{Constraints}
1. Stock balance for each period:
\[
x_n = x_{n-1} + b_n - s_n \quad \text{for } n = 1, \ldots, N
\]
2. Capacity constraint:
\[
x_n \leq C \quad \text{for } n = 1, \ldots, N
\]
3. Non-negativity constraints:
\[
b_n \geq 0, \, s_n \geq 0, \, x_n \geq 0 \quad \text{for } n = 1, \ldots, N
\]
4. Warehouse empty at the end of the last period:
\[
x_N = 0
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

\section*{Warehouse Operations Linear Programming Model}

\subsection*{Parameters}
\begin{itemize}
    \item $C$: Capacity of the warehouse
    \item $H$: Holding cost per unit for one period
    \item $P_n$: Selling price of the commodity in period $n$, for $n = 1, \ldots, N$
    \item $C_n$: Cost of purchasing the commodity in period $n$, for $n = 1, \ldots, N$
\end{itemize}

\subsection*{Variables}
\begin{itemize}
    \item $b_n$: Buy quantity in period $n$, for $n = 1, \ldots, N$
    \item $s_n$: Sell quantity in period $n$, for $n = 1, \ldots, N$
    \item $x_n$: Stock at the end of period $n$, for $n = 1, \ldots, N$
\end{itemize}

\subsection*{Objective Function}
Maximize total profit over the periods:
\[
\text{Maximize } Z = \sum_{n=1}^{N} \left( P_n s_n - C_n b_n - H x_n \right)
\]

\subsection*{Constraints}
1. Stock balance for each period:
\[
x_n = x_{n-1} + b_n - s_n \quad \text{for } n = 1, \ldots, N
\]
2. Capacity constraint:
\[
x_n \leq C \quad \text{for } n = 1, \ldots, N
\]
3. Non-negativity constraints:
\[
b_n \geq 0, \, s_n \geq 0, \, x_n \geq 0 \quad \text{for } n = 1, \ldots, N
\]
4. Warehouse empty at the end of the last period:
\[
x_N = 0
\]

\end{document}</MATH_MODEL>
<DATA>
{'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data provided
data = {
    'capacity': 10,
    'holding_cost': 2,
    'price': [1, 2, 100],
    'cost': [100, 1, 100]
}

C = data['capacity']
H = data['holding_cost']
P = data['price']
C_cost = data['cost']

N = len(P)

#### Create the LP problem
problem = pulp.LpProblem("Warehouse_Operations", pulp.LpMaximize)

#### Variables
b = pulp.LpVariable.dicts("buy", range(N), lowBound=0, cat='Continuous')  #### Buy quantities
s = pulp.LpVariable.dicts("sell", range(N), lowBound=0, cat='Continuous')  #### Sell quantities
x = pulp.LpVariable.dicts("stock", range(N), lowBound=0, cat='Continuous')  #### Stock levels

#### Objective function
problem += pulp.lpSum(P[n] * s[n] - C_cost[n] * b[n] - H * x[n] for n in range(N)), "Total_Profit"

#### Constraints
#### Stock balance for each period
for n in range(N):
    if n == 0:
        problem += x[n] == b[n] - s[n], f"Stock_Balance_{n+1}"
    else:
        problem += x[n] == x[n-1] + b[n] - s[n], f"Stock_Balance_{n+1}"
    
    #### Capacity constraint
    problem += x[n] <= C, f"Capacity_Constraint_{n+1}"

#### Final stock should be zero
problem += x[N-1] == 0, "Final_Stock_Zero"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

