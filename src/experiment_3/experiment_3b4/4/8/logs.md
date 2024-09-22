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
To formulate the given problem as a linear programming (LP) model, we need to establish our decision variables, objective function, and constraints based on the given information.

**Decision Variables:**
- Let \( x_k \) represent the quantity of spare part \( k \) to be made during the month.

**Objective Function:**
- We aim to maximize the total profit. The profit from each part \( k \) is given by \( \text{profit}_{k} \), and the total profit is the sum of the profits of all parts. Thus, the objective function can be written as:
  \[
  \text{Maximize} \quad Z = \sum_{k=1}^{K} \text{profit}_{k} \times x_k
  \]

**Constraints:**
- Each shop \( s \) has a limited capacity \(\text{capacity}_{s}\) for worker-hours, and each part \( k \) requires \(\text{time}_{k, s}\) worker-hours in shop \( s \). Therefore, for each shop \( s \), we have the constraint:
  \[
  \sum_{k=1}^{K} \text{time}_{k, s} \times x_k \leq \text{capacity}_{s} \quad \text{for each } s = 1, 2, \ldots, S
  \]

- Additionally, the quantity of each part produced \( x_k \) must be non-negative:
  \[
  x_k \geq 0 \quad \text{for each } k = 1, 2, \ldots, K
  \]

Now, I will write the complete LP model in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\textbf{Decision Variables:}

\begin{itemize}
    \item \( x_k \): Quantity of spare part \( k \) to be made, for \( k = 1, 2, \ldots, K \).
\end{itemize}

\textbf{Objective Function:}

Maximize the total profit:
\[
\text{Maximize} \quad Z = \sum_{k=1}^{K} \text{profit}_{k} \times x_k
\]

\textbf{Constraints:}

\begin{enumerate}
    \item Capacity constraints for each shop \( s \):
    \[
    \sum_{k=1}^{K} \text{time}_{k, s} \times x_k \leq \text{capacity}_{s}, \quad \text{for } s = 1, 2, \ldots, S
    \]
    \item Non-negativity constraints for each part:
    \[
    x_k \geq 0, \quad \text{for } k = 1, 2, \ldots, K
    \]
\end{enumerate}

\end{document}
```

This formulation provides the necessary framework to determine the optimal quantities of each spare part to maximize the total profit, considering the constraints from the capacities of various shops.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\textbf{Decision Variables:}

\begin{itemize}
    \item \( x_k \): Quantity of spare part \( k \) to be made, for \( k = 1, 2, \ldots, K \).
\end{itemize}

\textbf{Objective Function:}

Maximize the total profit:
\[
\text{Maximize} \quad Z = \sum_{k=1}^{K} \text{profit}_{k} \times x_k
\]

\textbf{Constraints:}

\begin{enumerate}
    \item Capacity constraints for each shop \( s \):
    \[
    \sum_{k=1}^{K} \text{time}_{k, s} \times x_k \leq \text{capacity}_{s}, \quad \text{for } s = 1, 2, \ldots, S
    \]
    \item Non-negativity constraints for each part:
    \[
    x_k \geq 0, \quad \text{for } k = 1, 2, \ldots, K
    \]
\end{enumerate}

\end{document}</MATH_MODEL>
<DATA>
{'NumParts': 5, 'NumMachines': 2, 'Time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 'Profit': [30, 20, 40, 25, 10], 'Capacity': [700, 1000]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data extraction from JSON format
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

#### Define Linear Programming Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(num_parts)]

#### Objective Function
problem += pulp.lpSum(profit[k] * x[k] for k in range(num_parts))

#### Constraints - Capacity for each machine
for s in range(num_machines):
    problem += pulp.lpSum(time[k][s] * x[k] for k in range(num_parts)) <= capacity[s]

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

