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
To model the given problem as a Mixed Integer Programming (MIP) problem, we can define binary decision variables for each item indicating whether the item is included in the knapsack or not. The objective is to maximize the total value of the items included in the knapsack subject to the constraint that the total size of these items does not exceed the capacity of the knapsack.

Here is the mathematical model in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Knapsack Problem Formulation}

Given:

- Maximum capacity of the knapsack: \( C \)
- \( K \) items, where each item \( k \) has:
  - Value: \( \text{value}_k \)
  - Size: \( \text{size}_k \)

Define binary decision variables:

\[
\text{isincluded}_k = 
\begin{cases} 
1, & \text{if item } k \text{ is included in the knapsack} \\
0, & \text{otherwise}
\end{cases}
\]

Objective:

\[
\max \sum_{k=1}^{K} \text{value}_k \cdot \text{isincluded}_k
\]

Subject to the constraint:

\[
\sum_{k=1}^{K} \text{size}_k \cdot \text{isincluded}_k \leq C
\]

Where:
- \(\text{isincluded}_k \in \{0, 1\}\) for all \(k = 1, \ldots, K\)

\end{document}
```

This model uses a binary variable \(\text{isincluded}_k\) for each item to decide whether or not the item should be included in the knapsack. The objective function maximizes the total value of the selected items, and the constraint ensures that the total size of the selected items does not exceed the capacity \( C \) of the knapsack.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Knapsack Problem Formulation}

Given:

- Maximum capacity of the knapsack: \( C \)
- \( K \) items, where each item \( k \) has:
  - Value: \( \text{value}_k \)
  - Size: \( \text{size}_k \)

Define binary decision variables:

\[
\text{isincluded}_k = 
\begin{cases} 
1, & \text{if item } k \text{ is included in the knapsack} \\
0, & \text{otherwise}
\end{cases}
\]

Objective:

\[
\max \sum_{k=1}^{K} \text{value}_k \cdot \text{isincluded}_k
\]

Subject to the constraint:

\[
\sum_{k=1}^{K} \text{size}_k \cdot \text{isincluded}_k \leq C
\]

Where:
- \(\text{isincluded}_k \in \{0, 1\}\) for all \(k = 1, \ldots, K\)

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
values = data['value']
sizes = data['size']
K = len(values)

#### Create the linear programming problem
problem = pulp.LpProblem("Knapsack_Problem", pulp.LpMaximize)

#### Decision variables
isincluded = pulp.LpVariable.dicts("isincluded", range(K), cat='Binary')

#### Objective function
problem += pulp.lpSum([values[k] * isincluded[k] for k in range(K)]), "Total_Value"

#### Capacity constraint
problem += pulp.lpSum([sizes[k] * isincluded[k] for k in range(K)]) <= C, "Capacity_Constraint"

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

