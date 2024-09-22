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
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Formulation}

Let \( K \) be the number of spare parts and \( S \) be the number of shops. We denote the following variables:

- \( x_k \): quantity of spare part \( k \) produced, for \( k = 1, 2, \ldots, K \).

Given the inputs:
\begin{itemize}
    \item \( time_{k,s} \): required worker-hours for part \( k \) in shop \( s \)
    \item \( profit_k \): profit of part \( k \)
    \item \( capacity_s \): capacity of shop \( s \) in working hours
\end{itemize}

The objective is to maximize total profit:

\[
\text{Maximize } Z = \sum_{k=1}^{K} profit_k \cdot x_k
\]

Subject to the constraints related to the capacity of each shop:

\[
\sum_{k=1}^{K} time_{k,s} \cdot x_k \leq capacity_s, \quad \text{for } s = 1, 2, \ldots, S
\]

Additionally, we include the non-negativity constraints:

\[
x_k \geq 0, \quad \text{for } k = 1, 2, \ldots, K
\]

Thus, the complete linear programming model can be summarized as follows:

\begin{align*}
\text{Maximize } & Z = \sum_{k=1}^{K} profit_k \cdot x_k \\
\text{subject to } & \sum_{k=1}^{K} time_{k,s} \cdot x_k \leq capacity_s, \quad s = 1, 2, \ldots, S \\
& x_k \geq 0, \quad k = 1, 2, \ldots, K
\end{align*}

\end{document}
```

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Formulation}

Let \( K \) be the number of spare parts and \( S \) be the number of shops. We denote the following variables:

- \( x_k \): quantity of spare part \( k \) produced, for \( k = 1, 2, \ldots, K \).

Given the inputs:
\begin{itemize}
    \item \( time_{k,s} \): required worker-hours for part \( k \) in shop \( s \)
    \item \( profit_k \): profit of part \( k \)
    \item \( capacity_s \): capacity of shop \( s \) in working hours
\end{itemize}

The objective is to maximize total profit:

\[
\text{Maximize } Z = \sum_{k=1}^{K} profit_k \cdot x_k
\]

Subject to the constraints related to the capacity of each shop:

\[
\sum_{k=1}^{K} time_{k,s} \cdot x_k \leq capacity_s, \quad \text{for } s = 1, 2, \ldots, S
\]

Additionally, we include the non-negativity constraints:

\[
x_k \geq 0, \quad \text{for } k = 1, 2, \ldots, K
\]

Thus, the complete linear programming model can be summarized as follows:

\begin{align*}
\text{Maximize } & Z = \sum_{k=1}^{K} profit_k \cdot x_k \\
\text{subject to } & \sum_{k=1}^{K} time_{k,s} \cdot x_k \leq capacity_s, \quad s = 1, 2, \ldots, S \\
& x_k \geq 0, \quad k = 1, 2, \ldots, K
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'NumParts': 5, 'NumMachines': 2, 'Time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 'Profit': [30, 20, 40, 25, 10], 'Capacity': [700, 1000]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Input data
data = {
    'NumParts': 5,
    'NumMachines': 2,
    'Time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    'Profit': [30, 20, 40, 25, 10],
    'Capacity': [700, 1000]
}

#### Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Define variables
x = pulp.LpVariable.dicts("x", range(data['NumParts']), lowBound=0)

#### Objective function
problem += pulp.lpSum(data['Profit'][k] * x[k] for k in range(data['NumParts']))

#### Constraints
for s in range(data['NumMachines']):
    problem += pulp.lpSum(data['Time'][k][s] * x[k] for k in range(data['NumParts'])) <= data['Capacity'][s]

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

