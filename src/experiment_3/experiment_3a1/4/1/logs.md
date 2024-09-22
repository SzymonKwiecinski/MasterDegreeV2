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

\subsection*{Parameters}
\begin{itemize}
    \item $M$: Number of different goods
    \item $N$: Number of different raw materials
    \item $available_i$: Amount of raw material $i$ available for $i = 1, \ldots, N$
    \item $req_{i,j}$: Amount of material $i$ required to produce one unit of good $j$ for $j = 1, \ldots, M$ and $i = 1, \ldots, N$
    \item $price_j$: Revenue obtained from producing one unit of good $j$ for $j = 1, \ldots, M$
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $amount_j$: Amount of good $j$ produced for $j = 1, \ldots, M$
\end{itemize}

\subsection*{Objective Function}
Maximize the total revenue:
\[
\text{Maximize } Z = \sum_{j=1}^{M} price_j \cdot amount_j
\]

\subsection*{Constraints}
The production of goods must not exceed the available raw materials:
\[
\sum_{j=1}^{M} req_{i,j} \cdot amount_j \leq available_i \quad \text{for } i = 1, \ldots, N
\]

Additionally, the amount produced cannot be negative:
\[
amount_j \geq 0 \quad \text{for } j = 1, \ldots, M
\]

\subsection*{Output}
The result will provide the optimal amounts of each good to produce:
\[
\text{Output: } \{ "amount": [amount_j \text{ for } j = 1, \ldots, M] \}
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

\subsection*{Parameters}
\begin{itemize}
    \item $M$: Number of different goods
    \item $N$: Number of different raw materials
    \item $available_i$: Amount of raw material $i$ available for $i = 1, \ldots, N$
    \item $req_{i,j}$: Amount of material $i$ required to produce one unit of good $j$ for $j = 1, \ldots, M$ and $i = 1, \ldots, N$
    \item $price_j$: Revenue obtained from producing one unit of good $j$ for $j = 1, \ldots, M$
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $amount_j$: Amount of good $j$ produced for $j = 1, \ldots, M$
\end{itemize}

\subsection*{Objective Function}
Maximize the total revenue:
\[
\text{Maximize } Z = \sum_{j=1}^{M} price_j \cdot amount_j
\]

\subsection*{Constraints}
The production of goods must not exceed the available raw materials:
\[
\sum_{j=1}^{M} req_{i,j} \cdot amount_j \leq available_i \quad \text{for } i = 1, \ldots, N
\]

Additionally, the amount produced cannot be negative:
\[
amount_j \geq 0 \quad \text{for } j = 1, \ldots, M
\]

\subsection*{Output}
The result will provide the optimal amounts of each good to produce:
\[
\text{Output: } \{ "amount": [amount_j \text{ for } j = 1, \ldots, M] \}
\]

\end{document}</MATH_MODEL>
<DATA>
{'M': 4, 'N': 5, 'Available': [10, 20, 15, 35, 25], 'Requirements': [[3, 2, 0, 0, 0], [0, 5, 2, 1, 0], [1, 0, 0, 5, 3], [0, 3, 1, 1, 5]], 'Prices': [7, 10, 5, 9]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data
data = json.loads('{"M": 4, "N": 5, "Available": [10, 20, 15, 35, 25], "Requirements": [[3, 2, 0, 0, 0], [0, 5, 2, 1, 0], [1, 0, 0, 5, 3], [0, 3, 1, 1, 5]], "Prices": [7, 10, 5, 9]}')

M = data['M']
N = data['N']
available = data['Available']
requirements = data['Requirements']
prices = data['Prices']

#### Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
amounts = pulp.LpVariable.dicts("amount", range(M), lowBound=0)

#### Objective Function
problem += pulp.lpSum(prices[j] * amounts[j] for j in range(M))

#### Constraints
for i in range(N):
    problem += (pulp.lpSum(requirements[j][i] * amounts[j] for j in range(M)) <= available[i]), f"Material_Constraint_{i}"

#### Solve the problem
problem.solve()

#### Output the results
result = [amounts[j].varValue for j in range(M)]
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

