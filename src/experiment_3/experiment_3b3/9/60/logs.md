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

\title{Mixed Integer Linear Programming Model for Project Assignment}
\author{}
\date{}
\maketitle

\section*{Problem Definition}

Let:
\begin{itemize}
    \item $I$: Number of projects
    \item $J$: Number of consultants
    \item $K$: Maximum number of projects per consultant
    \item $f_j$: Fixed cost of hiring consultant $j$ for $j = 1, \ldots, J$
    \item $c_{i,j}$: Additional cost of assigning project $i$ to consultant $j$ for $i = 1, \ldots, I$ and $j = 1, \ldots, J$
    \item $x_{j}$: Binary variable where $x_{j} = 1$ if consultant $j$ is hired, $0$ otherwise
    \item $y_{i,j}$: Binary variable where $y_{i,j} = 1$ if project $i$ is assigned to consultant $j$, $0$ otherwise
\end{itemize}

\section*{Objective Function}

The objective is to minimize the total cost incurred from hiring consultants and assigning projects, formulated as follows:

\[
\text{Minimize} \quad Z = \sum_{j=1}^{J} f_j x_j + \sum_{i=1}^{I} \sum_{j=1}^{J} c_{i,j} y_{i,j}
\]

\section*{Constraints}

\begin{itemize}
    \item Each project must be assigned to exactly one consultant:
    \[
    \sum_{j=1}^{J} y_{i,j} = 1 \quad \forall i = 1, \ldots, I
    \]
    
    \item A consultant can only work on projects if they are hired:
    \[
    y_{i,j} \leq x_j \quad \forall i = 1, \ldots, I, \quad \forall j = 1, \ldots, J
    \]

    \item Each consultant can be assigned a maximum of $K$ projects:
    \[
    \sum_{i=1}^{I} y_{i,j} \leq K x_j \quad \forall j = 1, \ldots, J
    \]

    \item Binary constraints on decision variables:
    \[
    x_j \in \{0, 1\} \quad \forall j = 1, \ldots, J
    \]
    \[
    y_{i,j} \in \{0, 1\} \quad \forall i = 1, \ldots, I, \quad \forall j = 1, \ldots, J
    \]
\end{itemize}

\section*{Output}

The solution provides:
\begin{itemize}
    \item Assignments of projects to each consultant, represented as $assignment_{j,i}$ where project $i$ is assigned to consultant $j$.
    \item Total cost, denoted as $total\_cost$.
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

\title{Mixed Integer Linear Programming Model for Project Assignment}
\author{}
\date{}
\maketitle

\section*{Problem Definition}

Let:
\begin{itemize}
    \item $I$: Number of projects
    \item $J$: Number of consultants
    \item $K$: Maximum number of projects per consultant
    \item $f_j$: Fixed cost of hiring consultant $j$ for $j = 1, \ldots, J$
    \item $c_{i,j}$: Additional cost of assigning project $i$ to consultant $j$ for $i = 1, \ldots, I$ and $j = 1, \ldots, J$
    \item $x_{j}$: Binary variable where $x_{j} = 1$ if consultant $j$ is hired, $0$ otherwise
    \item $y_{i,j}$: Binary variable where $y_{i,j} = 1$ if project $i$ is assigned to consultant $j$, $0$ otherwise
\end{itemize}

\section*{Objective Function}

The objective is to minimize the total cost incurred from hiring consultants and assigning projects, formulated as follows:

\[
\text{Minimize} \quad Z = \sum_{j=1}^{J} f_j x_j + \sum_{i=1}^{I} \sum_{j=1}^{J} c_{i,j} y_{i,j}
\]

\section*{Constraints}

\begin{itemize}
    \item Each project must be assigned to exactly one consultant:
    \[
    \sum_{j=1}^{J} y_{i,j} = 1 \quad \forall i = 1, \ldots, I
    \]
    
    \item A consultant can only work on projects if they are hired:
    \[
    y_{i,j} \leq x_j \quad \forall i = 1, \ldots, I, \quad \forall j = 1, \ldots, J
    \]

    \item Each consultant can be assigned a maximum of $K$ projects:
    \[
    \sum_{i=1}^{I} y_{i,j} \leq K x_j \quad \forall j = 1, \ldots, J
    \]

    \item Binary constraints on decision variables:
    \[
    x_j \in \{0, 1\} \quad \forall j = 1, \ldots, J
    \]
    \[
    y_{i,j} \in \{0, 1\} \quad \forall i = 1, \ldots, I, \quad \forall j = 1, \ldots, J
    \]
\end{itemize}

\section*{Output}

The solution provides:
\begin{itemize}
    \item Assignments of projects to each consultant, represented as $assignment_{j,i}$ where project $i$ is assigned to consultant $j$.
    \item Total cost, denoted as $total\_cost$.
\end{itemize}

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

#### Number of projects and consultants
I = len(data['additional_costs'])
J = len(data['fixed_costs'])
K = data['max_projects_per_consultant']

#### Initialize the problem
problem = pulp.LpProblem("Project_Assignment_Problem", pulp.LpMinimize)

#### Decision variables
x = [pulp.LpVariable(f"x_{j}", cat="Binary") for j in range(J)]
y = [[pulp.LpVariable(f"y_{i}_{j}", cat="Binary") for j in range(J)] for i in range(I)]

#### Objective function
problem += (pulp.lpSum([data['fixed_costs'][j] * x[j] for j in range(J)]) +
            pulp.lpSum([data['additional_costs'][i][j] * y[i][j] for i in range(I) for j in range(J)]))

#### Constraints
#### Each project must be assigned to exactly one consultant
for i in range(I):
    problem += pulp.lpSum([y[i][j] for j in range(J)]) == 1

#### A consultant can only work on projects if they are hired
for i in range(I):
    for j in range(J):
        problem += y[i][j] <= x[j]

#### Each consultant can be assigned a maximum of K projects
for j in range(J):
    problem += pulp.lpSum([y[i][j] for i in range(I)]) <= K * x[j]

#### Solve the problem
problem.solve()

#### Results
assignments = {(i, j): pulp.value(y[i][j]) for i in range(I) for j in range(J)}
total_cost = pulp.value(problem.objective)

#### Print the objective
print(f'(Objective Value): <OBJ>{total_cost}</OBJ>')
```


