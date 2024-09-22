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
To solve this problem, we'll create a Mixed Integer Programming (MIP) model using binary variables. The objective is to maximize the total value of the items included in the knapsack without exceeding its capacity. Here is the mathematical model represented in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Knapsack Problem Formulation}

\textbf{Given:}
\begin{itemize}
    \item A set of items \( k \in \{1, \ldots, K\} \).
    \item Each item \( k \) has a value \( \text{value}_k \) and size \( \text{size}_k \).
    \item Maximum capacity of the knapsack: \( C \).
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item \( x_k \) is a binary variable where \( x_k = 1 \) if item \( k \) is included in the knapsack, and \( x_k = 0 \) otherwise.
\end{itemize}

\textbf{Objective Function:}
\[
\text{Maximize} \quad \sum_{k=1}^{K} \text{value}_k \cdot x_k
\]

\textbf{Subject to:}
\[
\sum_{k=1}^{K} \text{size}_k \cdot x_k \leq C
\]

\textbf{Binary Constraints:}
\[
x_k \in \{0, 1\}, \quad \forall k \in \{1, \ldots, K\}
\]

\end{document}
```

This formulation includes:
- A set of binary decision variables \( x_k \) to indicate whether each item is included in the knapsack.
- A linear objective function to maximize the total value of the selected items.
- A capacity constraint to ensure the total size of the selected items does not exceed the knapsack's capacity.
- The binary constraints denote that each \( x_k \) can only be 0 or 1, representing the inclusion or exclusion of an item.

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

\textbf{Given:}
\begin{itemize}
    \item A set of items \( k \in \{1, \ldots, K\} \).
    \item Each item \( k \) has a value \( \text{value}_k \) and size \( \text{size}_k \).
    \item Maximum capacity of the knapsack: \( C \).
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item \( x_k \) is a binary variable where \( x_k = 1 \) if item \( k \) is included in the knapsack, and \( x_k = 0 \) otherwise.
\end{itemize}

\textbf{Objective Function:}
\[
\text{Maximize} \quad \sum_{k=1}^{K} \text{value}_k \cdot x_k
\]

\textbf{Subject to:}
\[
\sum_{k=1}^{K} \text{size}_k \cdot x_k \leq C
\]

\textbf{Binary Constraints:}
\[
x_k \in \{0, 1\}, \quad \forall k \in \{1, \ldots, K\}
\]

\end{document}</MATH_MODEL>
<DATA>
{'C': 10, 'value': [10, 20], 'size': [8, 6]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON format
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}
C = data['C']
values = data['value']
sizes = data['size']
K = len(values)

#### Create the problem
problem = pulp.LpProblem("Knapsack_Problem", pulp.LpMaximize)

#### Decision variables
x = pulp.LpVariable.dicts('x', range(K), cat='Binary')

#### Objective function
problem += pulp.lpSum(values[k] * x[k] for k in range(K)), "Total_Value"

#### Constraints
problem += pulp.lpSum(sizes[k] * x[k] for k in range(K)) <= C, "Capacity_Constraint"

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

