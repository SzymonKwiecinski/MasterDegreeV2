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

\section*{Mathematical Model for the Knapsack Problem}

Given a set of items indexed by \( k \) where \( k = 1, \ldots, K \), each item has a value \( \text{value}_k \) and a size \( \text{size}_k \). The container has a maximum capacity \( C \). The goal is to maximize the total value of the packed items under the constraint of the container's capacity.

\subsection*{Variables}
Let \( x_k \) be a binary variable defined as:
\[
x_k = 
\begin{cases}
1 & \text{if item } k \text{ is included in the knapsack} \\
0 & \text{otherwise}
\end{cases}
\]

\subsection*{Objective Function}
The objective is to maximize the total value of the packed items:
\[
\text{Maximize } Z = \sum_{k=1}^{K} \text{value}_k \cdot x_k
\]

\subsection*{Constraints}
The total size of the selected items must not exceed the capacity of the knapsack:
\[
\sum_{k=1}^{K} \text{size}_k \cdot x_k \leq C
\]

\subsection*{Binary Constraints}
The decision variables are binary:
\[
x_k \in \{0, 1\} \quad \forall k = 1, \ldots, K
\]

\subsection*{Output}
The output format will include an array indicating whether each item is included in the container:
\[
\text{output} = \{ \text{isincluded}_k \text{ for } k = 1, \ldots, K \}
\]
where
\[
\text{isincluded}_k = x_k
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

\section*{Mathematical Model for the Knapsack Problem}

Given a set of items indexed by \( k \) where \( k = 1, \ldots, K \), each item has a value \( \text{value}_k \) and a size \( \text{size}_k \). The container has a maximum capacity \( C \). The goal is to maximize the total value of the packed items under the constraint of the container's capacity.

\subsection*{Variables}
Let \( x_k \) be a binary variable defined as:
\[
x_k = 
\begin{cases}
1 & \text{if item } k \text{ is included in the knapsack} \\
0 & \text{otherwise}
\end{cases}
\]

\subsection*{Objective Function}
The objective is to maximize the total value of the packed items:
\[
\text{Maximize } Z = \sum_{k=1}^{K} \text{value}_k \cdot x_k
\]

\subsection*{Constraints}
The total size of the selected items must not exceed the capacity of the knapsack:
\[
\sum_{k=1}^{K} \text{size}_k \cdot x_k \leq C
\]

\subsection*{Binary Constraints}
The decision variables are binary:
\[
x_k \in \{0, 1\} \quad \forall k = 1, \ldots, K
\]

\subsection*{Output}
The output format will include an array indicating whether each item is included in the container:
\[
\text{output} = \{ \text{isincluded}_k \text{ for } k = 1, \ldots, K \}
\]
where
\[
\text{isincluded}_k = x_k
\]

\end{document}</MATH_MODEL>
<DATA>
{'C': 10, 'value': [10, 20], 'size': [8, 6]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}
capacity = data['C']
values = data['value']
sizes = data['size']
num_items = len(values)

#### Problem
problem = pulp.LpProblem("Knapsack_Problem", pulp.LpMaximize)

#### Variables
x = [pulp.LpVariable(f'x_{k}', cat='Binary') for k in range(num_items)]

#### Objective Function
problem += pulp.lpSum(values[k] * x[k] for k in range(num_items)), "Total Value"

#### Constraints
problem += pulp.lpSum(sizes[k] * x[k] for k in range(num_items)) <= capacity, "Total Size"

#### Solve
problem.solve()

#### Output
output = [pulp.value(x[k]) for k in range(num_items)]
print("Included in knapsack:", output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

