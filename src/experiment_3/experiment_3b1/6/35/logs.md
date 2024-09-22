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
    \item \( C \): Capacity of the warehouse
    \item \( h \): Holding cost per unit for one period
    \item \( p_n \): Selling price of the commodity in period \( n \)
    \item \( c_n \): Cost of purchasing the commodity in period \( n \)
    \item \( N \): Total number of periods
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( x_n \): Buy quantity in period \( n \)
    \item \( y_n \): Sell quantity in period \( n \)
    \item \( S_n \): Stock at the end of period \( n \)
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit over all periods:
\[
\text{Maximize} \quad Z = \sum_{n=1}^{N} (p_n \cdot y_n - c_n \cdot x_n - h \cdot S_n)
\]

\subsection*{Constraints}
1. Capacity constraint:
\[
S_n \leq C \quad \forall n \in \{1, 2, \ldots, N\}
\]

2. Stock balance equation:
\[
S_n = S_{n-1} + x_n - y_n \quad \forall n \in \{1, 2, \ldots, N\}
\]
where \( S_0 = 0 \) (initially empty).

3. Non-negativity constraints:
\[
x_n \geq 0, \quad y_n \geq 0, \quad S_n \geq 0 \quad \forall n \in \{1, 2, \ldots, N\}
\]

4. Final stock must be zero:
\[
S_N = 0
\]

\subsection*{Output Variables}
The outputs are:
\begin{itemize}
    \item \( \text{buyquantity} = [x_n \text{ for } n = 1, \ldots, N] \)
    \item \( \text{sellquantity} = [y_n \text{ for } n = 1, \ldots, N] \)
    \item \( \text{stock} = [S_n \text{ for } n = 1, \ldots, N] \)
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
    \item \( C \): Capacity of the warehouse
    \item \( h \): Holding cost per unit for one period
    \item \( p_n \): Selling price of the commodity in period \( n \)
    \item \( c_n \): Cost of purchasing the commodity in period \( n \)
    \item \( N \): Total number of periods
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( x_n \): Buy quantity in period \( n \)
    \item \( y_n \): Sell quantity in period \( n \)
    \item \( S_n \): Stock at the end of period \( n \)
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit over all periods:
\[
\text{Maximize} \quad Z = \sum_{n=1}^{N} (p_n \cdot y_n - c_n \cdot x_n - h \cdot S_n)
\]

\subsection*{Constraints}
1. Capacity constraint:
\[
S_n \leq C \quad \forall n \in \{1, 2, \ldots, N\}
\]

2. Stock balance equation:
\[
S_n = S_{n-1} + x_n - y_n \quad \forall n \in \{1, 2, \ldots, N\}
\]
where \( S_0 = 0 \) (initially empty).

3. Non-negativity constraints:
\[
x_n \geq 0, \quad y_n \geq 0, \quad S_n \geq 0 \quad \forall n \in \{1, 2, \ldots, N\}
\]

4. Final stock must be zero:
\[
S_N = 0
\]

\subsection*{Output Variables}
The outputs are:
\begin{itemize}
    \item \( \text{buyquantity} = [x_n \text{ for } n = 1, \ldots, N] \)
    \item \( \text{sellquantity} = [y_n \text{ for } n = 1, \ldots, N] \)
    \item \( \text{stock} = [S_n \text{ for } n = 1, \ldots, N] \)
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Given data in JSON format
data = json.loads('{"capacity": 10, "holding_cost": 2, "price": [1, 2, 100], "cost": [100, 1, 100]}')

#### Extracting data
C = data['capacity']
h = data['holding_cost']
p = data['price']
c = data['cost']
N = len(p)

#### Create the problem
problem = pulp.LpProblem("Warehouse_Operations", pulp.LpMaximize)

#### Decision variables
x = pulp.LpVariable.dicts("Buy_Quantity", range(1, N + 1), lowBound=0, cat='Continuous')
y = pulp.LpVariable.dicts("Sell_Quantity", range(1, N + 1), lowBound=0, cat='Continuous')
S = pulp.LpVariable.dicts("Stock", range(0, N + 1), lowBound=0, cat='Continuous')

#### Objective function
problem += pulp.lpSum(p[n - 1] * y[n] - c[n - 1] * x[n] - h * S[n] for n in range(1, N + 1))

#### Constraints
#### Capacity constraint
for n in range(1, N + 1):
    problem += S[n] <= C

#### Stock balance equation
for n in range(1, N + 1):
    if n == 1:
        problem += S[n] == x[n] - y[n]
    else:
        problem += S[n] == S[n - 1] + x[n] - y[n]

#### Final stock must be zero
problem += S[N] == 0

#### Solve the problem
problem.solve()

#### Print results
buy_quantity = [x[n].varValue for n in range(1, N + 1)]
sell_quantity = [y[n].varValue for n in range(1, N + 1)]
stock = [S[n].varValue for n in range(0, N + 1)]

print(f'Buy Quantity: {buy_quantity}')
print(f'Sell Quantity: {sell_quantity}')
print(f'Stock: {stock}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

