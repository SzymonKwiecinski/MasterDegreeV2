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
To solve this problem, we will formulate it as a Linear Programming (LP) model. Our objective is to determine the optimal quantities of each spare part to manufacture in order to maximize the profit, subject to shop capacity constraints.

Let:
- \( K \) be the total number of different spare parts.
- \( S \) be the total number of shops.
- \( \text{time}_{k,s} \) be the required worker-hours for part \( k \) in shop \( s \).
- \( \text{profit}_{k} \) be the profit yielded by part \( k \).
- \( \text{capacity}_{s} \) be the working hour capacity of shop \( s \).

The decision variable:
- \( \text{quantity}_{k} \) represents the amount of part \( k \) to be made.

The objective function is to maximize the profit:

\[
\text{Maximize} \quad \sum_{k=1}^{K} \text{profit}_{k} \times \text{quantity}_{k}
\]

Subject to constraints for each shop's capacity:

\[
\sum_{k=1}^{K} \text{time}_{k,s} \times \text{quantity}_{k} \leq \text{capacity}_{s}, \quad \text{for each } s = 1, \ldots, S
\]

And the non-negativity constraints for the decision variables:

\[
\text{quantity}_{k} \geq 0, \quad \text{for each } k = 1, \ldots, K
\]

Here's the complete LP formulation in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\textbf{Linear Programming Model}

\textbf{Objective:}
\[
\text{Maximize} \quad Z = \sum_{k=1}^{K} \text{profit}_{k} \times \text{quantity}_{k}
\]

\textbf{Subject to:}
\[
\sum_{k=1}^{K} \text{time}_{k,s} \times \text{quantity}_{k} \leq \text{capacity}_{s}, \quad \forall s = 1, \ldots, S
\]

\[
\text{quantity}_{k} \geq 0, \quad \forall k = 1, \ldots, K
\]

\end{document}
```

This LP model will help determine the optimal production quantities for each spare part while respecting the capacity constraints of each shop to maximize the total profit.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\textbf{Linear Programming Model}

\textbf{Objective:}
\[
\text{Maximize} \quad Z = \sum_{k=1}^{K} \text{profit}_{k} \times \text{quantity}_{k}
\]

\textbf{Subject to:}
\[
\sum_{k=1}^{K} \text{time}_{k,s} \times \text{quantity}_{k} \leq \text{capacity}_{s}, \quad \forall s = 1, \ldots, S
\]

\[
\text{quantity}_{k} \geq 0, \quad \forall k = 1, \ldots, K
\]

\end{document}</MATH_MODEL>
<DATA>
{'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 'profit': [30, 20, 40, 25, 10], 'capacity': [700, 1000]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data in JSON format
data_json = '{"time": [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], "profit": [30, 20, 40, 25, 10], "capacity": [700, 1000]}'
data = json.loads(data_json)

#### Extract data
time = data['time']
profit = data['profit']
capacity = data['capacity']

#### Parameters
K = len(profit)  #### Number of products
S = len(capacity)  #### Number of resources

#### Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
quantity = pulp.LpVariable.dicts("quantity", range(K), lowBound=0)

#### Objective function
problem += pulp.lpSum(profit[k] * quantity[k] for k in range(K)), "Total_Profit"

#### Constraints
for s in range(S):
    problem += pulp.lpSum(time[k][s] * quantity[k] for k in range(K)) <= capacity[s], f"Capacity_Constraint_{s}"

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

