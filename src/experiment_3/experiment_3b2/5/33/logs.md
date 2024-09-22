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
To formulate the given problem as a Mixed Integer Programming (MIP) model, we can represent it using the following components:

- **Variables:**
  - Let \( x_k \) be a binary variable that indicates whether item \( k \) is included in the container. So, \( x_k = 1 \) if the item is included and \( x_k = 0 \) otherwise.

- **Objective:**
  - Maximize the total value of the packed items.

- **Constraints:**
  - The total size of the packed items must not exceed the capacity \( C \).

We will write the problem formulation using LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Mathematical Model:}

\begin{itemize}
    \item \textbf{Variables:}
    \begin{align*}
        x_k & : \text{Binary variable indicating if item $k$ is included in the container.}
    \end{align*}
    
    \item \textbf{Objective: Maximize the total value of the packed items.}
    \begin{align*}
        \text{Maximize} \quad & \sum_{k=1}^{K} \text{value}_{k} \cdot x_k
    \end{align*}
    
    \item \textbf{Constraints:}
    \begin{align*}
        \text{subject to} \quad & \sum_{k=1}^{K} \text{size}_{k} \cdot x_k \leq C, \\
        & x_k \in \{0, 1\} \quad \text{for all } k = 1, \ldots, K
    \end{align*}
\end{itemize}

\end{document}
```

In this MIP model, the objective function is to maximize the sum of the values of the items that are included in the container. The constraint ensures that the total size of the included items does not exceed the container's capacity. Each item can either be included or not, hence the binary constraint on \( x_k \).

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Mathematical Model:}

\begin{itemize}
    \item \textbf{Variables:}
    \begin{align*}
        x_k & : \text{Binary variable indicating if item $k$ is included in the container.}
    \end{align*}
    
    \item \textbf{Objective: Maximize the total value of the packed items.}
    \begin{align*}
        \text{Maximize} \quad & \sum_{k=1}^{K} \text{value}_{k} \cdot x_k
    \end{align*}
    
    \item \textbf{Constraints:}
    \begin{align*}
        \text{subject to} \quad & \sum_{k=1}^{K} \text{size}_{k} \cdot x_k \leq C, \\
        & x_k \in \{0, 1\} \quad \text{for all } k = 1, \ldots, K
    \end{align*}
\end{itemize}

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

#### Number of items
K = len(values)

#### Create the problem
problem = pulp.LpProblem("Knapsack_Problem", pulp.LpMaximize)

#### Decision variables
x = pulp.LpVariable.dicts("x", range(K), cat='Binary')

#### Objective function
problem += pulp.lpSum(values[k] * x[k] for k in range(K)), "Total_Value"

#### Constraint
problem += pulp.lpSum(sizes[k] * x[k] for k in range(K)) <= C, "Size_Constraint"

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

