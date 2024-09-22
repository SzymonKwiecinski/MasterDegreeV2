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
To approach this problem, we need to formulate a Mixed Integer Programming (MIP) model that will help us determine the optimal subset of items to include in the knapsack.

######### Mathematical Model

Define:
- Let \( K \) be the set of items.
- \( \text{value}_k \) be the value of item \( k \).
- \( \text{size}_k \) be the size of item \( k \).
- \( C \) be the maximum capacity of the knapsack.
- \( x_k \) be a binary decision variable where \( x_k = 1 \) if item \( k \) is included in the knapsack and \( x_k = 0 \) otherwise.

The objective is to maximize the total value of the items included in the knapsack, subject to the constraint that the total size of the selected items does not exceed the knapsack's capacity.

######### Objective Function

Maximize:
\[
\sum_{k=1}^{K} \text{value}_k \cdot x_k
\]

######### Constraints

- Capacity Constraint:
\[
\sum_{k=1}^{K} \text{size}_k \cdot x_k \leq C
\]

- Binary Constraints:
\[
x_k \in \{0, 1\}, \quad \forall k \in K
\]

######### LATEX Code

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Mixed Integer Programming Formulation for the Knapsack Problem}

\textbf{Objective:}
\[
\text{Maximize} \quad \sum_{k=1}^{K} \text{value}_k \cdot x_k
\]

\textbf{Subject to:}
\[
\sum_{k=1}^{K} \text{size}_k \cdot x_k \leq C
\]

\[
x_k \in \{0, 1\}, \quad \forall k \in K
\]

\end{document}
```

In this model:
- The objective function aims to maximize the sum of the values of the items included in the knapsack.
- The constraint ensures that the total size of the items included does not exceed the knapsack's capacity.
- Each decision variable \( x_k \) is binary, indicating whether or not an item is included in the knapsack. 

By solving this MIP model, you will obtain the values of \( x_k \) which determine the optimal items to include, represented in the output format as \(\text{{isincluded}} = [\text{{isincluded}}_k \text{ for } k \text{ in } 1,...,K]\).

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Mixed Integer Programming Formulation for the Knapsack Problem}

\textbf{Objective:}
\[
\text{Maximize} \quad \sum_{k=1}^{K} \text{value}_k \cdot x_k
\]

\textbf{Subject to:}
\[
\sum_{k=1}^{K} \text{size}_k \cdot x_k \leq C
\]

\[
x_k \in \{0, 1\}, \quad \forall k \in K
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

#### Extracting data
C = data['C']
values = data['value']
sizes = data['size']
K = len(values)

#### Problem
problem = pulp.LpProblem("Knapsack_Problem", pulp.LpMaximize)

#### Decision Variables
x = [pulp.LpVariable(f"x_{k}", cat='Binary') for k in range(K)]

#### Objective Function
problem += pulp.lpSum(values[k] * x[k] for k in range(K))

#### Constraints
problem += pulp.lpSum(sizes[k] * x[k] for k in range(K)) <= C

#### Solve
problem.solve()

#### Results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

