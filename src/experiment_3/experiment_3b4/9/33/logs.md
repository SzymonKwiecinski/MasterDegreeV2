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
To model this problem as a Mixed Integer Programming (MIP) problem using binary variables, we will define a binary variable \( x_k \) which will be 1 if item \( k \) is included in the knapsack, and 0 otherwise.

The objective is to maximize the total value of the included items, subject to the constraint that the total size of these items does not exceed the knapsack's capacity \( C \).

Here is the mathematical model for the knapsack problem in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Knapsack Problem}

\textbf{Given:}
\begin{itemize}
    \item Capacity of the knapsack: \( C \)
    \item Value of each item: \( \text{value}_k \) for \( k = 1, \ldots, K \)
    \item Size of each item: \( \text{size}_k \) for \( k = 1, \ldots, K \)
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item \( x_k = \begin{cases} 
    1, & \text{if item } k \text{ is included in the knapsack} \\
    0, & \text{otherwise}
    \end{cases} \) for \( k = 1, \ldots, K \)
\end{itemize}

\textbf{Objective:}
\[
\text{Maximize } \sum_{k=1}^{K} \text{value}_k \cdot x_k
\]

\textbf{Subject to:}
\[
\sum_{k=1}^{K} \text{size}_k \cdot x_k \leq C
\]

\[
x_k \in \{0, 1\} \quad \forall k = 1, \ldots, K
\]

\end{document}
```

In this model:
- The objective function \(\sum_{k=1}^{K} \text{value}_k \cdot x_k\) aims to maximize the total value of the selected items.
- The constraint \(\sum_{k=1}^{K} \text{size}_k \cdot x_k \leq C\) ensures that the total size of the selected items does not exceed the knapsack capacity.
- The binary decision variables \(x_k\) indicate whether each item \(k\) is included in the knapsack.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Knapsack Problem}

\textbf{Given:}
\begin{itemize}
    \item Capacity of the knapsack: \( C \)
    \item Value of each item: \( \text{value}_k \) for \( k = 1, \ldots, K \)
    \item Size of each item: \( \text{size}_k \) for \( k = 1, \ldots, K \)
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item \( x_k = \begin{cases} 
    1, & \text{if item } k \text{ is included in the knapsack} \\
    0, & \text{otherwise}
    \end{cases} \) for \( k = 1, \ldots, K \)
\end{itemize}

\textbf{Objective:}
\[
\text{Maximize } \sum_{k=1}^{K} \text{value}_k \cdot x_k
\]

\textbf{Subject to:}
\[
\sum_{k=1}^{K} \text{size}_k \cdot x_k \leq C
\]

\[
x_k \in \{0, 1\} \quad \forall k = 1, \ldots, K
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

#### Decision Variables
x = [pulp.LpVariable(f'x{k}', cat='Binary') for k in range(num_items)]

#### Objective Function
problem += pulp.lpSum(values[k] * x[k] for k in range(num_items)), "Total Value"

#### Constraints
problem += pulp.lpSum(sizes[k] * x[k] for k in range(num_items)) <= capacity, "Capacity Constraint"

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

