# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: MIP
PROBLEM INFO:

- The knapsack problem has a significant place in the study of integer programming models with binary variables. 
- In the knapsack problem, one needs to pack a set of items in a container.
- Each item \var{k} has value \var{value_{k}} and size \var{size_{k}}.
- And the container has maximum capacity \var{C}. 
- If the total size of the items exceeds the capacity, we can't pack them all. 
- In that case, the problem is to choose a subset of the items of maximum total value that will fit in the container. 

INPUT FORMAT:

{
	"C": C,
	"value": [value_{k} for k in 1,...,K],
	"size": [size_{k} for k in 1,...,K]
}


OBJECTIVE: Maximize the total value of the packed items

OUTPUT INFO:

- \var{isincluded} represents whether each item is included in the container

OUTPUT FORMAT:

{
	"isincluded": [isincluded_{k} for k in 1,...,K]
}
</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\title{Mathematical Model for the Knapsack Problem}
\author{}
\date{}
\maketitle

\section{Problem Definition}
We are given a set of items, each with a respective value and size, and a container with a maximum capacity. The goal is to select a subset of items that maximizes the total value while ensuring that the total size does not exceed the capacity of the container.

\section{Parameters}
\begin{itemize}
    \item \( C \): Maximum capacity of the container.
    \item \( K \): Total number of items available.
    \item \( \text{value}_k \): Value of item \( k \) for \( k = 1, \ldots, K \).
    \item \( \text{size}_k \): Size of item \( k \) for \( k = 1, \ldots, K \).
\end{itemize}

\section{Variables}
\begin{itemize}
    \item \( \text{isincluded}_k \): Binary variable indicating whether item \( k \) is included in the knapsack (1 if included, 0 otherwise) for \( k = 1, \ldots, K \).
\end{itemize}

\section{Objective Function}
The objective is to maximize the total value of the items included in the knapsack:
\[
\text{Maximize } Z = \sum_{k=1}^{K} \text{value}_k \cdot \text{isincluded}_k
\]

\section{Constraints}
The total size of the selected items must not exceed the maximum capacity of the knapsack:
\[
\sum_{k=1}^{K} \text{size}_k \cdot \text{isincluded}_k \leq C
\]

\section{Model Formulation}
The complete model can be formulated as follows:

\begin{align*}
\text{Maximize } & Z = \sum_{k=1}^{K} \text{value}_k \cdot \text{isincluded}_k \\
\text{subject to } & \sum_{k=1}^{K} \text{size}_k \cdot \text{isincluded}_k \leq C \\
& \text{isincluded}_k \in \{0, 1\} \quad \text{for } k = 1, \ldots, K
\end{align*}

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

\title{Mathematical Model for the Knapsack Problem}
\author{}
\date{}
\maketitle

\section{Problem Definition}
We are given a set of items, each with a respective value and size, and a container with a maximum capacity. The goal is to select a subset of items that maximizes the total value while ensuring that the total size does not exceed the capacity of the container.

\section{Parameters}
\begin{itemize}
    \item \( C \): Maximum capacity of the container.
    \item \( K \): Total number of items available.
    \item \( \text{value}_k \): Value of item \( k \) for \( k = 1, \ldots, K \).
    \item \( \text{size}_k \): Size of item \( k \) for \( k = 1, \ldots, K \).
\end{itemize}

\section{Variables}
\begin{itemize}
    \item \( \text{isincluded}_k \): Binary variable indicating whether item \( k \) is included in the knapsack (1 if included, 0 otherwise) for \( k = 1, \ldots, K \).
\end{itemize}

\section{Objective Function}
The objective is to maximize the total value of the items included in the knapsack:
\[
\text{Maximize } Z = \sum_{k=1}^{K} \text{value}_k \cdot \text{isincluded}_k
\]

\section{Constraints}
The total size of the selected items must not exceed the maximum capacity of the knapsack:
\[
\sum_{k=1}^{K} \text{size}_k \cdot \text{isincluded}_k \leq C
\]

\section{Model Formulation}
The complete model can be formulated as follows:

\begin{align*}
\text{Maximize } & Z = \sum_{k=1}^{K} \text{value}_k \cdot \text{isincluded}_k \\
\text{subject to } & \sum_{k=1}^{K} \text{size}_k \cdot \text{isincluded}_k \leq C \\
& \text{isincluded}_k \in \{0, 1\} \quad \text{for } k = 1, \ldots, K
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'C': 10, 'value': [10, 20], 'size': [8, 6]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Parse the data
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}
C = data['C']
values = data['value']
sizes = data['size']
K = len(values)

#### Create a problem instance
problem = pulp.LpProblem("Knapsack_Problem", pulp.LpMaximize)

#### Define decision variables
isincluded = [pulp.LpVariable(f'isincluded_{k}', cat='Binary') for k in range(K)]

#### Objective function
problem += pulp.lpSum(values[k] * isincluded[k] for k in range(K)), "Total Value"

#### Constraint: Total size must not exceed capacity
problem += pulp.lpSum(sizes[k] * isincluded[k] for k in range(K)) <= C, "Capacity"

#### Solve the problem
problem.solve()

#### Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

