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
To model this knapsack problem as a Mixed Integer Programming (MIP) problem, we need to create a mathematical representation focusing on maximizing the total value of items packed within a given capacity constraint. Below is the mathematical formulation using LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\section*{Mathematical Model of the Knapsack Problem}

\textbf{Given:}
\begin{itemize}
    \item $C$: Maximum capacity of the knapsack.
    \item $value_k$: Value of item $k$ for $k = 1, \ldots, K$.
    \item $size_k$: Size of item $k$ for $k = 1, \ldots, K$.
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $isincluded_k$: Binary variable that equals 1 if item $k$ is included in the knapsack, 0 otherwise.
\end{itemize}

\textbf{Objective:}
\[
\text{Maximize} \quad \sum_{k=1}^{K} value_k \cdot isincluded_k
\]

\textbf{Subject to:}
\[
\sum_{k=1}^{K} size_k \cdot isincluded_k \leq C
\]
\[
isincluded_k \in \{0, 1\} \quad \text{for } k = 1, \ldots, K
\]

\end{document}
```

Here is the explanation of the model:

- The objective is to maximize the total value, which is represented by the sum of the values of the included items, \(\sum_{k=1}^{K} value_k \cdot isincluded_k\).
- The constraint ensures that the total size of the included items does not exceed the knapsack's capacity, \(\sum_{k=1}^{K} size_k \cdot isincluded_k \leq C\).
- The decision variables \(isincluded_k\) are binary, indicating whether or not each item is included in the knapsack.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\section*{Mathematical Model of the Knapsack Problem}

\textbf{Given:}
\begin{itemize}
    \item $C$: Maximum capacity of the knapsack.
    \item $value_k$: Value of item $k$ for $k = 1, \ldots, K$.
    \item $size_k$: Size of item $k$ for $k = 1, \ldots, K$.
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $isincluded_k$: Binary variable that equals 1 if item $k$ is included in the knapsack, 0 otherwise.
\end{itemize}

\textbf{Objective:}
\[
\text{Maximize} \quad \sum_{k=1}^{K} value_k \cdot isincluded_k
\]

\textbf{Subject to:}
\[
\sum_{k=1}^{K} size_k \cdot isincluded_k \leq C
\]
\[
isincluded_k \in \{0, 1\} \quad \text{for } k = 1, \ldots, K
\]

\end{document}</MATH_MODEL>
<DATA>
{'C': 10, 'value': [10, 20], 'size': [8, 6]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Given data
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}
C = data['C']
value = data['value']
size = data['size']

#### Create the linear programming problem
problem = pulp.LpProblem("KnapsackProblem", pulp.LpMaximize)

#### Decision variables
K = len(value)
isincluded = pulp.LpVariable.dicts("isincluded", range(K), cat='Binary')

#### Objective function
problem += pulp.lpSum(value[k] * isincluded[k] for k in range(K)), "TotalValue"

#### Constraint
problem += pulp.lpSum(size[k] * isincluded[k] for k in range(K)) <= C, "CapacityConstraint"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

