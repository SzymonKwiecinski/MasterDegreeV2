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

\section*{Mixed Integer Programming Model for the Knapsack Problem}

\subsection*{Parameters}
\begin{itemize}
    \item $C$: Maximum capacity of the container
    \item $value_k$: Value of item $k$, where $k = 1, 2, \ldots, K$
    \item $size_k$: Size of item $k$, where $k = 1, 2, \ldots, K$
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $x_k$: Binary variable indicating whether item $k$ is included in the knapsack (1 if included, 0 otherwise), where $k = 1, 2, \ldots, K$
\end{itemize}

\subsection*{Objective Function}
\begin{align*}
\text{Maximize} \quad & \sum_{k=1}^{K} value_k \cdot x_k
\end{align*}

\subsection*{Constraints}
\begin{align*}
\text{Subject to} \quad & \sum_{k=1}^{K} size_k \cdot x_k \leq C \\
& x_k \in \{0, 1\}, \quad k = 1, 2, \ldots, K
\end{align*}

\subsection*{Output}
The output will be represented as:
\begin{itemize}
    \item $isincluded_k$: Represents whether each item $k$ is included in the container.
\end{itemize}
The output format will be:
\[
\{ "isincluded": [isincluded_{1}, isincluded_{2}, \ldots, isincluded_{K}] \}
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

\section*{Mixed Integer Programming Model for the Knapsack Problem}

\subsection*{Parameters}
\begin{itemize}
    \item $C$: Maximum capacity of the container
    \item $value_k$: Value of item $k$, where $k = 1, 2, \ldots, K$
    \item $size_k$: Size of item $k$, where $k = 1, 2, \ldots, K$
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $x_k$: Binary variable indicating whether item $k$ is included in the knapsack (1 if included, 0 otherwise), where $k = 1, 2, \ldots, K$
\end{itemize}

\subsection*{Objective Function}
\begin{align*}
\text{Maximize} \quad & \sum_{k=1}^{K} value_k \cdot x_k
\end{align*}

\subsection*{Constraints}
\begin{align*}
\text{Subject to} \quad & \sum_{k=1}^{K} size_k \cdot x_k \leq C \\
& x_k \in \{0, 1\}, \quad k = 1, 2, \ldots, K
\end{align*}

\subsection*{Output}
The output will be represented as:
\begin{itemize}
    \item $isincluded_k$: Represents whether each item $k$ is included in the container.
\end{itemize}
The output format will be:
\[
\{ "isincluded": [isincluded_{1}, isincluded_{2}, \ldots, isincluded_{K}] \}
\]

\end{document}</MATH_MODEL>
<DATA>
{'C': 10, 'value': [10, 20], 'size': [8, 6]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data from the provided JSON
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}
C = data['C']
values = data['value']
sizes = data['size']

#### Number of items
K = len(values)

#### Create the problem
problem = pulp.LpProblem("KnapsackProblem", pulp.LpMaximize)

#### Decision variables
x = pulp.LpVariable.dicts("x", range(K), cat='Binary')

#### Objective function
problem += pulp.lpSum(values[k] * x[k] for k in range(K)), "TotalValue"

#### Constraints
problem += pulp.lpSum(sizes[k] * x[k] for k in range(K)) <= C, "CapacityConstraint"

#### Solve the problem
problem.solve()

#### Prepare the output
isincluded = [int(x[k].value()) for k in range(K)]
output = {
    "isincluded": isincluded
}

#### Print the objective value and the output
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(json.dumps(output))
```

