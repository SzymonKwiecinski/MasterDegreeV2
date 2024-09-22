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

\section*{Mathematical Model}

We are given the following parameters:

- \( I \): Number of projects
- \( J \): Number of consultants
- \( K \): Maximum number of projects that a consultant can handle
- \( f_j \): Fixed cost of hiring consultant \textit{j}, for \( j = 1, \ldots, J \)
- \( c_{i,j} \): Cost of assigning project \textit{i} to consultant \textit{j}, for \( i = 1, \ldots, I \) and \( j = 1, \ldots, J \)

\subsection*{Decision Variables}

- \( x_{i,j} \): Binary variable that is 1 if project \textit{i} is assigned to consultant \textit{j}, 0 otherwise.
- \( y_j \): Binary variable that is 1 if consultant \textit{j} is hired, 0 otherwise.

\subsection*{Objective Function}

Minimize the total cost:

\[
\text{Minimize } Z = \sum_{j=1}^{J} f_j y_j + \sum_{i=1}^{I} \sum_{j=1}^{J} c_{i,j} x_{i,j}
\]

\subsection*{Constraints}

1. Each project must be assigned to exactly one consultant:

\[
\sum_{j=1}^{J} x_{i,j} = 1, \quad \forall i = 1, \ldots, I
\]

2. If a project is assigned to a consultant, that consultant must be hired:

\[
x_{i,j} \leq y_j, \quad \forall i = 1, \ldots, I, \quad j = 1, \ldots, J
\]

3. Each consultant can be assigned at most \( K \) projects:

\[
\sum_{i=1}^{I} x_{i,j} \leq K y_j, \quad \forall j = 1, \ldots, J
\]

4. Binary constraints for the decision variables:

\[
x_{i,j} \in \{0, 1\}, \quad \forall i = 1, \ldots, I, \quad j = 1, \ldots, J
\]

\[
y_j \in \{0, 1\}, \quad \forall j = 1, \ldots, J
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

\section*{Mathematical Model}

We are given the following parameters:

- \( I \): Number of projects
- \( J \): Number of consultants
- \( K \): Maximum number of projects that a consultant can handle
- \( f_j \): Fixed cost of hiring consultant \textit{j}, for \( j = 1, \ldots, J \)
- \( c_{i,j} \): Cost of assigning project \textit{i} to consultant \textit{j}, for \( i = 1, \ldots, I \) and \( j = 1, \ldots, J \)

\subsection*{Decision Variables}

- \( x_{i,j} \): Binary variable that is 1 if project \textit{i} is assigned to consultant \textit{j}, 0 otherwise.
- \( y_j \): Binary variable that is 1 if consultant \textit{j} is hired, 0 otherwise.

\subsection*{Objective Function}

Minimize the total cost:

\[
\text{Minimize } Z = \sum_{j=1}^{J} f_j y_j + \sum_{i=1}^{I} \sum_{j=1}^{J} c_{i,j} x_{i,j}
\]

\subsection*{Constraints}

1. Each project must be assigned to exactly one consultant:

\[
\sum_{j=1}^{J} x_{i,j} = 1, \quad \forall i = 1, \ldots, I
\]

2. If a project is assigned to a consultant, that consultant must be hired:

\[
x_{i,j} \leq y_j, \quad \forall i = 1, \ldots, I, \quad j = 1, \ldots, J
\]

3. Each consultant can be assigned at most \( K \) projects:

\[
\sum_{i=1}^{I} x_{i,j} \leq K y_j, \quad \forall j = 1, \ldots, J
\]

4. Binary constraints for the decision variables:

\[
x_{i,j} \in \{0, 1\}, \quad \forall i = 1, \ldots, I, \quad j = 1, \ldots, J
\]

\[
y_j \in \{0, 1\}, \quad \forall j = 1, \ldots, J
\]

\end{document}</MATH_MODEL>
<DATA>
{'fixed_costs': [100, 150, 135], 'additional_costs': [[10, 12, 20], [10, 8, 12], [15, 8, 20], [10, 6, 15], [8, 10, 15]], 'max_projects_per_consultant': 3}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the provided JSON
data = {
    'fixed_costs': [100, 150, 135],
    'additional_costs': [[10, 12, 20], [10, 8, 12], [15, 8, 20], [10, 6, 15], [8, 10, 15]],
    'max_projects_per_consultant': 3
}

#### Parameters
I = len(data['additional_costs'])  #### Number of projects
J = len(data['fixed_costs'])        #### Number of consultants
K = data['max_projects_per_consultant']  #### Maximum projects per consultant

#### Create the linear programming problem
problem = pulp.LpProblem("Consultant_Selection", pulp.LpMinimize)

#### Decision Variables
x = pulp.LpVariable.dicts("project_assignment", (range(I), range(J)), cat='Binary')
y = pulp.LpVariable.dicts("consultant_hired", range(J), cat='Binary')

#### Objective Function
problem += pulp.lpSum(data['fixed_costs'][j] * y[j] for j in range(J)) + \
           pulp.lpSum(data['additional_costs'][i][j] * x[i][j] for i in range(I) for j in range(J)), "Total_Cost"

#### Constraints
#### Each project must be assigned to exactly one consultant
for i in range(I):
    problem += pulp.lpSum(x[i][j] for j in range(J)) == 1, f"Project_Assignment_{i}"

#### If a project is assigned to a consultant, that consultant must be hired
for i in range(I):
    for j in range(J):
        problem += x[i][j] <= y[j], f"Consultant_Hire_{i}_{j}"

#### Each consultant can be assigned at most K projects
for j in range(J):
    problem += pulp.lpSum(x[i][j] for i in range(I)) <= K * y[j], f"Max_Projects_Consultant_{j}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

