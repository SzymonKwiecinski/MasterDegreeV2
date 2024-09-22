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
To create a mathematical model for this Linear Programming problem, we need to define the decision variables, objective function, and constraints based on the given problem description.

######### Decision Variables:
- \( \text{buyquantity}_{n} \): The amount of the commodity purchased in period \( n \).
- \( \text{sellquantity}_{n} \): The amount of the commodity sold in period \( n \).
- \( \text{stock}_{n} \): The stock of the commodity at the end of period \( n \).

######### Parameters:
- \( \text{capacity} \): Maximum capacity of the warehouse.
- \( \text{holding\_cost} \): Holding cost per unit per period.
- \( \text{price}_{n} \): Selling price of the commodity in period \( n \).
- \( \text{cost}_{n} \): Purchase cost of the commodity in period \( n \).
  
######### Objective Function:
Maximize the total profit over \( N \) periods, which is the difference between the revenue from selling and the costs of buying and holding the stock.

######### Constraints:
1. Capacity Constraint: The stock in each period should not exceed the warehouse capacity.
2. Balance Constraint: The stock at the end of each period should be equal to the stock at the end of the previous period plus the quantity bought minus the quantity sold.
3. Initial and Final Stock Constraints: The warehouse starts empty and must end empty.

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model}

\subsection*{Decision Variables}
Let \( \text{buyquantity}_{n} \geq 0 \) be the quantity bought in period \( n \), \( \text{sellquantity}_{n} \geq 0 \) be the quantity sold in period \( n \), and \( \text{stock}_{n} \geq 0 \) be the stock level at the end of period \( n \), for \( n = 1, \ldots, N \).

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Maximize } \sum_{n=1}^{N} \left( \text{price}_{n} \cdot \text{sellquantity}_{n} - \text{cost}_{n} \cdot \text{buyquantity}_{n} - \text{holding\_cost} \cdot \text{stock}_{n} \right)
\]

\subsection*{Constraints}
1. \textbf{Capacity Constraint:}
\[ 
\text{stock}_{n} \leq \text{capacity}, \quad \forall n = 1, 2, \ldots, N 
\]

2. \textbf{Balance Constraint:}
\[
\text{stock}_{n} = \text{stock}_{n-1} + \text{buyquantity}_{n} - \text{sellquantity}_{n}, \quad \forall n = 1, 2, \ldots, N
\]
where \( \text{stock}_{0} = 0 \).

3. \textbf{Initial and Final Stock Constraints:}
\[
\text{stock}_{0} = 0, \quad \text{stock}_{N} = 0
\]

\end{document}
```

This model will ensure that the operations maximize profit while respecting the storage limitations and purchase/sale dynamics for each period.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model}

\subsection*{Decision Variables}
Let \( \text{buyquantity}_{n} \geq 0 \) be the quantity bought in period \( n \), \( \text{sellquantity}_{n} \geq 0 \) be the quantity sold in period \( n \), and \( \text{stock}_{n} \geq 0 \) be the stock level at the end of period \( n \), for \( n = 1, \ldots, N \).

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Maximize } \sum_{n=1}^{N} \left( \text{price}_{n} \cdot \text{sellquantity}_{n} - \text{cost}_{n} \cdot \text{buyquantity}_{n} - \text{holding\_cost} \cdot \text{stock}_{n} \right)
\]

\subsection*{Constraints}
1. \textbf{Capacity Constraint:}
\[ 
\text{stock}_{n} \leq \text{capacity}, \quad \forall n = 1, 2, \ldots, N 
\]

2. \textbf{Balance Constraint:}
\[
\text{stock}_{n} = \text{stock}_{n-1} + \text{buyquantity}_{n} - \text{sellquantity}_{n}, \quad \forall n = 1, 2, \ldots, N
\]
where \( \text{stock}_{0} = 0 \).

3. \textbf{Initial and Final Stock Constraints:}
\[
\text{stock}_{0} = 0, \quad \text{stock}_{N} = 0
\]

\end{document}</MATH_MODEL>
<DATA>
{'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data
data = json.loads('{"capacity": 10, "holding_cost": 2, "price": [1, 2, 100], "cost": [100, 1, 100]}')
capacity = data['capacity']
holding_cost = data['holding_cost']
price = data['price']
cost = data['cost']
N = len(price)

#### Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
buyquantity = pulp.LpVariable.dicts("buyquantity", range(1, N+1), lowBound=0)
sellquantity = pulp.LpVariable.dicts("sellquantity", range(1, N+1), lowBound=0)
stock = pulp.LpVariable.dicts("stock", range(0, N+1), lowBound=0)

#### Objective function
problem += pulp.lpSum(price[n-1] * sellquantity[n] - cost[n-1] * buyquantity[n] - holding_cost * stock[n] for n in range(1, N+1))

#### Constraints
#### Capacity constraint
for n in range(1, N+1):
    problem += stock[n] <= capacity

#### Balance constraints
for n in range(1, N+1):
    if n == 1:
        problem += stock[n] == buyquantity[n] - sellquantity[n]
    else:
        problem += stock[n] == stock[n-1] + buyquantity[n] - sellquantity[n]

#### Initial and Final stock constraints
problem += stock[0] == 0  #### Initial stock
problem += stock[N] == 0   #### Final stock

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

