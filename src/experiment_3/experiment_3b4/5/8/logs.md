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
To formulate the given problem as a Linear Programming (LP) model, we need to define the decision variables, constraints, and the objective function. We will use the following notation:

- Let \( x_k \) for \( k = 1, \ldots, K \) be the decision variables representing the quantity of each spare part to be produced.

The objective is to maximize the total profit, subject to the constraints imposed by the available capacity in each shop.

Here is the mathematical model:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Decision Variables:}
\begin{align*}
x_k & \text{ : quantity of part } k \text{ to be produced, for } k = 1, \ldots, K.
\end{align*}

\textbf{Objective Function:}
\begin{align*}
\text{Maximize} \quad Z & = \sum_{k=1}^{K} \text{profit}_{k} \cdot x_k.
\end{align*}

\textbf{Constraints:}
\begin{align*}
\text{Subject to:} \quad & \sum_{k=1}^{K} \text{time}_{k, s} \cdot x_k \leq \text{capacity}_{s}, \quad \forall s = 1, \ldots, S, \\
& x_k \geq 0, \quad \forall k = 1, \ldots, K.
\end{align*}

\end{document}
```

Explanation of the model:

1. **Decision Variables**: 
   - \( x_k \) is the quantity of spare part \( k \) to be produced.

2. **Objective Function**:
   - The goal is to maximize the total profit, which is the sum of the profit of each part multiplied by its produced quantity.

3. **Constraints**:
   - The first set of constraints ensures that the total worker-hours required in each shop does not exceed the shop's capacity. This is represented by \( \sum_{k=1}^{K} \text{time}_{k, s} \cdot x_k \leq \text{capacity}_{s} \).
   - The second set of constraints ensures that the quantity of each part is non-negative.

This formulation will help determine the optimal number of each spare part to produce in order to maximize profit while respecting the capacity constraints of each shop.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Decision Variables:}
\begin{align*}
x_k & \text{ : quantity of part } k \text{ to be produced, for } k = 1, \ldots, K.
\end{align*}

\textbf{Objective Function:}
\begin{align*}
\text{Maximize} \quad Z & = \sum_{k=1}^{K} \text{profit}_{k} \cdot x_k.
\end{align*}

\textbf{Constraints:}
\begin{align*}
\text{Subject to:} \quad & \sum_{k=1}^{K} \text{time}_{k, s} \cdot x_k \leq \text{capacity}_{s}, \quad \forall s = 1, \ldots, S, \\
& x_k \geq 0, \quad \forall k = 1, \ldots, K.
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'NumParts': 5, 'NumMachines': 2, 'Time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 'Profit': [30, 20, 40, 25, 10], 'Capacity': [700, 1000]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {
    'NumParts': 5,
    'NumMachines': 2,
    'Time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    'Profit': [30, 20, 40, 25, 10],
    'Capacity': [700, 1000]
}

#### Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
x = [pulp.LpVariable(f'x{k}', lowBound=0, cat='Continuous') for k in range(data['NumParts'])]

#### Objective Function
problem += pulp.lpSum(data['Profit'][k] * x[k] for k in range(data['NumParts']))

#### Constraints
for s in range(data['NumMachines']):
    problem += pulp.lpSum(data['Time'][k][s] * x[k] for k in range(data['NumParts'])) <= data['Capacity'][s]

#### Solve
problem.solve()

#### Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

