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
To formulate the given problem as a linear programming model, we need to establish the objective function and constraints based on the provided information. We aim to determine the optimal quantities of each spare part to manufacture, maximizing the total profit, while adhering to the capacity constraints of each shop.

Let's define the problem as follows:

**Decision Variables:**

- Let \( x_k \) be the quantity of spare part \( k \) to be produced, for \( k = 1, 2, \ldots, K \).

**Objective Function:**

- Maximize the total profit, which can be expressed as:
  \[
  \text{Maximize} \quad Z = \sum_{k=1}^{K} \text{profit}_k \cdot x_k
  \]

**Constraints:**

- For each shop \( s \), the total required working hours must not exceed the shop's capacity:
  \[
  \sum_{k=1}^{K} \text{time}_{k,s} \cdot x_k \leq \text{capacity}_s \quad \text{for each shop } s = 1, 2, \ldots, S
  \]

- Non-negativity constraints:
  \[
  x_k \geq 0 \quad \text{for each part } k = 1, 2, \ldots, K
  \]

Below is the formulation in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Formulation}

\subsection*{Objective}
Maximize the profit:
\[
Z = \sum_{k=1}^{K} \text{profit}_k \cdot x_k
\]

\subsection*{Constraints}
\begin{align*}
\sum_{k=1}^{K} \text{time}_{k,s} \cdot x_k & \leq \text{capacity}_s \quad \text{for each shop } s = 1, 2, \ldots, S \\
x_k & \geq 0 \quad \text{for each part } k = 1, 2, \ldots, K
\end{align*}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( x_k \): quantity of spare part \( k \) to be produced
\end{itemize}

\end{document}
```

This linear programming model will help determine the optimal production quantities for the spare parts to maximize profit while respecting the capacity constraints of the shops.

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

\subsection*{Objective}
Maximize the profit:
\[
Z = \sum_{k=1}^{K} \text{profit}_k \cdot x_k
\]

\subsection*{Constraints}
\begin{align*}
\sum_{k=1}^{K} \text{time}_{k,s} \cdot x_k & \leq \text{capacity}_s \quad \text{for each shop } s = 1, 2, \ldots, S \\
x_k & \geq 0 \quad \text{for each part } k = 1, 2, \ldots, K
\end{align*}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( x_k \): quantity of spare part \( k \) to be produced
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 'profit': [30, 20, 40, 25, 10], 'capacity': [700, 1000]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON
data = {
    'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    'profit': [30, 20, 40, 25, 10],
    'capacity': [700, 1000]
}

#### Number of parts (K) and shops (S)
K = len(data['profit'])
S = len(data['capacity'])

#### Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables: quantity to produce for each spare part
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(K)]

#### Objective Function: Maximize Z
problem += pulp.lpSum(data['profit'][k] * x[k] for k in range(K))

#### Constraints: Capacity constraints for each shop
for s in range(S):
    problem += pulp.lpSum(data['time'][k][s] * x[k] for k in range(K)) <= data['capacity'][s]

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

