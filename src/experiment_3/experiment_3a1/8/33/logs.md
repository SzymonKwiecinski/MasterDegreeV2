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

\subsection*{Sets}
Let \( K \) be the set of items, where \( k \in K \).

\subsection*{Parameters}
\begin{align*}
C & \text{ : maximum capacity of the container} \\
value_k & \text{ : value of item } k \\
size_k & \text{ : size of item } k 
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
isincluded_k & = \begin{cases} 
1 & \text{if item } k \text{ is included in the container} \\
0 & \text{otherwise}
\end{cases} \quad \forall k \in K 
\end{align*}

\subsection*{Objective Function}
Maximize the total value of the items included in the container:
\[
\text{Maximize } Z = \sum_{k \in K} value_k \cdot isincluded_k
\]

\subsection*{Constraints}
Ensure that the total size of the items included does not exceed the capacity of the container:
\[
\sum_{k \in K} size_k \cdot isincluded_k \leq C
\]

\subsection*{Final Model}
The complete mathematical model is defined as follows:
\[
\begin{aligned}
& \text{Maximize } Z = \sum_{k \in K} value_k \cdot isincluded_k \\
& \text{subject to} \\
& \sum_{k \in K} size_k \cdot isincluded_k \leq C \\
& isincluded_k \in \{0, 1\} \quad \forall k \in K 
\end{aligned}
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

\subsection*{Sets}
Let \( K \) be the set of items, where \( k \in K \).

\subsection*{Parameters}
\begin{align*}
C & \text{ : maximum capacity of the container} \\
value_k & \text{ : value of item } k \\
size_k & \text{ : size of item } k 
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
isincluded_k & = \begin{cases} 
1 & \text{if item } k \text{ is included in the container} \\
0 & \text{otherwise}
\end{cases} \quad \forall k \in K 
\end{align*}

\subsection*{Objective Function}
Maximize the total value of the items included in the container:
\[
\text{Maximize } Z = \sum_{k \in K} value_k \cdot isincluded_k
\]

\subsection*{Constraints}
Ensure that the total size of the items included does not exceed the capacity of the container:
\[
\sum_{k \in K} size_k \cdot isincluded_k \leq C
\]

\subsection*{Final Model}
The complete mathematical model is defined as follows:
\[
\begin{aligned}
& \text{Maximize } Z = \sum_{k \in K} value_k \cdot isincluded_k \\
& \text{subject to} \\
& \sum_{k \in K} size_k \cdot isincluded_k \leq C \\
& isincluded_k \in \{0, 1\} \quad \forall k \in K 
\end{aligned}
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
value = data['value']
size = data['size']

#### Number of items
K = range(len(value))

#### Create the linear programming problem
problem = pulp.LpProblem("KnapsackProblem", pulp.LpMaximize)

#### Decision variables
isincluded = pulp.LpVariable.dicts("isincluded", K, 0, 1, pulp.LpBinary)

#### Objective function
problem += pulp.lpSum([value[k] * isincluded[k] for k in K]), "TotalValue"

#### Constraints
problem += pulp.lpSum([size[k] * isincluded[k] for k in K]) <= C, "CapacityConstraint"

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

