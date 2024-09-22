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
    \item $C$: Capacity of the warehouse
    \item $H$: Holding cost per unit for one period
    \item $P_n$: Selling price of the commodity in period $n$, for $n = 1, \ldots, N$
    \item $C_n$: Cost of purchasing the commodity in period $n$, for $n = 1, \ldots, N$
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $b_n$: Amount of buying in period $n$, for $n = 1, \ldots, N$
    \item $s_n$: Amount of selling in period $n$, for $n = 1, \ldots, N$
    \item $x_n$: Stock at the end of period $n$, for $n = 1, \ldots, N$
\end{itemize}

\subsection*{Objective Function}
Maximize total profit:
\[
\text{Maximize} \quad Z = \sum_{n=1}^{N} (P_n s_n - C_n b_n - H x_n)
\]

\subsection*{Subject to Constraints}
\begin{itemize}
    \item Stock balance equation:
    \[
    x_n = x_{n-1} + b_n - s_n \quad \text{for } n = 1, \ldots, N
    \]
    \item Capacity constraint:
    \[
    x_n \leq C  \quad \text{for } n = 1, \ldots, N
    \]
    \item Non-negativity constraints:
    \[
    b_n \geq 0, \quad s_n \geq 0, \quad x_n \geq 0 \quad \text{for } n = 1, \ldots, N
    \]
    \item Initial stock and final requirement:
    \[
    x_0 = 0 \quad \text{and} \quad x_N = 0
    \]
\end{itemize}

\subsection*{Output Variables}
\begin{itemize}
    \item $b_n$: Buy quantities for each period $n$, for $n = 1, \ldots, N$
    \item $s_n$: Sell quantities for each period $n$, for $n = 1, \ldots, N$
    \item $x_n$: Stock levels for each period $n$, for $n = 1, \ldots, N$
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

\section*{Mathematical Model for Warehouse Operations}

\subsection*{Parameters}
\begin{itemize}
    \item $C$: Capacity of the warehouse
    \item $H$: Holding cost per unit for one period
    \item $P_n$: Selling price of the commodity in period $n$, for $n = 1, \ldots, N$
    \item $C_n$: Cost of purchasing the commodity in period $n$, for $n = 1, \ldots, N$
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $b_n$: Amount of buying in period $n$, for $n = 1, \ldots, N$
    \item $s_n$: Amount of selling in period $n$, for $n = 1, \ldots, N$
    \item $x_n$: Stock at the end of period $n$, for $n = 1, \ldots, N$
\end{itemize}

\subsection*{Objective Function}
Maximize total profit:
\[
\text{Maximize} \quad Z = \sum_{n=1}^{N} (P_n s_n - C_n b_n - H x_n)
\]

\subsection*{Subject to Constraints}
\begin{itemize}
    \item Stock balance equation:
    \[
    x_n = x_{n-1} + b_n - s_n \quad \text{for } n = 1, \ldots, N
    \]
    \item Capacity constraint:
    \[
    x_n \leq C  \quad \text{for } n = 1, \ldots, N
    \]
    \item Non-negativity constraints:
    \[
    b_n \geq 0, \quad s_n \geq 0, \quad x_n \geq 0 \quad \text{for } n = 1, \ldots, N
    \]
    \item Initial stock and final requirement:
    \[
    x_0 = 0 \quad \text{and} \quad x_N = 0
    \]
\end{itemize}

\subsection*{Output Variables}
\begin{itemize}
    \item $b_n$: Buy quantities for each period $n$, for $n = 1, \ldots, N$
    \item $s_n$: Sell quantities for each period $n$, for $n = 1, \ldots, N$
    \item $x_n$: Stock levels for each period $n$, for $n = 1, \ldots, N$
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

#### Parameters
C = data['capacity']
H = data['holding_cost']
P = data['price']
C_n = data['cost']
N = len(P)

#### Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
b = pulp.LpVariable.dicts("Buy", range(N), lowBound=0, cat='Continuous')
s = pulp.LpVariable.dicts("Sell", range(N), lowBound=0, cat='Continuous')
x = pulp.LpVariable.dicts("Stock", range(N+1), lowBound=0, cat='Continuous')

#### Objective Function
profit = pulp.lpSum((P[n] * s[n] - C_n[n] * b[n] - H * x[n]) for n in range(N))
problem += profit

#### Constraints
problem += (x[0] == 0, "Initial_Stock")

for n in range(N):
    problem += (x[n+1] == x[n] + b[n] - s[n], f"Stock_Balance_{n}")
    problem += (x[n] <= C, f"Capacity_Constraint_{n}")

problem += (x[N] == 0, "Final_Stock")

#### Solve
problem.solve()

#### Output
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

