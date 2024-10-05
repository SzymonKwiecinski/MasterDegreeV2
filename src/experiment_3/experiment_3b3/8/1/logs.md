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

\textbf{Given:}
\begin{itemize}
    \item A firm produces $M$ different goods using $N$ different raw materials.
    \item The amount of raw material $i$ available is $available_i$ for $i = 1, \ldots, N$.
    \item Good $j$ requires $req_{i,j}$ units of material $i$ per unit produced for $i = 1, \ldots, N$ and $j = 1, \ldots, M$.
    \item Good $j$ results in a revenue of $price_j$ per unit produced for $j = 1, \ldots, M$.
\end{itemize}

\textbf{Objective:} Maximize the total revenue.

\textbf{Let:} 
\begin{itemize}
    \item $amount_j$ be the amount of good $j$ produced for $j = 1, \ldots, M$.
\end{itemize}

\textbf{Objective Function:}
\[
\text{Maximize } Z = \sum_{j=1}^{M} price_j \cdot amount_j
\]

\textbf{Subject to the constraints:}
\[
\sum_{j=1}^{M} req_{i,j} \cdot amount_j \leq available_i, \quad \forall i = 1, \ldots, N
\]

\textbf{Non-negativity Constraints:}
\[
amount_j \geq 0, \quad \forall j = 1, \ldots, M
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

\textbf{Given:}
\begin{itemize}
    \item A firm produces $M$ different goods using $N$ different raw materials.
    \item The amount of raw material $i$ available is $available_i$ for $i = 1, \ldots, N$.
    \item Good $j$ requires $req_{i,j}$ units of material $i$ per unit produced for $i = 1, \ldots, N$ and $j = 1, \ldots, M$.
    \item Good $j$ results in a revenue of $price_j$ per unit produced for $j = 1, \ldots, M$.
\end{itemize}

\textbf{Objective:} Maximize the total revenue.

\textbf{Let:} 
\begin{itemize}
    \item $amount_j$ be the amount of good $j$ produced for $j = 1, \ldots, M$.
\end{itemize}

\textbf{Objective Function:}
\[
\text{Maximize } Z = \sum_{j=1}^{M} price_j \cdot amount_j
\]

\textbf{Subject to the constraints:}
\[
\sum_{j=1}^{M} req_{i,j} \cdot amount_j \leq available_i, \quad \forall i = 1, \ldots, N
\]

\textbf{Non-negativity Constraints:}
\[
amount_j \geq 0, \quad \forall j = 1, \ldots, M
\]

\end{document}</MATH_MODEL>
<DATA>
{'M': 4, 'N': 5, 'Available': [10, 20, 15, 35, 25], 'Requirements': [[3, 2, 0, 0, 0], [0, 5, 2, 1, 0], [1, 0, 0, 5, 3], [0, 3, 1, 1, 5]], 'Prices': [7, 10, 5, 9]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON
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

#### Extracting data
M = data['M']
N = data['N']
available = data['Available']
requirements = data['Requirements']
prices = data['Prices']

#### Initialize the problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

#### Decision variables
amount = [pulp.LpVariable(f'amount_{j}', lowBound=0, cat='Continuous') for j in range(M)]

#### Objective function
problem += pulp.lpSum(prices[j] * amount[j] for j in range(M)), "Total Revenue"

#### Constraints
for i in range(N):
    problem += (pulp.lpSum(requirements[j][i] * amount[j] for j in range(M)) <= available[i]), f"Material_{i}_Constraint"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

