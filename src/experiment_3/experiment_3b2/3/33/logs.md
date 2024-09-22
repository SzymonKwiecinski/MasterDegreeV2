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
To model the given knapsack problem as a Mixed Integer Programming (MIP) problem, we introduce binary decision variables \( x_k \) for each item \( k \). The variable \( x_k \) will take the value 1 if the item is included in the knapsack and 0 otherwise. Our objective is to maximize the total value of the items included in the knapsack, under the constraint that the total size of the included items does not exceed the knapsack's capacity \( C \).

Here is the formulation in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Knapsack Problem Formulation:}

\textbf{Given:}
\begin{itemize}
    \item Maximum Capacity: \( C \)
    \item Values of items: \( \mathbf{value} = [\text{value}_1, \text{value}_2, \ldots, \text{value}_K] \)
    \item Sizes of items: \( \mathbf{size} = [\text{size}_1, \text{size}_2, \ldots, \text{size}_K] \)
\end{itemize}

\textbf{Decision Variables:}
\[
x_k =
\begin{cases} 
1, & \text{if item } k \text{ is included in the knapsack} \\
0, & \text{otherwise}
\end{cases}
\]
for \( k = 1, 2, \ldots, K \).

\textbf{Objective:}
Maximize the total value of the included items:
\[
\max \sum_{k=1}^{K} \text{value}_k \cdot x_k
\]

\textbf{Constraints:}
\begin{align}
\sum_{k=1}^{K} \text{size}_k \cdot x_k & \leq C \quad \text{(Capacity constraint)}
\end{align}

\textbf{Binary Constraints:}
\[
x_k \in \{0, 1\} \quad \text{for } k = 1, 2, \ldots, K
\]

\end{document}
```

This formulation captures the essence of the knapsack problem, where we aim to maximize the value of included items while respecting the capacity constraint of the container. The binary variables \( x_k \) determine whether each item is included in the optimal solution. By solving this MIP, we can determine the optimal set of items to include in the knapsack.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Knapsack Problem Formulation:}

\textbf{Given:}
\begin{itemize}
    \item Maximum Capacity: \( C \)
    \item Values of items: \( \mathbf{value} = [\text{value}_1, \text{value}_2, \ldots, \text{value}_K] \)
    \item Sizes of items: \( \mathbf{size} = [\text{size}_1, \text{size}_2, \ldots, \text{size}_K] \)
\end{itemize}

\textbf{Decision Variables:}
\[
x_k =
\begin{cases} 
1, & \text{if item } k \text{ is included in the knapsack} \\
0, & \text{otherwise}
\end{cases}
\]
for \( k = 1, 2, \ldots, K \).

\textbf{Objective:}
Maximize the total value of the included items:
\[
\max \sum_{k=1}^{K} \text{value}_k \cdot x_k
\]

\textbf{Constraints:}
\begin{align}
\sum_{k=1}^{K} \text{size}_k \cdot x_k & \leq C \quad \text{(Capacity constraint)}
\end{align}

\textbf{Binary Constraints:}
\[
x_k \in \{0, 1\} \quad \text{for } k = 1, 2, \ldots, K
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
C = data['C']
values = data['value']
sizes = data['size']
K = len(values)

#### Create the problem
problem = pulp.LpProblem("Knapsack_Problem", pulp.LpMaximize)

#### Decision Variables
x = pulp.LpVariable.dicts("x", range(K), cat='Binary')

#### Objective Function
problem += pulp.lpSum([values[k] * x[k] for k in range(K)]), "Total_Value"

#### Capacity Constraint
problem += pulp.lpSum([sizes[k] * x[k] for k in range(K)]) <= C, "Capacity_Constraint"

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

