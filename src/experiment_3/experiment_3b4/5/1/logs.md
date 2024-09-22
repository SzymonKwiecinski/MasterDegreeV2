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

\section*{Linear Programming Model for Maximizing Revenue}

\subsection*{Problem Description}

A firm produces \( M \) different goods using \( N \) different raw materials. The objective is to determine the amount of each good to produce to maximize the firm's total revenue, subject to the availability of raw materials.

\subsection*{Data}

\begin{itemize}
    \item Let \( \text{available}_i \) be the amount of raw material \( i \) available for \( i = 1, \ldots, N \).
    \item Let \( \text{req}_{i,j} \) be the units of material \( i \) required per unit of good \( j \) produced for \( i = 1, \ldots, N \) and \( j = 1, \ldots, M \).
    \item Let \( \text{price}_j \) be the revenue per unit produced of good \( j \) for \( j = 1, \ldots, M \).
\end{itemize}

\subsection*{Variables}

\begin{itemize}
    \item Let \( \text{amount}_j \) be the amount of good \( j \) produced for \( j = 1, \ldots, M \).
\end{itemize}

\subsection*{Objective Function}

Maximize the total revenue:

\[
\text{Maximize} \quad Z = \sum_{j=1}^{M} \text{price}_j \times \text{amount}_j
\]

\subsection*{Constraints}

\begin{itemize}
    \item Material constraints: Ensure that the production does not exceed available raw materials.
    \[
    \sum_{j=1}^{M} \text{req}_{i,j} \times \text{amount}_j \leq \text{available}_i, \quad \forall i = 1, \ldots, N
    \]
    \item Non-negativity constraints: Production amount for each good cannot be negative.
    \[
    \text{amount}_j \geq 0, \quad \forall j = 1, \ldots, M
    \]
\end{itemize}

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

\section*{Linear Programming Model for Maximizing Revenue}

\subsection*{Problem Description}

A firm produces \( M \) different goods using \( N \) different raw materials. The objective is to determine the amount of each good to produce to maximize the firm's total revenue, subject to the availability of raw materials.

\subsection*{Data}

\begin{itemize}
    \item Let \( \text{available}_i \) be the amount of raw material \( i \) available for \( i = 1, \ldots, N \).
    \item Let \( \text{req}_{i,j} \) be the units of material \( i \) required per unit of good \( j \) produced for \( i = 1, \ldots, N \) and \( j = 1, \ldots, M \).
    \item Let \( \text{price}_j \) be the revenue per unit produced of good \( j \) for \( j = 1, \ldots, M \).
\end{itemize}

\subsection*{Variables}

\begin{itemize}
    \item Let \( \text{amount}_j \) be the amount of good \( j \) produced for \( j = 1, \ldots, M \).
\end{itemize}

\subsection*{Objective Function}

Maximize the total revenue:

\[
\text{Maximize} \quad Z = \sum_{j=1}^{M} \text{price}_j \times \text{amount}_j
\]

\subsection*{Constraints}

\begin{itemize}
    \item Material constraints: Ensure that the production does not exceed available raw materials.
    \[
    \sum_{j=1}^{M} \text{req}_{i,j} \times \text{amount}_j \leq \text{available}_i, \quad \forall i = 1, \ldots, N
    \]
    \item Non-negativity constraints: Production amount for each good cannot be negative.
    \[
    \text{amount}_j \geq 0, \quad \forall j = 1, \ldots, M
    \]
\end{itemize}

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
        [1, 0, 0, 5],
        [0, 3, 1, 1],
        [0, 0, 3, 0]
    ],
    'Prices': [7, 10, 5, 9]
}

#### Number of goods and materials
M = data['M']
N = data['N']

#### Available materials and requirements
available = data['Available']
requirements = data['Requirements']

#### Prices for each good
prices = data['Prices']

#### Define the LP problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

#### Define decision variables
amount = [pulp.LpVariable(f'amount_{j}', lowBound=0, cat='Continuous') for j in range(M)]

#### Objective function
problem += pulp.lpSum(prices[j] * amount[j] for j in range(M))

#### Constraints
for i in range(N):
    problem += pulp.lpSum(requirements[i][j] * amount[j] for j in range(M)) <= available[i]

#### Solve the problem
problem.solve()

#### Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

