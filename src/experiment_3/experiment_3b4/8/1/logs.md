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

\section*{Linear Programming Formulation}

We are given a problem where a firm produces \( M \) different goods using \( N \) different raw materials. We need to determine the amount of each good to produce in order to maximize total revenue.

\subsection*{Parameters}

\begin{itemize}
    \item \( \text{available}_i \): Amount of raw material \( i \) available, for \( i = 1, \ldots, N \).
    \item \( \text{req}_{i,j} \): Units of material \( i \) required per unit of good \( j \), for \( i = 1, \ldots, N \) and \( j = 1, \ldots, M \).
    \item \( \text{price}_j \): Revenue per unit of good \( j \), for \( j = 1, \ldots, M \).
\end{itemize}

\subsection*{Decision Variables}

\begin{itemize}
    \item \( \text{amount}_j \): Number of units of good \( j \) to produce, for \( j = 1, \ldots, M \).
\end{itemize}

\subsection*{Objective Function}

Maximize the total revenue:
\[
\text{Maximize } Z = \sum_{j=1}^{M} \text{price}_j \times \text{amount}_j
\]

\subsection*{Constraints}

The constraints ensure that the production does not exceed the available resources:
\[
\sum_{j=1}^{M} \text{req}_{i,j} \times \text{amount}_j \leq \text{available}_i, \quad \forall i = 1, \ldots, N
\]

\subsection*{Non-Negativity}

Ensure that the amount produced for each good is non-negative:
\[
\text{amount}_j \geq 0, \quad \forall j = 1, \ldots, M
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

\section*{Linear Programming Formulation}

We are given a problem where a firm produces \( M \) different goods using \( N \) different raw materials. We need to determine the amount of each good to produce in order to maximize total revenue.

\subsection*{Parameters}

\begin{itemize}
    \item \( \text{available}_i \): Amount of raw material \( i \) available, for \( i = 1, \ldots, N \).
    \item \( \text{req}_{i,j} \): Units of material \( i \) required per unit of good \( j \), for \( i = 1, \ldots, N \) and \( j = 1, \ldots, M \).
    \item \( \text{price}_j \): Revenue per unit of good \( j \), for \( j = 1, \ldots, M \).
\end{itemize}

\subsection*{Decision Variables}

\begin{itemize}
    \item \( \text{amount}_j \): Number of units of good \( j \) to produce, for \( j = 1, \ldots, M \).
\end{itemize}

\subsection*{Objective Function}

Maximize the total revenue:
\[
\text{Maximize } Z = \sum_{j=1}^{M} \text{price}_j \times \text{amount}_j
\]

\subsection*{Constraints}

The constraints ensure that the production does not exceed the available resources:
\[
\sum_{j=1}^{M} \text{req}_{i,j} \times \text{amount}_j \leq \text{available}_i, \quad \forall i = 1, \ldots, N
\]

\subsection*{Non-Negativity}

Ensure that the amount produced for each good is non-negative:
\[
\text{amount}_j \geq 0, \quad \forall j = 1, \ldots, M
\]

\end{document}</MATH_MODEL>
<DATA>
{'M': 4, 'N': 5, 'Available': [10, 20, 15, 35, 25], 'Requirements': [[3, 2, 0, 0, 0], [0, 5, 2, 1, 0], [1, 0, 0, 5, 3], [0, 3, 1, 1, 5]], 'Prices': [7, 10, 5, 9]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {
    'M': 4, 
    'N': 5, 
    'Available': [10, 20, 15, 35, 25], 
    'Requirements': [
        [3, 2, 0, 0], 
        [0, 5, 2, 1], 
        [0, 0, 5, 3], 
        [1, 0, 0, 5], 
        [0, 3, 1, 1]
    ], 
    'Prices': [7, 10, 5, 9]
}

#### Problem
problem = pulp.LpProblem("MaximizeRevenue", pulp.LpMaximize)

#### Decision Variables
amount = [pulp.LpVariable(f'amount_{j}', lowBound=0, cat='Continuous') for j in range(data['M'])]

#### Objective Function
problem += pulp.lpSum(data['Prices'][j] * amount[j] for j in range(data['M']))

#### Constraints
for i in range(data['N']):
    problem += pulp.lpSum(data['Requirements'][i][j] * amount[j] for j in range(data['M'])) <= data['Available'][i]

#### Solve
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

