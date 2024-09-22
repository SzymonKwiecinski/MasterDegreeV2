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

Let \( M \) be the number of different goods produced and \( N \) be the number of different raw materials available. We denote:

\begin{itemize}
    \item \( \text{available}_{i} \): the amount of raw material \( i \) available for \( i = 1, \ldots, N \).
    \item \( \text{req}_{i,j} \): the amount of raw material \( i \) required to produce one unit of good \( j \) for \( j = 1, \ldots, M \).
    \item \( \text{price}_{j} \): the revenue obtained from producing one unit of good \( j \).
    \item \( \text{amount}_{j} \): the number of units of good \( j \) produced.
\end{itemize}

\subsection*{Objective Function}
The objective is to maximize the total revenue, given by:

\[
\text{Maximize } Z = \sum_{j=1}^{M} \text{price}_{j} \cdot \text{amount}_{j}
\]

\subsection*{Constraints}
The production of goods must not exceed the available raw materials. For each raw material \( i \), we have the constraint:

\[
\sum_{j=1}^{M} \text{req}_{i,j} \cdot \text{amount}_{j} \leq \text{available}_{i} \quad \text{for } i = 1, \ldots, N
\]

Additionally, the production amounts must be non-negative:

\[
\text{amount}_{j} \geq 0 \quad \text{for } j = 1, \ldots, M
\]

\subsection*{Formulation}
Putting it all together, the Linear Program can be formulated as:

\[
\begin{align*}
\text{Maximize } & Z = \sum_{j=1}^{M} \text{price}_{j} \cdot \text{amount}_{j} \\
\text{subject to } & \sum_{j=1}^{M} \text{req}_{i,j} \cdot \text{amount}_{j} \leq \text{available}_{i}, \quad i = 1, \ldots, N \\
& \text{amount}_{j} \geq 0, \quad j = 1, \ldots, M
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

Let \( M \) be the number of different goods produced and \( N \) be the number of different raw materials available. We denote:

\begin{itemize}
    \item \( \text{available}_{i} \): the amount of raw material \( i \) available for \( i = 1, \ldots, N \).
    \item \( \text{req}_{i,j} \): the amount of raw material \( i \) required to produce one unit of good \( j \) for \( j = 1, \ldots, M \).
    \item \( \text{price}_{j} \): the revenue obtained from producing one unit of good \( j \).
    \item \( \text{amount}_{j} \): the number of units of good \( j \) produced.
\end{itemize}

\subsection*{Objective Function}
The objective is to maximize the total revenue, given by:

\[
\text{Maximize } Z = \sum_{j=1}^{M} \text{price}_{j} \cdot \text{amount}_{j}
\]

\subsection*{Constraints}
The production of goods must not exceed the available raw materials. For each raw material \( i \), we have the constraint:

\[
\sum_{j=1}^{M} \text{req}_{i,j} \cdot \text{amount}_{j} \leq \text{available}_{i} \quad \text{for } i = 1, \ldots, N
\]

Additionally, the production amounts must be non-negative:

\[
\text{amount}_{j} \geq 0 \quad \text{for } j = 1, \ldots, M
\]

\subsection*{Formulation}
Putting it all together, the Linear Program can be formulated as:

\[
\begin{align*}
\text{Maximize } & Z = \sum_{j=1}^{M} \text{price}_{j} \cdot \text{amount}_{j} \\
\text{subject to } & \sum_{j=1}^{M} \text{req}_{i,j} \cdot \text{amount}_{j} \leq \text{available}_{i}, \quad i = 1, \ldots, N \\
& \text{amount}_{j} \geq 0, \quad j = 1, \ldots, M
\end{align*}
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
    'Requirements': [[3, 2, 0, 0, 0], [0, 5, 2, 1, 0], [1, 0, 0, 5, 3], [0, 3, 1, 1, 5]],
    'Prices': [7, 10, 5, 9]
}

#### Create the LP problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

#### Decision variables
amounts = [pulp.LpVariable(f'amount_{j}', lowBound=0) for j in range(data['M'])]

#### Objective function
problem += pulp.lpSum(data['Prices'][j] * amounts[j] for j in range(data['M'])), "Total_Revenue"

#### Constraints
for i in range(data['N']):
    problem += pulp.lpSum(data['Requirements'][j][i] * amounts[j] for j in range(data['M'])) <= data['Available'][i], f"Raw_Material_Constraint_{i}"

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

