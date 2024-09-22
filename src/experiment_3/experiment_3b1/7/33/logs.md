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

\textbf{Parameters:}
\begin{itemize}
    \item $C$: Maximum capacity of the container
    \item $K$: Total number of items
    \item $value_k$: Value of item $k$, for $k = 1, \ldots, K$
    \item $size_k$: Size of item $k$, for $k = 1, \ldots, K$
\end{itemize}

\textbf{Variables:}
\begin{itemize}
    \item $isincluded_k \in \{0, 1\}$: Binary variable indicating whether item $k$ is included in the knapsack (1 if included, 0 otherwise)
\end{itemize}

\textbf{Objective Function:}
\[
\text{Maximize } \sum_{k=1}^{K} value_k \cdot isincluded_k
\]

\textbf{Constraints:}
\[
\sum_{k=1}^{K} size_k \cdot isincluded_k \leq C
\]

\textbf{Variable Definition:}
\[
isincluded_k \in \{0, 1\}, \quad \forall k = 1, \ldots, K
\]

\textbf{Output:}
\begin{itemize}
    \item $isincluded = [isincluded_k \text{ for } k = 1, \ldots, K]$
\end{itemize}

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

\textbf{Parameters:}
\begin{itemize}
    \item $C$: Maximum capacity of the container
    \item $K$: Total number of items
    \item $value_k$: Value of item $k$, for $k = 1, \ldots, K$
    \item $size_k$: Size of item $k$, for $k = 1, \ldots, K$
\end{itemize}

\textbf{Variables:}
\begin{itemize}
    \item $isincluded_k \in \{0, 1\}$: Binary variable indicating whether item $k$ is included in the knapsack (1 if included, 0 otherwise)
\end{itemize}

\textbf{Objective Function:}
\[
\text{Maximize } \sum_{k=1}^{K} value_k \cdot isincluded_k
\]

\textbf{Constraints:}
\[
\sum_{k=1}^{K} size_k \cdot isincluded_k \leq C
\]

\textbf{Variable Definition:}
\[
isincluded_k \in \{0, 1\}, \quad \forall k = 1, \ldots, K
\]

\textbf{Output:}
\begin{itemize}
    \item $isincluded = [isincluded_k \text{ for } k = 1, \ldots, K]$
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'C': 10, 'value': [10, 20], 'size': [8, 6]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}
C = data['C']
values = data['value']
sizes = data['size']
K = len(values)

#### Create the problem
problem = pulp.LpProblem("Knapsack_Problem", pulp.LpMaximize)

#### Create binary variables
isincluded = pulp.LpVariable.dicts("isincluded", range(K), cat='Binary')

#### Objective function
problem += pulp.lpSum([values[k] * isincluded[k] for k in range(K)]), "Total_Value"

#### Constraints
problem += pulp.lpSum([sizes[k] * isincluded[k] for k in range(K)]) <= C, "Capacity_Constraint"

#### Solve the problem
problem.solve()

#### Output results
isincluded_values = [int(isincluded[k].varValue) for k in range(K)]
print(f'Included items: {isincluded_values}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

