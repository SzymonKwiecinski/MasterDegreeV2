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
To solve this problem, we'll formulate a linear programming model to determine the optimal buying and selling quantities in order to maximize profit. Let's denote the following:

- Let \( x_n \) be the amount bought in period \( n \).
- Let \( y_n \) be the amount sold in period \( n \).
- Let \( s_n \) be the stock at the end of period \( n \).

We need to maximize the total profit, which is given by the total revenue from sales minus the cost of buying and the holding cost of stock.

######### Objective Function
\[
\text{Maximize } \sum_{n=1}^{N} (price_{n} \times y_n - cost_{n} \times x_n) - \sum_{n=1}^{N} (holding\_cost \times s_n)
\]

######### Constraints
1. **Stock Capacity Constraint**: The stock at the end of each period should not exceed the warehouse capacity.
   \[
   s_n \leq \text{capacity}, \quad \forall n = 1, \ldots, N
   \]

2. **Stock Balance Constraint**: The stock at the end of period \( n \) should be equal to the stock from the previous period plus the purchase minus the sales in period \( n \).
   \[
   s_n = s_{n-1} + x_n - y_n, \quad \forall n = 1, \ldots, N
   \]
   Since the warehouse is initially empty, we start with:
   \[
   s_0 = 0
   \]

3. **Non-Negativity Constraints**: The amounts bought, sold, and the stock must be non-negative.
   \[
   x_n \geq 0, \quad y_n \geq 0, \quad s_n \geq 0, \quad \forall n = 1, \ldots, N
   \]

4. **Final Stock Constraint**: The warehouse should be empty at the end of the last period.
   \[
   s_N = 0
   \]

Here is the formulation in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:} Maximize the profit
\[
\text{Maximize } \sum_{n=1}^{N} (price_{n} \times y_n - cost_{n} \times x_n) - \sum_{n=1}^{N} (holding\_cost \times s_n)
\]

\textbf{Subject to:}
\begin{align*}
& s_n \leq \text{capacity}, \quad \forall n = 1, \ldots, N \\
& s_n = s_{n-1} + x_n - y_n, \quad \forall n = 1, \ldots, N \\
& x_n \geq 0, \quad y_n \geq 0, \quad s_n \geq 0, \quad \forall n = 1, \ldots, N \\
& s_0 = 0 \\
& s_N = 0
\end{align*}

\end{document}
```

This model will allow us to determine the optimal buy and sell quantities in order to maximize the profit over the given time periods, respecting all constraints.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:} Maximize the profit
\[
\text{Maximize } \sum_{n=1}^{N} (price_{n} \times y_n - cost_{n} \times x_n) - \sum_{n=1}^{N} (holding\_cost \times s_n)
\]

\textbf{Subject to:}
\begin{align*}
& s_n \leq \text{capacity}, \quad \forall n = 1, \ldots, N \\
& s_n = s_{n-1} + x_n - y_n, \quad \forall n = 1, \ldots, N \\
& x_n \geq 0, \quad y_n \geq 0, \quad s_n \geq 0, \quad \forall n = 1, \ldots, N \\
& s_0 = 0 \\
& s_N = 0
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data from JSON
data = json.loads('{"capacity": 10, "holding_cost": 2, "price": [1, 2, 100], "cost": [100, 1, 100]}')

#### Problem definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Variables
N = len(data['price'])
x = pulp.LpVariable.dicts("x", range(N), lowBound=0)
y = pulp.LpVariable.dicts("y", range(N), lowBound=0)
s = pulp.LpVariable.dicts("s", range(N + 1), lowBound=0)

#### Objective function
profit = pulp.lpSum(data['price'][n] * y[n] - data['cost'][n] * x[n] for n in range(N))
holding_cost = pulp.lpSum(data['holding_cost'] * s[n] for n in range(N))
problem += profit - holding_cost

#### Constraints
for n in range(N):
    problem += s[n] <= data['capacity'], f"Capacity_Constraint_{n}"
    if n == 0:
        problem += s[0] == 0, "Initial_Stock_0"
    else:
        problem += s[n] == s[n - 1] + x[n - 1] - y[n - 1], f"Stock_Balance_{n}"

problem += s[N] == 0, "Final_Stock_Condition"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

