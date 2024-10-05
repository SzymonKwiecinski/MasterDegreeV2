# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: MILP

PROBLEM INFO:

- A company has \var{I} projects to be done by consultants.
- They have a choice of \var{J} consultants.
- Each consultant may be assigned up to \var{K} projects. 
- Hiring consultant \var{j} incurs a fixed cost of \var{f_j}.
- Assigning project \var{i} to consultant \var{j} incurs an additional cost of \var{c_{i,j}}.

INPUT FORMAT: 

{
    "fixed_costs": [f_j for j in 1, ..., J],
    "additional_costs": [[c_{i,j} for j in 1, ..., J] for i in 1, ..., I],
    "max_projects_per_consultant": K
}

OBJECTIVE: Determine the assignment of consultants to projects that minimizes the total cost.

OUTPUT INFO:

- The projects assigned to each consultant \var{assignment_{j,i}}.
- \var{total_cost} reflects the total cost of hiring consultants and assigning them to projects.

OUTPUT FORMAT:

{
    "assignments": [[assignment_{j,i} for i in 1, ..., I] for j in 1, ..., J],
    "total_cost": total_cost
}
</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
To tackle this problem, we need to formulate a Mixed-Integer Linear Programming (MILP) model. Our goal is to minimize the total cost, which includes both the fixed costs of hiring consultants and the variable costs of assigning projects to consultants.

######### Decision Variables:
- \( x_{j,i} \): Binary variable indicating if project \( i \) is assigned to consultant \( j \) (1 if assigned, 0 otherwise).
- \( y_j \): Binary variable indicating if consultant \( j \) is hired (1 if hired, 0 otherwise).

######### Parameters:
- \( f_j \): Fixed cost for hiring consultant \( j \).
- \( c_{i,j} \): Cost of assigning project \( i \) to consultant \( j \).
- \( K \): Maximum number of projects that can be assigned to any consultant.

######### Objective Function:
Minimize the total cost of hiring consultants and assigning projects:

\[
\text{Minimize} \quad \sum_{j=1}^{J} f_j \cdot y_j + \sum_{i=1}^{I} \sum_{j=1}^{J} c_{i,j} \cdot x_{j,i}
\]

######### Constraints:
1. Each project is assigned to exactly one consultant:
   \[
   \sum_{j=1}^{J} x_{j,i} = 1, \quad \forall i = 1, \ldots, I
   \]

2. A consultant must be hired if they are assigned any project:
   \[
   x_{j,i} \leq y_j, \quad \forall i = 1, \ldots, I, \, \forall j = 1, \ldots, J
   \]

3. A consultant can be assigned up to \( K \) projects:
   \[
   \sum_{i=1}^{I} x_{j,i} \leq K \cdot y_j, \quad \forall j = 1, \ldots, J
   \]

4. Variables are binary:
   \[
   x_{j,i} \in \{0, 1\}, \quad y_j \in \{0, 1\}
   \]

The corresponding LaTeX code for the MILP model is as follows:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Mixed-Integer Linear Programming Model:}

\begin{align*}
    \text{Minimize} \quad & \sum_{j=1}^{J} f_j \cdot y_j + \sum_{i=1}^{I} \sum_{j=1}^{J} c_{i,j} \cdot x_{j,i} \\
    \text{subject to} \quad & \sum_{j=1}^{J} x_{j,i} = 1, \quad \forall i = 1, \ldots, I \\
    & x_{j,i} \leq y_j, \quad \forall i = 1, \ldots, I, \quad \forall j = 1, \ldots, J \\
    & \sum_{i=1}^{I} x_{j,i} \leq K \cdot y_j, \quad \forall j = 1, \ldots, J \\
    & x_{j,i} \in \{0, 1\}, \quad \forall i = 1, \ldots, I, \quad \forall j = 1, \ldots, J \\
    & y_j \in \{0, 1\}, \quad \forall j = 1, \ldots, J
\end{align*}

\end{document}
``` 

This formulation captures the essence of the problem you're facing, ensuring that costs are minimized while respecting the limitations on consultant capabilities and assignments.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Mixed-Integer Linear Programming Model:}

\begin{align*}
    \text{Minimize} \quad & \sum_{j=1}^{J} f_j \cdot y_j + \sum_{i=1}^{I} \sum_{j=1}^{J} c_{i,j} \cdot x_{j,i} \\
    \text{subject to} \quad & \sum_{j=1}^{J} x_{j,i} = 1, \quad \forall i = 1, \ldots, I \\
    & x_{j,i} \leq y_j, \quad \forall i = 1, \ldots, I, \quad \forall j = 1, \ldots, J \\
    & \sum_{i=1}^{I} x_{j,i} \leq K \cdot y_j, \quad \forall j = 1, \ldots, J \\
    & x_{j,i} \in \{0, 1\}, \quad \forall i = 1, \ldots, I, \quad \forall j = 1, \ldots, J \\
    & y_j \in \{0, 1\}, \quad \forall j = 1, \ldots, J
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'fixed_costs': [100, 150, 135], 'additional_costs': [[10, 12, 20], [10, 8, 12], [15, 8, 20], [10, 6, 15], [8, 10, 15]], 'max_projects_per_consultant': 3}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON
data = {
    'fixed_costs': [100, 150, 135],
    'additional_costs': [
        [10, 12, 20],
        [10, 8, 12],
        [15, 8, 20],
        [10, 6, 15],
        [8, 10, 15]
    ],
    'max_projects_per_consultant': 3
}

fixed_costs = data['fixed_costs']
additional_costs = data['additional_costs']
K = data['max_projects_per_consultant']

I = len(additional_costs)  #### Number of projects
J = len(fixed_costs)       #### Number of consultants

#### Define the problem
problem = pulp.LpProblem("Consultant_Selection", pulp.LpMinimize)

#### Decision variables
x = pulp.LpVariable.dicts("x", ((j, i) for j in range(J) for i in range(I)), cat='Binary')
y = pulp.LpVariable.dicts("y", (j for j in range(J)), cat='Binary')

#### Objective function
problem += pulp.lpSum(fixed_costs[j] * y[j] + pulp.lpSum(additional_costs[i][j] * x[j, i] for i in range(I)) for j in range(J))

#### Constraints
for i in range(I):
    problem += pulp.lpSum(x[j, i] for j in range(J)) == 1

for j in range(J):
    problem += pulp.lpSum(x[j, i] for i in range(I)) <= K * y[j]

for i in range(I):
    for j in range(J):
        problem += x[j, i] <= y[j]

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

