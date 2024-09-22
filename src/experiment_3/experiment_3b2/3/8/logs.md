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
To model the given problem as a Linear Programming (LP) problem, we need to maximize the total profit obtained from manufacturing spare automobile parts subject to time and capacity constraints in different shops. The decision variables, constraints, and objective function are defined as follows:

**Decision Variables:**
- Let \( x_k \) be the quantity of spare part \( k \) to be manufactured.

**Objective Function:**
- Maximize the total profit:
  \[
  \text{Maximize } Z = \sum_{k=1}^{K} \text{profit}_{k} \times x_k
  \]

**Constraints:**
- For each shop \( s \), the total working hours needed for manufacturing all parts should not exceed the shop's capacity:
  \[
  \sum_{k=1}^{K} \text{time}_{k,s} \times x_k \leq \text{capacity}_{s} \quad \text{for all } s = 1, \ldots, S
  \]
- Non-negativity constraints:
  \[
  x_k \geq 0 \quad \text{for all } k = 1, \ldots, K
  \]

The following is the corresponding LaTeX code to represent the model:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\subsection*{Decision Variables}
Let \( x_k \) be the quantity of spare part \( k \) to be manufactured, for \( k = 1, \ldots, K \).

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Maximize } Z = \sum_{k=1}^{K} \text{profit}_{k} \times x_k
\]

\subsection*{Constraints}
\begin{enumerate}
    \item Shop capacity constraints:
    \[
    \sum_{k=1}^{K} \text{time}_{k,s} \times x_k \leq \text{capacity}_{s} \quad \text{for all } s = 1, \ldots, S
    \]
    \item Non-negativity constraints:
    \[
    x_k \geq 0 \quad \text{for all } k = 1, \ldots, K
    \]
\end{enumerate}

\end{document}
```

This LaTeX document provides a structured representation of the linear programming model to optimize the production quantities of spare parts for maximum profit while considering the constraints imposed by shop capacities.

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

\subsection*{Decision Variables}
Let \( x_k \) be the quantity of spare part \( k \) to be manufactured, for \( k = 1, \ldots, K \).

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Maximize } Z = \sum_{k=1}^{K} \text{profit}_{k} \times x_k
\]

\subsection*{Constraints}
\begin{enumerate}
    \item Shop capacity constraints:
    \[
    \sum_{k=1}^{K} \text{time}_{k,s} \times x_k \leq \text{capacity}_{s} \quad \text{for all } s = 1, \ldots, S
    \]
    \item Non-negativity constraints:
    \[
    x_k \geq 0 \quad \text{for all } k = 1, \ldots, K
    \]
\end{enumerate}

\end{document}</MATH_MODEL>
<DATA>
{'NumParts': 5, 'NumMachines': 2, 'Time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 'Profit': [30, 20, 40, 25, 10], 'Capacity': [700, 1000]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Provided data in JSON format
data = json.loads('{"NumParts": 5, "NumMachines": 2, "Time": [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], "Profit": [30, 20, 40, 25, 10], "Capacity": [700, 1000]}')

#### Extracting data
NumParts = data['NumParts']
NumMachines = data['NumMachines']
Time = data['Time']
Profit = data['Profit']
Capacity = data['Capacity']

#### Create the linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Create decision variables
x = pulp.LpVariable.dicts("x", range(NumParts), lowBound=0, cat='Continuous')

#### Objective function
problem += pulp.lpSum(Profit[k] * x[k] for k in range(NumParts)), "Total_Profit"

#### Constraints
for s in range(NumMachines):
    problem += pulp.lpSum(Time[k][s] * x[k] for k in range(NumParts)) <= Capacity[s], f"Capacity_Constraint_{s+1}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

