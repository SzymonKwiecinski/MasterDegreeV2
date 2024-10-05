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
To formulate this problem as a linear programming model, we need to define the decision variables, the objective function, and the constraints based on the given information.

**Decision Variables:**
- Let \( x_k \) be the quantity of spare part \( k \) to be produced.

**Objective Function:**
- The objective is to maximize the total profit from producing the parts. This can be formulated as:
  \[
  \text{Maximize } Z = \sum_{k=1}^{K} \text{profit}_k \cdot x_k
  \]

**Constraints:**
- Each part requires a certain number of worker-hours in each shop, and the total time used in any shop should not exceed its capacity. Thus, for each shop \( s \), we have:
  \[
  \sum_{k=1}^{K} \text{time}_{k, s} \cdot x_k \leq \text{capacity}_s, \quad \forall s \in \{1, \ldots, S\}
  \]

- Non-negativity constraints:
  \[
  x_k \geq 0, \quad \forall k \in \{1, \ldots, K\}
  \]

Given these components, let us construct the linear programming model in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\title{Linear Programming Model for Maximizing Profit in Spare Parts Production}
\author{}
\date{}
\maketitle

\section*{Problem Formulation}

\subsection*{Decision Variables}
Let \( x_k \) be the quantity of spare part \( k \) to be produced, where \( k = 1, \ldots, K \).

\subsection*{Objective Function}
Maximize the total profit:
\[
Z = \sum_{k=1}^{K} \text{profit}_k \cdot x_k
\]

\subsection*{Constraints}
\begin{align*}
&\text{Shop Capacity Constraints:} \\
&\sum_{k=1}^{K} \text{time}_{k, s} \cdot x_k \leq \text{capacity}_s, \quad \forall s \in \{1, \ldots, S\} \\

&\text{Non-negativity Constraints:} \\
&x_k \geq 0, \quad \forall k \in \{1, \ldots, K\}
\end{align*}

\end{document}
```

This LaTeX code defines the linear programming model for determining the optimal quantities of each spare part to maximize profit, given the constraints on shop capacities. The decision variables represent the quantity of each part to be made, and the constraints ensure that production does not exceed the available working hours in any shop.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\title{Linear Programming Model for Maximizing Profit in Spare Parts Production}
\author{}
\date{}
\maketitle

\section*{Problem Formulation}

\subsection*{Decision Variables}
Let \( x_k \) be the quantity of spare part \( k \) to be produced, where \( k = 1, \ldots, K \).

\subsection*{Objective Function}
Maximize the total profit:
\[
Z = \sum_{k=1}^{K} \text{profit}_k \cdot x_k
\]

\subsection*{Constraints}
\begin{align*}
&\text{Shop Capacity Constraints:} \\
&\sum_{k=1}^{K} \text{time}_{k, s} \cdot x_k \leq \text{capacity}_s, \quad \forall s \in \{1, \ldots, S\} \\

&\text{Non-negativity Constraints:} \\
&x_k \geq 0, \quad \forall k \in \{1, \ldots, K\}
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'NumParts': 5, 'NumMachines': 2, 'Time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 'Profit': [30, 20, 40, 25, 10], 'Capacity': [700, 1000]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the JSON
data = {
    'NumParts': 5,
    'NumMachines': 2,
    'Time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    'Profit': [30, 20, 40, 25, 10],
    'Capacity': [700, 1000]
}

#### Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(data['NumParts'])]

#### Objective Function
problem += pulp.lpSum(data['Profit'][k] * x[k] for k in range(data['NumParts']))

#### Constraints
#### Shop Capacity Constraints
for s in range(data['NumMachines']):
    problem += pulp.lpSum(data['Time'][k][s] * x[k] for k in range(data['NumParts'])) <= data['Capacity'][s]

#### Solve the problem
problem.solve()

#### Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

