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
To formulate this problem as a linear programming model, we will define the decision variables, objective function, and constraints based on the given information. The problem is to determine the number of each spare part to be manufactured in order to maximize profit, subject to the constraints on working hours in various shops.

Let's define:

- \( x_k \): the quantity of spare part \( k \) to be produced.

The problem is given by:

Objective function:
\[ \text{Maximize } Z = \sum_{k=1}^{K} \text{profit}_{k} \cdot x_k \]

Subject to the constraints:
\[ \sum_{k=1}^{K} \text{time}_{k, s} \cdot x_k \leq \text{capacity}_{s}, \quad \forall s \in \{1, \ldots, S\} \]

Non-negativity constraints:
\[ x_k \geq 0, \quad \forall k \in \{1, \ldots, K\} \]

Here is the complete model in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\textbf{Linear Programming Model}

\begin{align*}
\text{Maximize } & Z = \sum_{k=1}^{K} \text{profit}_{k} \cdot x_k \\
\text{Subject to:} \\
& \sum_{k=1}^{K} \text{time}_{k, s} \cdot x_k \leq \text{capacity}_{s}, \quad \forall s \in \{1, \ldots, S\} \\
& x_k \geq 0, \quad \forall k \in \{1, \ldots, K\}
\end{align*}

\end{document}
```

In this formulation:
- The objective function \( Z \) aims to maximize total profit.
- The first set of constraints ensures that the total worker-hours for all parts in each shop do not exceed the shop's capacity.
- The non-negativity constraints ensure that the quantity of each part produced is non-negative. 

By solving this linear programming problem, you will obtain the optimal quantities of each spare part that should be manufactured in order to maximize profit while respecting the capacity constraints of each shop.

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

\begin{align*}
\text{Maximize } & Z = \sum_{k=1}^{K} \text{profit}_{k} \cdot x_k \\
\text{Subject to:} \\
& \sum_{k=1}^{K} \text{time}_{k, s} \cdot x_k \leq \text{capacity}_{s}, \quad \forall s \in \{1, \ldots, S\} \\
& x_k \geq 0, \quad \forall k \in \{1, \ldots, K\}
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'NumParts': 5, 'NumMachines': 2, 'Time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 'Profit': [30, 20, 40, 25, 10], 'Capacity': [700, 1000]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Parse data
data = {
    'NumParts': 5,
    'NumMachines': 2,
    'Time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    'Profit': [30, 20, 40, 25, 10],
    'Capacity': [700, 1000]
}

#### Problem setup
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
x = [pulp.LpVariable(f"x_{k}", lowBound=0, cat='Continuous') for k in range(data['NumParts'])]

#### Objective function
profit = data['Profit']
problem += pulp.lpSum(profit[k] * x[k] for k in range(data['NumParts']))

#### Constraints
time = data['Time']
capacity = data['Capacity']

#### Capacity constraints for each machine
for s in range(data['NumMachines']):
    problem += pulp.lpSum(time[k][s] * x[k] for k in range(data['NumParts'])) <= capacity[s]

#### Solve the problem
problem.solve()

#### Output the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

