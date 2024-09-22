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
    \item Let \( C \) be the maximum capacity of the container.
    \item Let \( K \) be the total number of items.
    \item Let \( value_k \) be the value of item \( k \) for \( k = 1, \ldots, K \).
    \item Let \( size_k \) be the size of item \( k \) for \( k = 1, \ldots, K \).
\end{itemize}

\subsection*{Variables}
\begin{itemize}
    \item Let \( x_k \) be the binary decision variable which indicates whether item \( k \) is included in the container:
    \[
    x_k = 
    \begin{cases} 
    1 & \text{if item } k \text{ is included} \\
    0 & \text{otherwise}
    \end{cases}
    \]
\end{itemize}

\subsection*{Objective Function}
The objective is to maximize the total value of the packed items:
\[
\text{Maximize } Z = \sum_{k=1}^{K} value_k \cdot x_k
\]

\subsection*{Constraints}
The total size of the packed items must not exceed the container's capacity:
\[
\sum_{k=1}^{K} size_k \cdot x_k \leq C
\]

\subsection*{Binary Constraints}
The decision variables \( x_k \) must be binary:
\[
x_k \in \{0, 1\}, \quad \forall k \in \{1, 2, \ldots, K\}
\]

\subsection*{Output}
The solution will indicate whether each item is included in the container:
\[
\text{Output: } \{ \text{isincluded}_k \,|\, k = 1, \ldots, K \} \text{ where } \text{isincluded}_k = x_k
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
    \item Let \( C \) be the maximum capacity of the container.
    \item Let \( K \) be the total number of items.
    \item Let \( value_k \) be the value of item \( k \) for \( k = 1, \ldots, K \).
    \item Let \( size_k \) be the size of item \( k \) for \( k = 1, \ldots, K \).
\end{itemize}

\subsection*{Variables}
\begin{itemize}
    \item Let \( x_k \) be the binary decision variable which indicates whether item \( k \) is included in the container:
    \[
    x_k = 
    \begin{cases} 
    1 & \text{if item } k \text{ is included} \\
    0 & \text{otherwise}
    \end{cases}
    \]
\end{itemize}

\subsection*{Objective Function}
The objective is to maximize the total value of the packed items:
\[
\text{Maximize } Z = \sum_{k=1}^{K} value_k \cdot x_k
\]

\subsection*{Constraints}
The total size of the packed items must not exceed the container's capacity:
\[
\sum_{k=1}^{K} size_k \cdot x_k \leq C
\]

\subsection*{Binary Constraints}
The decision variables \( x_k \) must be binary:
\[
x_k \in \{0, 1\}, \quad \forall k \in \{1, 2, \ldots, K\}
\]

\subsection*{Output}
The solution will indicate whether each item is included in the container:
\[
\text{Output: } \{ \text{isincluded}_k \,|\, k = 1, \ldots, K \} \text{ where } \text{isincluded}_k = x_k
\]

\end{document}</MATH_MODEL>
<DATA>
{'C': 10, 'value': [10, 20], 'size': [8, 6]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data input
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}
C = data['C']
values = data['value']
sizes = data['size']
K = len(values)

#### Problem definition
problem = pulp.LpProblem("Knapsack_Problem", pulp.LpMaximize)

#### Decision variables
x = pulp.LpVariable.dicts("x", range(K), cat='Binary')

#### Objective Function
problem += pulp.lpSum(values[k] * x[k] for k in range(K)), "Total_Value"

#### Capacity Constraint
problem += pulp.lpSum(sizes[k] * x[k] for k in range(K)) <= C, "Capacity_Constraint"

#### Solve the problem
problem.solve()

#### Output results
included_items = [k for k in range(K) if pulp.value(x[k]) == 1]
print(f'Included items: {included_items}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

