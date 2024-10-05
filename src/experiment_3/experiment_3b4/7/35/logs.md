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
To model the given warehouse operation problem as a Linear Programming (LP) problem, we need to consider the decision variables, constraints, and the objective function. Let's define:

- \( x_n \) as the amount of commodity bought in period \( n \).
- \( y_n \) as the amount of commodity sold in period \( n \).
- \( s_n \) as the stock at the end of period \( n \).

Given:
- The objective is to maximize profit over \( N \) periods.
- The warehouse capacity is limited to \texttt{capacity}.
- There is a holding cost \texttt{holding_cost} for keeping stock.
- The selling price in period \( n \) is \( \texttt{price}[n-1] \) and the cost of purchasing is \( \texttt{cost}[n-1] \).

The objective function (profit maximization) is formulated as:

\[
\text{Maximize} \quad \sum_{n=1}^{N} \left( \texttt{price}[n-1] \cdot y_n - \texttt{cost}[n-1] \cdot x_n - \texttt{holding_cost} \cdot s_n \right)
\]

Subject to the following constraints:

1. **Stock Balance**: For each period \( n \),
   \[
   s_{n} = s_{n-1} + x_n - y_n \quad \text{for} \quad n=1,...,N
   \]
   where \( s_0 = 0 \).

2. **Capacity Constraint**: The stock in any period cannot exceed the capacity:
   \[
   0 \leq s_n \leq \texttt{capacity} \quad \text{for} \quad n=1,...,N
   \]

3. **Non-Negativity**: The amount bought, sold, and the stock should be non-negative:
   \[
   x_n \geq 0, \quad y_n \geq 0, \quad s_n \geq 0 \quad \text{for} \quad n=1,...,N
   \]

4. **Final Stock Condition**: The warehouse needs to be empty at the end of the last period:
   \[
   s_N = 0
   \]

Here is the LaTeX representation of the LP formulation:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:}
\[
\text{Maximize} \quad \sum_{n=1}^{N} \left( \texttt{price}[n-1] \cdot y_n - \texttt{cost}[n-1] \cdot x_n - \texttt{holding_cost} \cdot s_n \right)
\]

\textbf{Subject to:}

\text{Stock balance:}
\[
s_{n} = s_{n-1} + x_n - y_n \quad \forall n=1,...,N, \quad s_0 = 0
\]

\text{Capacity constraint:}
\[
0 \leq s_n \leq \texttt{capacity} \quad \forall n=1,...,N
\]

\text{Non-negativity:}
\[
x_n \geq 0, \quad y_n \geq 0, \quad s_n \geq 0 \quad \forall n=1,...,N
\]

\text{Final stock condition:}
\[
s_N = 0
\]

\end{document}
```

This LP model can be solved using appropriate optimization software or solvers that handle linear programming problems. Upon solving, the outputs will be the optimal values for `buyquantity`, `sellquantity`, and `stock` for each period, aiming to maximize the overall profit.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:}
\[
\text{Maximize} \quad \sum_{n=1}^{N} \left( \texttt{price}[n-1] \cdot y_n - \texttt{cost}[n-1] \cdot x_n - \texttt{holding_cost} \cdot s_n \right)
\]

\textbf{Subject to:}

\text{Stock balance:}
\[
s_{n} = s_{n-1} + x_n - y_n \quad \forall n=1,...,N, \quad s_0 = 0
\]

\text{Capacity constraint:}
\[
0 \leq s_n \leq \texttt{capacity} \quad \forall n=1,...,N
\]

\text{Non-negativity:}
\[
x_n \geq 0, \quad y_n \geq 0, \quad s_n \geq 0 \quad \forall n=1,...,N
\]

\text{Final stock condition:}
\[
s_N = 0
\]

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

N = len(data['price'])

#### Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
x = [pulp.LpVariable(f"x_{n}", lowBound=0, cat='Continuous') for n in range(N)]
y = [pulp.LpVariable(f"y_{n}", lowBound=0, cat='Continuous') for n in range(N)]
s = [pulp.LpVariable(f"s_{n}", lowBound=0, cat='Continuous') for n in range(N+1)]

#### Set s_0 to 0
problem += (s[0] == 0)

#### Objective Function
problem += pulp.lpSum(data['price'][n] * y[n] - data['cost'][n] * x[n] - data['holding_cost'] * s[n+1] for n in range(N))

#### Constraints
for n in range(N):
    #### Stock balance constraint
    problem += (s[n+1] == s[n] + x[n] - y[n])
    #### Capacity constraint
    problem += (s[n+1] <= data['capacity'])

#### Final stock condition
problem += (s[N] == 0)

#### Solve
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

