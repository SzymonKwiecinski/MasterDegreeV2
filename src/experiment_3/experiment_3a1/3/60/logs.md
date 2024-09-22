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
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\title{Mathematical Model for Consultant Assignment Problem}
\author{}
\date{}
\maketitle

\section*{Problem Statement}
A company has \( I \) projects to be done by consultants. There are \( J \) available consultants, each of whom may be assigned up to \( K \) projects. Hiring consultant \( j \) incurs a fixed cost of \( f_j \), and assigning project \( i \) to consultant \( j \) incurs an additional cost of \( c_{i,j} \).

\section*{Decision Variables}
Define the binary decision variables:
\[
x_j = 
\begin{cases}
1, & \text{if consultant } j \text{ is hired} \\
0, & \text{otherwise}
\end{cases}
\]
\[
y_{i,j} = 
\begin{cases}
1, & \text{if project } i \text{ is assigned to consultant } j \\
0, & \text{otherwise}
\end{cases}
\]

\section*{Objective Function}
The objective is to minimize the total cost, which is the sum of the fixed costs of hiring consultants and the costs of assigning projects to consultants:
\[
\text{Minimize} \quad Z = \sum_{j=1}^{J} f_j x_j + \sum_{i=1}^{I} \sum_{j=1}^{J} c_{i,j} y_{i,j}
\]

\section*{Constraints}
1. Each project must be assigned to exactly one consultant:
\[
\sum_{j=1}^{J} y_{i,j} = 1, \quad \forall i = 1, \ldots, I
\]

2. A consultant can only be assigned a maximum of \( K \) projects:
\[
\sum_{i=1}^{I} y_{i,j} \leq K x_j, \quad \forall j = 1, \ldots, J
\]

3. Each assignment decision variable must be binary:
\[
y_{i,j} \in \{0, 1\}, \quad \forall i = 1, \ldots, I, \forall j = 1, \ldots, J
\]

4. Each hiring decision variable must be binary:
\[
x_j \in \{0, 1\}, \quad \forall j = 1, \ldots, J
\]

\section*{Output Variables}
The output consists of:
\begin{itemize}
    \item \( \text{assignments} = \left[ \left[y_{i,j}\right]_{i=1}^{I} \right]_{j=1}^{J} \)
    \item \( \text{total\_cost} = Z \)
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

\title{Mathematical Model for Consultant Assignment Problem}
\author{}
\date{}
\maketitle

\section*{Problem Statement}
A company has \( I \) projects to be done by consultants. There are \( J \) available consultants, each of whom may be assigned up to \( K \) projects. Hiring consultant \( j \) incurs a fixed cost of \( f_j \), and assigning project \( i \) to consultant \( j \) incurs an additional cost of \( c_{i,j} \).

\section*{Decision Variables}
Define the binary decision variables:
\[
x_j = 
\begin{cases}
1, & \text{if consultant } j \text{ is hired} \\
0, & \text{otherwise}
\end{cases}
\]
\[
y_{i,j} = 
\begin{cases}
1, & \text{if project } i \text{ is assigned to consultant } j \\
0, & \text{otherwise}
\end{cases}
\]

\section*{Objective Function}
The objective is to minimize the total cost, which is the sum of the fixed costs of hiring consultants and the costs of assigning projects to consultants:
\[
\text{Minimize} \quad Z = \sum_{j=1}^{J} f_j x_j + \sum_{i=1}^{I} \sum_{j=1}^{J} c_{i,j} y_{i,j}
\]

\section*{Constraints}
1. Each project must be assigned to exactly one consultant:
\[
\sum_{j=1}^{J} y_{i,j} = 1, \quad \forall i = 1, \ldots, I
\]

2. A consultant can only be assigned a maximum of \( K \) projects:
\[
\sum_{i=1}^{I} y_{i,j} \leq K x_j, \quad \forall j = 1, \ldots, J
\]

3. Each assignment decision variable must be binary:
\[
y_{i,j} \in \{0, 1\}, \quad \forall i = 1, \ldots, I, \forall j = 1, \ldots, J
\]

4. Each hiring decision variable must be binary:
\[
x_j \in \{0, 1\}, \quad \forall j = 1, \ldots, J
\]

\section*{Output Variables}
The output consists of:
\begin{itemize}
    \item \( \text{assignments} = \left[ \left[y_{i,j}\right]_{i=1}^{I} \right]_{j=1}^{J} \)
    \item \( \text{total\_cost} = Z \)
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'fixed_costs': [100, 150, 135], 'additional_costs': [[10, 12, 20], [10, 8, 12], [15, 8, 20], [10, 6, 15], [8, 10, 15]], 'max_projects_per_consultant': 3}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Input data
data = json.loads("{'fixed_costs': [100, 150, 135], 'additional_costs': [[10, 12, 20], [10, 8, 12], [15, 8, 20], [10, 6, 15], [8, 10, 15]], 'max_projects_per_consultant': 3}")

#### Define the problem
problem = pulp.LpProblem("Consultant_Assignment_Problem", pulp.LpMinimize)

#### Data extraction
I = len(data['additional_costs'])  #### Number of projects
J = len(data['fixed_costs'])        #### Number of consultants
K = data['max_projects_per_consultant']
f = data['fixed_costs']             #### Fixed costs
c = data['additional_costs']        #### Additional costs

#### Decision Variables
x = pulp.LpVariable.dicts("x", range(J), cat='Binary')  #### Hiring decision
y = pulp.LpVariable.dicts("y", (range(I), range(J)), cat='Binary')  #### Assignment decision

#### Objective Function
problem += pulp.lpSum(f[j] * x[j] for j in range(J)) + \
           pulp.lpSum(c[i][j] * y[i][j] for i in range(I) for j in range(J))

#### Constraints
#### 1. Each project must be assigned to exactly one consultant
for i in range(I):
    problem += pulp.lpSum(y[i][j] for j in range(J)) == 1

#### 2. A consultant can only be assigned a maximum of K projects
for j in range(J):
    problem += pulp.lpSum(y[i][j] for i in range(I)) <= K * x[j]

#### Solve the problem
problem.solve()

#### Output results
assignments = [[int(y[i][j].varValue) for j in range(J)] for i in range(I)]
total_cost = pulp.value(problem.objective)

print(f'Assignments: {assignments}')
print(f'Total Cost: {total_cost}')
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')
```

