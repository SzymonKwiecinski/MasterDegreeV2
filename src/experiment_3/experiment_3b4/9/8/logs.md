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
To formulate the linear programming problem for determining the quantities of each spare part to be made in order to maximize profit, we need to identify the decision variables, objective function, and constraints based on the given problem.

**Decision Variables:**
- Let \( x_k \) represent the quantity of part \( k \) to be produced, where \( k = 1, \ldots, K \).

**Objective Function:**
- We aim to maximize the total profit, which can be expressed as:
  \[
  \text{Maximize } Z = \sum_{k=1}^{K} \text{profit}_k \cdot x_k
  \]

**Constraints:**
- The production of parts is limited by the capacity of each shop. For each shop \( s \), the constraint is:
  \[
  \sum_{k=1}^{K} \text{time}_{k,s} \cdot x_k \leq \text{capacity}_s, \quad s = 1, \ldots, S
  \]
- Non-negativity constraints:
  \[
  x_k \geq 0, \quad k = 1, \ldots, K
  \]

Here is the complete mathematical model in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\textbf{Decision Variables:}
\begin{align*}
x_k &: \text{Quantity of part } k \text{ to be produced, for } k = 1, \ldots, K.
\end{align*}

\textbf{Objective Function:}
\begin{align*}
\text{Maximize } Z &= \sum_{k=1}^{K} \text{profit}_k \cdot x_k
\end{align*}

\textbf{Subject to Constraints:}
\begin{align*}
&\sum_{k=1}^{K} \text{time}_{k,s} \cdot x_k \leq \text{capacity}_s, \quad s = 1, \ldots, S \\
&x_k \geq 0, \quad k = 1, \ldots, K
\end{align*}

\end{document}
```

This formulation captures the essential elements of the problem and provides a structure for solving it using linear programming techniques. The decision variables \( x_k \) represent the quantities to be determined, and the constraints ensure the production complies with shop capacities. The objective function is designed to maximize the firm's profit from producing these parts.

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
\begin{align*}
x_k &: \text{Quantity of part } k \text{ to be produced, for } k = 1, \ldots, K.
\end{align*}

\textbf{Objective Function:}
\begin{align*}
\text{Maximize } Z &= \sum_{k=1}^{K} \text{profit}_k \cdot x_k
\end{align*}

\textbf{Subject to Constraints:}
\begin{align*}
&\sum_{k=1}^{K} \text{time}_{k,s} \cdot x_k \leq \text{capacity}_s, \quad s = 1, \ldots, S \\
&x_k \geq 0, \quad k = 1, \ldots, K
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

#### Create the Linear Programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(data['NumParts'])]

#### Objective function
problem += pulp.lpSum(data['Profit'][k] * x[k] for k in range(data['NumParts']))

#### Constraints
for s in range(data['NumMachines']):
    problem += pulp.lpSum(data['Time'][k][s] * x[k] for k in range(data['NumParts'])) <= data['Capacity'][s], f"Capacity_Constraint_{s}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

