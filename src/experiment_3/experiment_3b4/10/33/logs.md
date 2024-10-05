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
To model this knapsack problem as a Mixed Integer Programming (MIP) problem, we will use binary variables to represent whether each item is included in the container. The objective is to maximize the total value of the selected items while ensuring that the sum of their sizes does not exceed the container's capacity.

Below is the mathematical formulation in LaTeX format.

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Knapsack MIP Formulation}

\textbf{Given:}
\begin{itemize}
    \item A set of items indexed by \( k \) where \( k = 1, 2, \ldots, K \)
    \item Value of item \( k \): \( \text{value}_k \)
    \item Size of item \( k \): \( \text{size}_k \)
    \item Maximum capacity of the container: \( C \)
\end{itemize}

\textbf{Decision Variables:}
\[
\text{isincluded}_k =
\begin{cases} 
1, & \text{if item } k \text{ is included in the container} \\
0, & \text{otherwise}
\end{cases}
\]

\textbf{Objective:} Maximize the total value of the packed items
\[
\max \sum_{k=1}^K \text{value}_k \cdot \text{isincluded}_k
\]

\textbf{Subject to:}
\begin{align}
\sum_{k=1}^K \text{size}_k \cdot \text{isincluded}_k & \leq C \quad \text{(Capacity constraint)} \\
\text{isincluded}_k & \in \{0, 1\}, \quad \forall k = 1, 2, \ldots, K
\end{align}

\end{document}
```

This model captures the essence of the knapsack problem using binary decision variables, aiming to maximize the total value while adhering to the capacity constraint. Each item can either be included or not included in the knapsack, represented by the binary variable `isincluded_k`.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Knapsack MIP Formulation}

\textbf{Given:}
\begin{itemize}
    \item A set of items indexed by \( k \) where \( k = 1, 2, \ldots, K \)
    \item Value of item \( k \): \( \text{value}_k \)
    \item Size of item \( k \): \( \text{size}_k \)
    \item Maximum capacity of the container: \( C \)
\end{itemize}

\textbf{Decision Variables:}
\[
\text{isincluded}_k =
\begin{cases} 
1, & \text{if item } k \text{ is included in the container} \\
0, & \text{otherwise}
\end{cases}
\]

\textbf{Objective:} Maximize the total value of the packed items
\[
\max \sum_{k=1}^K \text{value}_k \cdot \text{isincluded}_k
\]

\textbf{Subject to:}
\begin{align}
\sum_{k=1}^K \text{size}_k \cdot \text{isincluded}_k & \leq C \quad \text{(Capacity constraint)} \\
\text{isincluded}_k & \in \{0, 1\}, \quad \forall k = 1, 2, \ldots, K
\end{align}

\end{document}</MATH_MODEL>
<DATA>
{'C': 10, 'value': [10, 20], 'size': [8, 6]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}
values = data['value']
sizes = data['size']
capacity = data['C']
num_items = len(values)

#### Problem
problem = pulp.LpProblem("KnapsackProblem", pulp.LpMaximize)

#### Decision Variables
isincluded = [pulp.LpVariable(f'isincluded_{k}', cat='Binary') for k in range(num_items)]

#### Objective Function
problem += pulp.lpSum(values[k] * isincluded[k] for k in range(num_items)), "Total Value"

#### Constraints
problem += pulp.lpSum(sizes[k] * isincluded[k] for k in range(num_items)) <= capacity, "Capacity Constraint"

#### Solve
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

