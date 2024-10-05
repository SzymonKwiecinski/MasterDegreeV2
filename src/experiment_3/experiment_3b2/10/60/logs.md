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
To model the given problem as a Mixed Integer Linear Programming (MILP) problem, we need to define the decision variables, objective function, and constraints. Here's a detailed mathematical model in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\usepackage{amssymb}
\begin{document}

\section*{MILP Model for Consultant Assignment Problem}

\subsection*{Sets and Indices}
\begin{align*}
    & I : \text{Set of projects, indexed by } i \\
    & J : \text{Set of consultants, indexed by } j
\end{align*}

\subsection*{Parameters}
\begin{align*}
    & f_j : \text{Fixed cost of hiring consultant } j \\
    & c_{i,j} : \text{Additional cost of assigning project } i \text{ to consultant } j \\
    & K : \text{Maximum number of projects that can be assigned to consultant } j
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
    & x_{i,j} = 
    \begin{cases} 
    1, & \text{if project } i \text{ is assigned to consultant } j \\
    0, & \text{otherwise}
    \end{cases} \\
    & y_j = 
    \begin{cases} 
    1, & \text{if consultant } j \text{ is hired} \\
    0, & \text{otherwise}
    \end{cases} 
\end{align*}

\subsection*{Objective Function}
Minimize the total cost:
\begin{equation}
    \min \sum_{j \in J} \left( f_j y_j + \sum_{i \in I} c_{i,j} x_{i,j} \right)
\end{equation}

\subsection*{Constraints}
\begin{align}
    & \sum_{j \in J} x_{i,j} = 1, \quad \forall i \in I & \text{(Each project is assigned to exactly one consultant)} \\
    & \sum_{i \in I} x_{i,j} \leq K y_j, \quad \forall j \in J & \text{(Consultant limits on projects)} \\
    & x_{i,j} \leq y_j, \quad \forall i \in I, \, j \in J & \text{(Project assigned only if consultant is hired)} \\
    & x_{i,j} \in \{0, 1\}, \quad \forall i \in I, \, j \in J & \text{(Binary decision variable for project assignment)} \\
    & y_j \in \{0, 1\}, \quad \forall j \in J & \text{(Binary decision variable for hiring consultant)}
\end{align}

\end{document}
```

This mathematical model captures the assignment of consultants to projects while minimizing the total cost, taking into account the fixed and additional costs, the maximum number of projects each consultant can handle, and ensuring that each project is assigned to exactly one consultant.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\usepackage{amssymb}
\begin{document}

\section*{MILP Model for Consultant Assignment Problem}

\subsection*{Sets and Indices}
\begin{align*}
    & I : \text{Set of projects, indexed by } i \\
    & J : \text{Set of consultants, indexed by } j
\end{align*}

\subsection*{Parameters}
\begin{align*}
    & f_j : \text{Fixed cost of hiring consultant } j \\
    & c_{i,j} : \text{Additional cost of assigning project } i \text{ to consultant } j \\
    & K : \text{Maximum number of projects that can be assigned to consultant } j
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
    & x_{i,j} = 
    \begin{cases} 
    1, & \text{if project } i \text{ is assigned to consultant } j \\
    0, & \text{otherwise}
    \end{cases} \\
    & y_j = 
    \begin{cases} 
    1, & \text{if consultant } j \text{ is hired} \\
    0, & \text{otherwise}
    \end{cases} 
\end{align*}

\subsection*{Objective Function}
Minimize the total cost:
\begin{equation}
    \min \sum_{j \in J} \left( f_j y_j + \sum_{i \in I} c_{i,j} x_{i,j} \right)
\end{equation}

\subsection*{Constraints}
\begin{align}
    & \sum_{j \in J} x_{i,j} = 1, \quad \forall i \in I & \text{(Each project is assigned to exactly one consultant)} \\
    & \sum_{i \in I} x_{i,j} \leq K y_j, \quad \forall j \in J & \text{(Consultant limits on projects)} \\
    & x_{i,j} \leq y_j, \quad \forall i \in I, \, j \in J & \text{(Project assigned only if consultant is hired)} \\
    & x_{i,j} \in \{0, 1\}, \quad \forall i \in I, \, j \in J & \text{(Binary decision variable for project assignment)} \\
    & y_j \in \{0, 1\}, \quad \forall j \in J & \text{(Binary decision variable for hiring consultant)}
\end{align}

\end{document}</MATH_MODEL>
<DATA>
{'fixed_costs': [100, 150, 135], 'additional_costs': [[10, 12, 20], [10, 8, 12], [15, 8, 20], [10, 6, 15], [8, 10, 15]], 'max_projects_per_consultant': 3}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data extraction from the provided JSON
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

#### Set of projects and consultants
projects = range(len(data['additional_costs']))
consultants = range(len(data['fixed_costs']))

#### Create the model
problem = pulp.LpProblem("Consultant_Assignment_Problem", pulp.LpMinimize)

#### Decision variables
x = pulp.LpVariable.dicts("x", (projects, consultants), cat='Binary')  #### Project assignment
y = pulp.LpVariable.dicts("y", consultants, cat='Binary')               #### Consultant hiring

#### Objective function
problem += pulp.lpSum(data['fixed_costs'][j] * y[j] for j in consultants) + \
           pulp.lpSum(data['additional_costs'][i][j] * x[i][j] for i in projects for j in consultants)

#### Constraints
#### Each project is assigned to exactly one consultant
for i in projects:
    problem += pulp.lpSum(x[i][j] for j in consultants) == 1

#### Consultant limits on projects
for j in consultants:
    problem += pulp.lpSum(x[i][j] for i in projects) <= data['max_projects_per_consultant'] * y[j]

#### Project assignment only if consultant is hired
for i in projects:
    for j in consultants:
        problem += x[i][j] <= y[j]

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

