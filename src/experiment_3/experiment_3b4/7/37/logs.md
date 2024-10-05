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
To formulate the given problem as a linear programming (LP) model, we need to define the decision variables, the objective function, and the constraints using the provided information.

Let's define:
- Decision Variables: \( x_k \) (quantity of spare part \( k \) to be produced)

Objective:
- Maximize the total profit, which is the sum of the profit from each part multiplied by the quantity of that part produced.

Constraints:
- Each shop \( s \) has a limited capacity in terms of worker-hours, which limits the total worker-hours for each part across all shops.

We will use the notation provided in the input format:
- \( \text{time}_{k, s} \) is the worker-hours required for part \( k \) in shop \( s \).
- \( \text{profit}_{k} \) is the profit for making part \( k \).
- \( \text{capacity}_{s} \) is the available working hours for shop \( s \).

Here's the mathematical formulation of the problem:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:} Maximize the profit

\[
Z = \sum_{k=1}^{K} \text{profit}_{k} \cdot x_k
\]

\textbf{Subject to constraints:}

\[
\sum_{k=1}^{K} \text{time}_{k, s} \cdot x_k \leq \text{capacity}_{s} \quad \forall s \in \{1, \ldots, S\}
\]

\[
x_k \geq 0 \quad \forall k \in \{1, \ldots, K\}
\]

where:
- \( x_k \) is the quantity of part \( k \) to be made.
- \( \text{time}_{k, s} \) is the required worker-hours for part \( k \) in shop \( s \).
- \( \text{profit}_{k} \) is the profit from producing one unit of part \( k \).
- \( \text{capacity}_{s} \) is the maximum available worker-hours for shop \( s \).

\end{document}
```

These equations describe an LP model where the objective is to maximize the profit, subject to the capacity constraints of each shop. The decision variables \( x_k \) are non-negative, indicating that no negative quantity of parts can be produced.

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
Z = \sum_{k=1}^{K} \text{profit}_{k} \cdot x_k
\]

\textbf{Subject to constraints:}

\[
\sum_{k=1}^{K} \text{time}_{k, s} \cdot x_k \leq \text{capacity}_{s} \quad \forall s \in \{1, \ldots, S\}
\]

\[
x_k \geq 0 \quad \forall k \in \{1, \ldots, K\}
\]

where:
- \( x_k \) is the quantity of part \( k \) to be made.
- \( \text{time}_{k, s} \) is the required worker-hours for part \( k \) in shop \( s \).
- \( \text{profit}_{k} \) is the profit from producing one unit of part \( k \).
- \( \text{capacity}_{s} \) is the maximum available worker-hours for shop \( s \).

\end{document}</MATH_MODEL>
<DATA>
{'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 'profit': [30, 20, 40, 25, 10], 'capacity': [700, 1000]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON
data = {'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 'profit': [30, 20, 40, 25, 10], 'capacity': [700, 1000]}

time = data['time']
profit = data['profit']
capacity = data['capacity']

#### Number of parts (K) and shops (S)
K = len(profit)
S = len(capacity)

#### Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Define decision variables
x = [pulp.LpVariable(f'x_{k+1}', lowBound=0, cat='Continuous') for k in range(K)]

#### Objective function
problem += pulp.lpSum(profit[k] * x[k] for k in range(K))

#### Constraints
for s in range(S):
    problem += pulp.lpSum(time[k][s] * x[k] for k in range(K)) <= capacity[s]

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

