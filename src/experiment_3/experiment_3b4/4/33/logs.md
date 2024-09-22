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
To model this problem, we will use Mixed Integer Programming (MIP) with binary variables indicating whether an item is included in the knapsack. The objective is to maximize the total value of the included items subject to the constraint that the total size does not exceed the container capacity \( C \).

Below is the mathematical formulation in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Knapsack Problem Formulation}

Given:
\begin{itemize}
    \item \( C \): Capacity of the container
    \item \( \text{value}_k \): Value of item \( k \)
    \item \( \text{size}_k \): Size of item \( k \)
\end{itemize}

Objective: Maximize the total value of the items included in the knapsack.

\begin{align*}
\max\ & \sum_{k=1}^{K} \text{value}_k \cdot x_k \\
\text{subject to} \quad & \sum_{k=1}^{K} \text{size}_k \cdot x_k \leq C, \\
& x_k \in \{0, 1\} \quad \forall k = 1, \ldots, K.
\end{align*}

Where:
\begin{itemize}
    \item \( x_k \) is a binary variable: 
    \[
    x_k = 
    \begin{cases} 
    1, & \text{if item } k \text{ is included in the knapsack} \\ 
    0, & \text{otherwise.}
    \end{cases}
    \]
\end{itemize}

The solution of this optimization problem will provide the binary vector \(\mathbf{x}\), indicating whether each item is included in the knapsack or not.

\end{document}
```

This LaTeX document explains the Mixed Integer Programming formulation for the knapsack problem. The objective is to maximize the total value of the items included in the knapsack while ensuring the total size does not exceed the given capacity \( C \). The decision variables \( x_k \) are binary, indicating whether an item is included or not.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Knapsack Problem Formulation}

Given:
\begin{itemize}
    \item \( C \): Capacity of the container
    \item \( \text{value}_k \): Value of item \( k \)
    \item \( \text{size}_k \): Size of item \( k \)
\end{itemize}

Objective: Maximize the total value of the items included in the knapsack.

\begin{align*}
\max\ & \sum_{k=1}^{K} \text{value}_k \cdot x_k \\
\text{subject to} \quad & \sum_{k=1}^{K} \text{size}_k \cdot x_k \leq C, \\
& x_k \in \{0, 1\} \quad \forall k = 1, \ldots, K.
\end{align*}

Where:
\begin{itemize}
    \item \( x_k \) is a binary variable: 
    \[
    x_k = 
    \begin{cases} 
    1, & \text{if item } k \text{ is included in the knapsack} \\ 
    0, & \text{otherwise.}
    \end{cases}
    \]
\end{itemize}

The solution of this optimization problem will provide the binary vector \(\mathbf{x}\), indicating whether each item is included in the knapsack or not.

\end{document}</MATH_MODEL>
<DATA>
{'C': 10, 'value': [10, 20], 'size': [8, 6]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Load the data from the provided JSON format
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}
C = data['C']
values = data['value']
sizes = data['size']
K = len(values)

#### Define the problem
problem = pulp.LpProblem("Knapsack_Problem", pulp.LpMaximize)

#### Define decision variables
x = [pulp.LpVariable(f'x{k}', cat='Binary') for k in range(K)]

#### Objective function
problem += pulp.lpSum(values[k] * x[k] for k in range(K))

#### Constraint: Total size must not exceed the capacity
problem += pulp.lpSum(sizes[k] * x[k] for k in range(K)) <= C

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

