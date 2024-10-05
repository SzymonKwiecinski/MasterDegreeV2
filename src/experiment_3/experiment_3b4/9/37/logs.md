# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP
PROBLEM INFO:

- A small firm specializes in making some types of spare automobile parts. 
- Each part is has to go through several shops 
- The required worker-hours for part \var{k} in shop \var{s} is \var{time_{k, s}}.
- The profit of part \var{k} is \var{profit_{k}}.
- The capacity of shop \var{s} is \var{capacity_{s}} working hours.

INPUT FORMAT:

{
	"time": [[time_{k, s} for s in 1,...,S] for k in 1,...,K],
	"profit": [profit_{k} for k in 1,...,K],
	"capacity": [capacity_{s} for s in 1,...,S]
}


OBJECTIVE: Formulate the problem of determining the quantities of each spare part to be made during the month so as to maximize profit.

OUTPUT INFO:

- \var{quantity} represents the amount of each spare part to be made

OUTPUT FORMAT:

{
	"quantity": [quantity_{k} for k in 1,...,K]
}
</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
To solve this problem, we'll define a linear programming model to maximize the profit from producing various spare parts. We'll denote the variables, objective function, and constraints according to the provided input.

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Maximizing Profit}

\textbf{Parameters:}

- Let \( K \) be the number of different spare parts.
- Let \( S \) be the number of shops.
- Let \( \text{time}_{k,s} \) be the required worker-hours for part \( k \) in shop \( s \).
- Let \( \text{profit}_{k} \) be the profit from producing one unit of part \( k \).
- Let \( \text{capacity}_{s} \) be the capacity of shop \( s \) in worker-hours.

\textbf{Decision Variables:}

- \( \text{quantity}_{k} \): the number of units of part \( k \) to be produced.

\textbf{Objective Function:}

Maximize the total profit:

\[
\text{Maximize} \quad Z = \sum_{k=1}^{K} \text{profit}_{k} \cdot \text{quantity}_{k}
\]

\textbf{Constraints:}

For each shop \( s \), the total worker-hours used must not exceed the shop's capacity:

\[
\sum_{k=1}^{K} \text{time}_{k,s} \cdot \text{quantity}_{k} \leq \text{capacity}_{s} \quad \text{for} \quad s = 1, \ldots, S
\]

Non-negativity constraints:

\[
\text{quantity}_{k} \geq 0 \quad \text{for} \quad k = 1, \ldots, K
\]

\textbf{Model:}

The linear programming model can be represented as follows:

\[
\begin{align*}
\text{Maximize} \quad & Z = \sum_{k=1}^{K} \text{profit}_{k} \cdot \text{quantity}_{k} \\
\text{subject to} \quad & \sum_{k=1}^{K} \text{time}_{k,s} \cdot \text{quantity}_{k} \leq \text{capacity}_{s}, \quad s = 1, \ldots, S \\
& \text{quantity}_{k} \geq 0, \quad k = 1, \ldots, K
\end{align*}
\]

\end{document}
```

This model sets up the LP problem with the objective of maximizing profits subject to shop capacity constraints and non-negativity of production quantities. Use this formulation to input data and solve the LP in suitable software (e.g., Python with libraries like PuLP or SciPy, or software like CPLEX or Gurobi).

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Maximizing Profit}

\textbf{Parameters:}

- Let \( K \) be the number of different spare parts.
- Let \( S \) be the number of shops.
- Let \( \text{time}_{k,s} \) be the required worker-hours for part \( k \) in shop \( s \).
- Let \( \text{profit}_{k} \) be the profit from producing one unit of part \( k \).
- Let \( \text{capacity}_{s} \) be the capacity of shop \( s \) in worker-hours.

\textbf{Decision Variables:}

- \( \text{quantity}_{k} \): the number of units of part \( k \) to be produced.

\textbf{Objective Function:}

Maximize the total profit:

\[
\text{Maximize} \quad Z = \sum_{k=1}^{K} \text{profit}_{k} \cdot \text{quantity}_{k}
\]

\textbf{Constraints:}

For each shop \( s \), the total worker-hours used must not exceed the shop's capacity:

\[
\sum_{k=1}^{K} \text{time}_{k,s} \cdot \text{quantity}_{k} \leq \text{capacity}_{s} \quad \text{for} \quad s = 1, \ldots, S
\]

Non-negativity constraints:

\[
\text{quantity}_{k} \geq 0 \quad \text{for} \quad k = 1, \ldots, K
\]

\textbf{Model:}

The linear programming model can be represented as follows:

\[
\begin{align*}
\text{Maximize} \quad & Z = \sum_{k=1}^{K} \text{profit}_{k} \cdot \text{quantity}_{k} \\
\text{subject to} \quad & \sum_{k=1}^{K} \text{time}_{k,s} \cdot \text{quantity}_{k} \leq \text{capacity}_{s}, \quad s = 1, \ldots, S \\
& \text{quantity}_{k} \geq 0, \quad k = 1, \ldots, K
\end{align*}
\]

\end{document}</MATH_MODEL>
<DATA>
{'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 'profit': [30, 20, 40, 25, 10], 'capacity': [700, 1000]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data based on the given JSON
data = {
    'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    'profit': [30, 20, 40, 25, 10],
    'capacity': [700, 1000]
}

#### Number of different spare parts (K) and shops (S)
K = len(data['profit'])
S = len(data['capacity'])

#### Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
quantity = [pulp.LpVariable(f"quantity_{k}", lowBound=0, cat='Continuous') for k in range(K)]

#### Objective Function
total_profit = pulp.lpSum(data['profit'][k] * quantity[k] for k in range(K))
problem += total_profit, "Total_Profit"

#### Constraints
for s in range(S):
    problem += (pulp.lpSum(data['time'][k][s] * quantity[k] for k in range(K)) <= data['capacity'][s]), f"Capacity_Constraint_Shop_{s}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

