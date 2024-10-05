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
To model the knapsack problem as a Mixed Integer Programming (MIP) problem with binary variables, we can define the following mathematical model.

Given:
- A set of items \( k \), each with a value \( \text{value}_k \) and size \( \text{size}_k \).
- A container with maximum capacity \( C \).

We introduce binary variables \( x_k \) for each item, where:
- \( x_k = 1 \) if item \( k \) is included in the knapsack, and 
- \( x_k = 0 \) otherwise.

The objective is to maximize the total value of the items included in the knapsack subject to the constraint that their total size does not exceed the capacity \( C \).

Here is the formulation of the problem in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Knapsack Problem Formulation}

Given:
\begin{itemize}
    \item $K$: Total number of items.
    \item $C$: Maximum capacity of the knapsack.
    \item $\text{value}_k$: Value of item $k$, for $k = 1, \ldots, K$.
    \item $\text{size}_k$: Size of item $k$, for $k = 1, \ldots, K$.
\end{itemize}

Define:
\begin{itemize}
    \item $x_k$: Binary variable, $x_k = 1$ if item $k$ is included in the knapsack, and $x_k = 0$ otherwise.
\end{itemize}

\textbf{Objective:}
\[
\text{Maximize} \quad \sum_{k=1}^{K} \text{value}_k \cdot x_k
\]

\textbf{Subject to:}
\[
\sum_{k=1}^{K} \text{size}_k \cdot x_k \leq C
\]

\[
x_k \in \{0, 1\} \quad \text{for} \quad k = 1, \ldots, K
\]

\end{document}
```

This model seeks to maximize the total value of the items packed in the knapsack while ensuring that their total size does not exceed the container's capacity. The solution to this problem will yield the values of the binary variables \( x_k \), indicating which items are included in the optimal subset.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Knapsack Problem Formulation}

Given:
\begin{itemize}
    \item $K$: Total number of items.
    \item $C$: Maximum capacity of the knapsack.
    \item $\text{value}_k$: Value of item $k$, for $k = 1, \ldots, K$.
    \item $\text{size}_k$: Size of item $k$, for $k = 1, \ldots, K$.
\end{itemize}

Define:
\begin{itemize}
    \item $x_k$: Binary variable, $x_k = 1$ if item $k$ is included in the knapsack, and $x_k = 0$ otherwise.
\end{itemize}

\textbf{Objective:}
\[
\text{Maximize} \quad \sum_{k=1}^{K} \text{value}_k \cdot x_k
\]

\textbf{Subject to:}
\[
\sum_{k=1}^{K} \text{size}_k \cdot x_k \leq C
\]

\[
x_k \in \{0, 1\} \quad \text{for} \quad k = 1, \ldots, K
\]

\end{document}</MATH_MODEL>
<DATA>
{'C': 10, 'value': [10, 20], 'size': [8, 6]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the JSON format
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}
C = data['C']
values = data['value']
sizes = data['size']
K = len(values)

#### Create the problem instance
problem = pulp.LpProblem("KnapsackProblem", pulp.LpMaximize)

#### Create binary decision variables
x = pulp.LpVariable.dicts("x", range(K), 0, 1, pulp.LpBinary)

#### Objective function
problem += pulp.lpSum(values[k] * x[k] for k in range(K)), "TotalValue"

#### Constraint for maximum capacity
problem += pulp.lpSum(sizes[k] * x[k] for k in range(K)) <= C, "CapacityConstraint"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

