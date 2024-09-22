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
To formulate the problem, we need to consider the objective function and the constraints that arise from the problem description.

**Objective Function:**
Maximize the total profit derived from manufacturing each type of spare part. The profit for part \(k\) is given by \(\text{profit}_k\), and the decision variable \(\text{quantity}_k\) represents the number of such parts. Therefore, the objective function is:

\[
\text{Maximize} \quad Z = \sum_{k=1}^{K} \text{profit}_k \times \text{quantity}_k
\]

**Constraints:**
1. For each shop \(s\), the total worker-hours used cannot exceed its capacity. The constraint for each shop \(s\) is:

\[
\sum_{k=1}^{K} \text{time}_{k, s} \times \text{quantity}_k \leq \text{capacity}_s \quad \forall \, s = 1, \ldots, S
\]

2. Non-negativity constraint for the decision variables:

\[
\text{quantity}_k \geq 0 \quad \forall \, k = 1, \ldots, K
\]

Below is the complete mathematical model in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\title{Spare Automobile Parts Production Problem}
\author{}
\date{}
\maketitle

\section*{Objective:}
Maximize the total profit:
\begin{equation}
Z = \sum_{k=1}^{K} \text{profit}_k \times \text{quantity}_k
\end{equation}

\section*{Constraints:}

For each shop \(s = 1, \ldots, S\):
\begin{equation}
\sum_{k=1}^{K} \text{time}_{k, s} \times \text{quantity}_k \leq \text{capacity}_s
\end{equation}

\section*{Non-negativity:}
\begin{equation}
\text{quantity}_k \geq 0 \quad \forall \, k = 1, \ldots, K
\end{equation}

\end{document}
```

The above LaTeX code represents the mathematical formulation of the problem to determine the optimal quantities of each spare part to be manufactured in order to maximize profit, while respecting shop capacity constraints.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\title{Spare Automobile Parts Production Problem}
\author{}
\date{}
\maketitle

\section*{Objective:}
Maximize the total profit:
\begin{equation}
Z = \sum_{k=1}^{K} \text{profit}_k \times \text{quantity}_k
\end{equation}

\section*{Constraints:}

For each shop \(s = 1, \ldots, S\):
\begin{equation}
\sum_{k=1}^{K} \text{time}_{k, s} \times \text{quantity}_k \leq \text{capacity}_s
\end{equation}

\section*{Non-negativity:}
\begin{equation}
\text{quantity}_k \geq 0 \quad \forall \, k = 1, \ldots, K
\end{equation}

\end{document}</MATH_MODEL>
<DATA>
{'NumParts': 5, 'NumMachines': 2, 'Time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 'Profit': [30, 20, 40, 25, 10], 'Capacity': [700, 1000]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON
data = {
    'NumParts': 5,
    'NumMachines': 2,
    'Time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    'Profit': [30, 20, 40, 25, 10],
    'Capacity': [700, 1000]
}

num_parts = data['NumParts']
num_machines = data['NumMachines']
time = data['Time']
profit = data['Profit']
capacity = data['Capacity']

#### Define the LP problem
problem = pulp.LpProblem("Spare_Automobile_Parts_Production", pulp.LpMaximize)

#### Define decision variables
quantity = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(num_parts)]

#### Objective Function
problem += pulp.lpSum([profit[k] * quantity[k] for k in range(num_parts)])

#### Constraints
for s in range(num_machines):
    problem += pulp.lpSum([time[k][s] * quantity[k] for k in range(num_parts)]) <= capacity[s]

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

