# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP

PROBLEM INFO:

- A firm produces \var{M} different goods using \var{N} different raw materials.
- The firm has \var{available_{i}} of raw material \var{i} available.
- Good \var{j} requires \var{req_{i,j}} units of material \var{i} per unit produced.
- Good \var{j} results in a revenue of \var{price_j} per unit produced.


INPUT FORMAT: 

{
    "available": [available_{i} for i in 1, ..., N]
    "requirements": [[req_{i,j} for i in 1, ..., N] for j in 1, ..., M],
    "prices": [price_{j} for j in 1, ..., M]
}

OBJECTIVE: How much of each good should the firm produce in order to maximize its total revenue?

OUTPUT INFO:

- the amount of each good produced \var{amount_{j}}.

OUTPUT FORMAT:

{
    "amount": [amount_{j} for j in 1, ..., M]
}

</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\subsection*{Variables}
Let \( x_j \) represent the amount of good \( j \) produced, where \( j = 1, 2, \ldots, M \).

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{available}_i \): Available units of raw material \( i \), for \( i = 1, 2, \ldots, N \).
    \item \( \text{req}_{i,j} \): Units of raw material \( i \) required to produce one unit of good \( j \).
    \item \( \text{price}_j \): Revenue generated from selling one unit of good \( j \).
\end{itemize}

\subsection*{Objective Function}
We aim to maximize the total revenue:
\[
\text{Maximize } Z = \sum_{j=1}^{M} \text{price}_j \cdot x_j
\]

\subsection*{Constraints}
The production must not exceed the available raw materials:
\[
\sum_{j=1}^{M} \text{req}_{i,j} \cdot x_j \leq \text{available}_i, \quad \text{for } i = 1, 2, \ldots, N
\]

\subsection*{Non-negativity Constraints}
\[
x_j \geq 0, \quad \text{for } j = 1, 2, \ldots, M
\]

\subsection*{Summary of the Model}
The complete linear programming model is thus:

\[
\begin{align*}
\text{Maximize } & Z = \sum_{j=1}^{M} \text{price}_j \cdot x_j \\
\text{subject to } & \sum_{j=1}^{M} \text{req}_{i,j} \cdot x_j \leq \text{available}_i, \quad \forall i \in \{1, 2, \ldots, N\} \\
& x_j \geq 0, \quad \forall j \in \{1, 2, \ldots, M\}
\end{align*}
\]

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

\section*{Linear Programming Model}

\subsection*{Variables}
Let \( x_j \) represent the amount of good \( j \) produced, where \( j = 1, 2, \ldots, M \).

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{available}_i \): Available units of raw material \( i \), for \( i = 1, 2, \ldots, N \).
    \item \( \text{req}_{i,j} \): Units of raw material \( i \) required to produce one unit of good \( j \).
    \item \( \text{price}_j \): Revenue generated from selling one unit of good \( j \).
\end{itemize}

\subsection*{Objective Function}
We aim to maximize the total revenue:
\[
\text{Maximize } Z = \sum_{j=1}^{M} \text{price}_j \cdot x_j
\]

\subsection*{Constraints}
The production must not exceed the available raw materials:
\[
\sum_{j=1}^{M} \text{req}_{i,j} \cdot x_j \leq \text{available}_i, \quad \text{for } i = 1, 2, \ldots, N
\]

\subsection*{Non-negativity Constraints}
\[
x_j \geq 0, \quad \text{for } j = 1, 2, \ldots, M
\]

\subsection*{Summary of the Model}
The complete linear programming model is thus:

\[
\begin{align*}
\text{Maximize } & Z = \sum_{j=1}^{M} \text{price}_j \cdot x_j \\
\text{subject to } & \sum_{j=1}^{M} \text{req}_{i,j} \cdot x_j \leq \text{available}_i, \quad \forall i \in \{1, 2, \ldots, N\} \\
& x_j \geq 0, \quad \forall j \in \{1, 2, \ldots, M\}
\end{align*}
\]

\end{document}</MATH_MODEL>
<DATA>
{'M': 4, 'N': 5, 'Available': [10, 20, 15, 35, 25], 'Requirements': [[3, 2, 0, 0, 0], [0, 5, 2, 1, 0], [1, 0, 0, 5, 3], [0, 3, 1, 1, 5]], 'Prices': [7, 10, 5, 9]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data in JSON format (as a dictionary for easy access)
data = {
    'M': 4, 
    'N': 5, 
    'Available': [10, 20, 15, 35, 25], 
    'Requirements': [
        [3, 2, 0, 0, 0], 
        [0, 5, 2, 1, 0], 
        [1, 0, 0, 5, 3], 
        [0, 3, 1, 1, 5]
    ], 
    'Prices': [7, 10, 5, 9]
}

#### Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
x = pulp.LpVariable.dicts("Production", range(data['M']), lowBound=0, cat='Continuous')

#### Objective function
problem += pulp.lpSum(data['Prices'][j] * x[j] for j in range(data['M'])), "Total_Revenue"

#### Constraints
for i in range(data['N']):
    problem += (pulp.lpSum(data['Requirements'][i][j] * x[j] for j in range(data['M'])) <= data['Available'][i]), f"Material_Constraint_{i+1}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

