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
To solve this problem, we need to formulate a Mixed Integer Linear Programming (MILP) model. Our objective is to minimize the total cost of hiring consultants and assigning projects subject to the constraints given.

Below is the MILP model in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\textbf{Objective:} Minimize the total cost of hiring consultants and assigning projects.

\section*{Sets}
\begin{align*}
    I & : \text{Set of projects, indexed by } i. \\
    J & : \text{Set of consultants, indexed by } j.
\end{align*}

\section*{Parameters}
\begin{align*}
    f_j & : \text{Fixed cost of hiring consultant } j. \\
    c_{i,j} & : \text{Cost of assigning project } i \text{ to consultant } j. \\
    K & : \text{Maximum number of projects a consultant can be assigned.}
\end{align*}

\section*{Decision Variables}
\begin{align*}
    x_{i,j} & = 
    \begin{cases} 
    1, & \text{if project } i \text{ is assigned to consultant } j; \\
    0, & \text{otherwise.}
    \end{cases} \\
    y_j & = 
    \begin{cases} 
    1, & \text{if consultant } j \text{ is hired;} \\
    0, & \text{otherwise.}
    \end{cases}
\end{align*}

\section*{Objective Function}
Minimize the total cost:
\begin{equation}
    \text{Total Cost} = \sum_{j \in J} f_j \cdot y_j + \sum_{i \in I} \sum_{j \in J} c_{i,j} \cdot x_{i,j}
\end{equation}

\section*{Constraints}
\begin{align*}
    & \text{1. Each project is assigned to exactly one consultant:} \\
    & \quad \sum_{j \in J} x_{i,j} = 1, \quad \forall i \in I. \\
    & \text{2. A consultant is not assigned more than } K \text{ projects:} \\
    & \quad \sum_{i \in I} x_{i,j} \leq K, \quad \forall j \in J. \\
    & \text{3. A project is assigned to a consultant only if they are hired:} \\
    & \quad x_{i,j} \leq y_j, \quad \forall i \in I, \forall j \in J. \\
    & \text{4. Binary constraints on decision variables:} \\
    & \quad x_{i,j} \in \{0, 1\}, \quad \forall i \in I, \forall j \in J. \\
    & \quad y_j \in \{0, 1\}, \quad \forall j \in J.
\end{align*}

\end{document}
```

This model captures the problem constraints and objectives as described, allowing it to be solved using a MILP solver to determine the optimal assignments and total cost.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\textbf{Objective:} Minimize the total cost of hiring consultants and assigning projects.

\section*{Sets}
\begin{align*}
    I & : \text{Set of projects, indexed by } i. \\
    J & : \text{Set of consultants, indexed by } j.
\end{align*}

\section*{Parameters}
\begin{align*}
    f_j & : \text{Fixed cost of hiring consultant } j. \\
    c_{i,j} & : \text{Cost of assigning project } i \text{ to consultant } j. \\
    K & : \text{Maximum number of projects a consultant can be assigned.}
\end{align*}

\section*{Decision Variables}
\begin{align*}
    x_{i,j} & = 
    \begin{cases} 
    1, & \text{if project } i \text{ is assigned to consultant } j; \\
    0, & \text{otherwise.}
    \end{cases} \\
    y_j & = 
    \begin{cases} 
    1, & \text{if consultant } j \text{ is hired;} \\
    0, & \text{otherwise.}
    \end{cases}
\end{align*}

\section*{Objective Function}
Minimize the total cost:
\begin{equation}
    \text{Total Cost} = \sum_{j \in J} f_j \cdot y_j + \sum_{i \in I} \sum_{j \in J} c_{i,j} \cdot x_{i,j}
\end{equation}

\section*{Constraints}
\begin{align*}
    & \text{1. Each project is assigned to exactly one consultant:} \\
    & \quad \sum_{j \in J} x_{i,j} = 1, \quad \forall i \in I. \\
    & \text{2. A consultant is not assigned more than } K \text{ projects:} \\
    & \quad \sum_{i \in I} x_{i,j} \leq K, \quad \forall j \in J. \\
    & \text{3. A project is assigned to a consultant only if they are hired:} \\
    & \quad x_{i,j} \leq y_j, \quad \forall i \in I, \forall j \in J. \\
    & \text{4. Binary constraints on decision variables:} \\
    & \quad x_{i,j} \in \{0, 1\}, \quad \forall i \in I, \forall j \in J. \\
    & \quad y_j \in \{0, 1\}, \quad \forall j \in J.
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

#### Extract data
fixed_costs = data['fixed_costs']
additional_costs = data['additional_costs']
K = data['max_projects_per_consultant']

#### Sets
projects = range(len(additional_costs))
consultants = range(len(fixed_costs))

#### Problem
problem = pulp.LpProblem("ConsultantAssignment", pulp.LpMinimize)

#### Decision Variables
x = pulp.LpVariable.dicts("x", [(i, j) for i in projects for j in consultants], cat='Binary')
y = pulp.LpVariable.dicts("y", consultants, cat='Binary')

#### Objective Function
problem += pulp.lpSum(fixed_costs[j] * y[j] for j in consultants) + \
           pulp.lpSum(additional_costs[i][j] * x[(i, j)] for i in projects for j in consultants)

#### Constraints

#### 1. Each project is assigned to exactly one consultant
for i in projects:
    problem += pulp.lpSum(x[(i, j)] for j in consultants) == 1

#### 2. A consultant is not assigned more than K projects
for j in consultants:
    problem += pulp.lpSum(x[(i, j)] for i in projects) <= K

#### 3. A project is assigned to a consultant only if they are hired
for i in projects:
    for j in consultants:
        problem += x[(i, j)] <= y[j]

#### Solve
problem.solve()

#### Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

