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
To solve this problem, we need to formulate a Mixed Integer Linear Programming (MILP) model that captures the constraints and objective described. We'll introduce binary variables to indicate whether a consultant is hired and whether a consultant is assigned to a particular project. Here is the mathematical formulation of the problem in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{amsfonts}
\begin{document}

\section*{MILP Formulation for Consultant Project Assignment}

\subsection*{Sets and Indices}
\begin{align*}
& I: \text{Set of projects, indexed by } i = 1, 2, \ldots, I. \\
& J: \text{Set of consultants, indexed by } j = 1, 2, \ldots, J.
\end{align*}

\subsection*{Parameters}
\begin{align*}
& f_j: \text{Fixed cost of hiring consultant } j, \quad j \in J. \\
& c_{i,j}: \text{Cost of assigning project } i \text{ to consultant } j, \quad i \in I, j \in J. \\
& K: \text{Maximum number of projects a consultant can handle.}
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
& x_{i,j} = 
\begin{cases} 
1, & \text{if project } i \text{ is assigned to consultant } j, \\
0, & \text{otherwise.} 
\end{cases} \\
& y_j = 
\begin{cases} 
1, & \text{if consultant } j \text{ is hired,} \\
0, & \text{otherwise.} 
\end{cases}
\end{align*}

\subsection*{Objective Function}
Minimize the total cost, which includes both the hiring and project assignment costs:
\begin{align*}
\text{Minimize } & \quad \sum_{j=1}^{J} f_j y_j + \sum_{i=1}^{I} \sum_{j=1}^{J} c_{i,j} x_{i,j}
\end{align*}

\subsection*{Constraints}
\begin{align*}
& \text{Each project must be assigned to exactly one consultant:} \\
& \quad \sum_{j=1}^{J} x_{i,j} = 1, \quad \forall i \in I. \\
& \text{A consultant must be hired before they are assigned any project:} \\
& \quad x_{i,j} \leq y_j, \quad \forall i \in I, j \in J. \\
& \text{A consultant can handle at most } K \text{ projects:} \\
& \quad \sum_{i=1}^{I} x_{i,j} \leq K y_j, \quad \forall j \in J. \\
& \text{Binary constraints for decision variables:} \\
& \quad x_{i,j} \in \{0, 1\}, \quad \forall i \in I, j \in J. \\
& \quad y_j \in \{0, 1\}, \quad \forall j \in J.
\end{align*}

\end{document}
```

This mathematical model defines the necessary constraints and objective function to determine the optimal assignment of projects to consultants. It ensures that each project is assigned to exactly one consultant, each consultant can only be assigned a limited number of projects as specified, and the total cost is minimized.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{amsfonts}
\begin{document}

\section*{MILP Formulation for Consultant Project Assignment}

\subsection*{Sets and Indices}
\begin{align*}
& I: \text{Set of projects, indexed by } i = 1, 2, \ldots, I. \\
& J: \text{Set of consultants, indexed by } j = 1, 2, \ldots, J.
\end{align*}

\subsection*{Parameters}
\begin{align*}
& f_j: \text{Fixed cost of hiring consultant } j, \quad j \in J. \\
& c_{i,j}: \text{Cost of assigning project } i \text{ to consultant } j, \quad i \in I, j \in J. \\
& K: \text{Maximum number of projects a consultant can handle.}
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
& x_{i,j} = 
\begin{cases} 
1, & \text{if project } i \text{ is assigned to consultant } j, \\
0, & \text{otherwise.} 
\end{cases} \\
& y_j = 
\begin{cases} 
1, & \text{if consultant } j \text{ is hired,} \\
0, & \text{otherwise.} 
\end{cases}
\end{align*}

\subsection*{Objective Function}
Minimize the total cost, which includes both the hiring and project assignment costs:
\begin{align*}
\text{Minimize } & \quad \sum_{j=1}^{J} f_j y_j + \sum_{i=1}^{I} \sum_{j=1}^{J} c_{i,j} x_{i,j}
\end{align*}

\subsection*{Constraints}
\begin{align*}
& \text{Each project must be assigned to exactly one consultant:} \\
& \quad \sum_{j=1}^{J} x_{i,j} = 1, \quad \forall i \in I. \\
& \text{A consultant must be hired before they are assigned any project:} \\
& \quad x_{i,j} \leq y_j, \quad \forall i \in I, j \in J. \\
& \text{A consultant can handle at most } K \text{ projects:} \\
& \quad \sum_{i=1}^{I} x_{i,j} \leq K y_j, \quad \forall j \in J. \\
& \text{Binary constraints for decision variables:} \\
& \quad x_{i,j} \in \{0, 1\}, \quad \forall i \in I, j \in J. \\
& \quad y_j \in \{0, 1\}, \quad \forall j \in J.
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'fixed_costs': [100, 150, 135], 'additional_costs': [[10, 12, 20], [10, 8, 12], [15, 8, 20], [10, 6, 15], [8, 10, 15]], 'max_projects_per_consultant': 3}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
fixed_costs = [100, 150, 135]
additional_costs = [
    [10, 12, 20],
    [10, 8, 12],
    [15, 8, 20],
    [10, 6, 15],
    [8, 10, 15]
]
max_projects_per_consultant = 3

#### Indices
I = range(len(additional_costs))  #### Projects
J = range(len(fixed_costs))       #### Consultants

#### Create the problem
problem = pulp.LpProblem("Consultant_Project_Assignment", pulp.LpMinimize)

#### Decision Variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in I for j in J), cat='Binary')
y = pulp.LpVariable.dicts("y", (j for j in J), cat='Binary')

#### Objective Function
problem += (
    pulp.lpSum(fixed_costs[j] * y[j] for j in J) +
    pulp.lpSum(additional_costs[i][j] * x[(i, j)] for i in I for j in J)
), "Total Cost"

#### Constraints

#### Each project must be assigned to exactly one consultant
for i in I:
    problem += (
        pulp.lpSum(x[(i, j)] for j in J) == 1
    ), f"Project_Assignment_{i}"

#### A consultant must be hired before they are assigned any project
for i in I:
    for j in J:
        problem += (
            x[(i, j)] <= y[j]
        ), f"Consultant_Hired_{i}_{j}"

#### A consultant can handle at most K projects
for j in J:
    problem += (
        pulp.lpSum(x[(i, j)] for i in I) <= max_projects_per_consultant * y[j]
    ), f"Max_Projects_{j}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

