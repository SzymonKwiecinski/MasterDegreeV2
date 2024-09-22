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

\section*{Mathematical Model for Consultant Assignment Problem}

\subsection*{Parameters}
\begin{itemize}
    \item $I$: Number of projects
    \item $J$: Number of consultants
    \item $K$: Maximum number of projects that can be assigned to a consultant
    \item $f_j$: Fixed cost of hiring consultant $j$ for $j = 1, \ldots, J$
    \item $c_{i,j}$: Additional cost of assigning project $i$ to consultant $j$ for $i = 1, \ldots, I$ and $j = 1, \ldots, J$
\end{itemize}

\subsection*{Decision Variables}
Let $x_{j,i}$ be a binary variable defined as:
\[
x_{j,i} = 
\begin{cases}
1 & \text{if project } i \text{ is assigned to consultant } j \\
0 & \text{otherwise}
\end{cases}
\]

Let $y_j$ be a binary variable defined as:
\[
y_j = 
\begin{cases}
1 & \text{if consultant } j \text{ is hired} \\
0 & \text{otherwise}
\end{cases}
\]

\subsection*{Objective Function}
Minimize the total cost:
\[
\text{Minimize } Z = \sum_{j=1}^{J} f_j y_j + \sum_{i=1}^{I} \sum_{j=1}^{J} c_{i,j} x_{j,i}
\]

\subsection*{Constraints}
\begin{itemize}
    \item Each project must be assigned to exactly one consultant:
    \[
    \sum_{j=1}^{J} x_{j,i} = 1 \quad \forall i = 1, \ldots, I
    \]
    
    \item A consultant can only take on up to $K$ projects:
    \[
    \sum_{i=1}^{I} x_{j,i} \leq K \cdot y_j \quad \forall j = 1, \ldots, J
    \]
    
    \item Binary constraints for decision variables:
    \[
    x_{j,i} \in \{0, 1\} \quad \forall i = 1, \ldots, I, \, j = 1, \ldots, J
    \]
    \[
    y_j \in \{0, 1\} \quad \forall j = 1, \ldots, J
    \]
\end{itemize}

\subsection*{Output}
The output of the model will include:
\begin{itemize}
    \item Assignments: A matrix of size $J \times I$ where each element is $x_{j,i}$ indicating whether project $i$ is assigned to consultant $j$.
    \item Total Cost: The total cost $Z$ as defined in the objective function.
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

\section*{Mathematical Model for Consultant Assignment Problem}

\subsection*{Parameters}
\begin{itemize}
    \item $I$: Number of projects
    \item $J$: Number of consultants
    \item $K$: Maximum number of projects that can be assigned to a consultant
    \item $f_j$: Fixed cost of hiring consultant $j$ for $j = 1, \ldots, J$
    \item $c_{i,j}$: Additional cost of assigning project $i$ to consultant $j$ for $i = 1, \ldots, I$ and $j = 1, \ldots, J$
\end{itemize}

\subsection*{Decision Variables}
Let $x_{j,i}$ be a binary variable defined as:
\[
x_{j,i} = 
\begin{cases}
1 & \text{if project } i \text{ is assigned to consultant } j \\
0 & \text{otherwise}
\end{cases}
\]

Let $y_j$ be a binary variable defined as:
\[
y_j = 
\begin{cases}
1 & \text{if consultant } j \text{ is hired} \\
0 & \text{otherwise}
\end{cases}
\]

\subsection*{Objective Function}
Minimize the total cost:
\[
\text{Minimize } Z = \sum_{j=1}^{J} f_j y_j + \sum_{i=1}^{I} \sum_{j=1}^{J} c_{i,j} x_{j,i}
\]

\subsection*{Constraints}
\begin{itemize}
    \item Each project must be assigned to exactly one consultant:
    \[
    \sum_{j=1}^{J} x_{j,i} = 1 \quad \forall i = 1, \ldots, I
    \]
    
    \item A consultant can only take on up to $K$ projects:
    \[
    \sum_{i=1}^{I} x_{j,i} \leq K \cdot y_j \quad \forall j = 1, \ldots, J
    \]
    
    \item Binary constraints for decision variables:
    \[
    x_{j,i} \in \{0, 1\} \quad \forall i = 1, \ldots, I, \, j = 1, \ldots, J
    \]
    \[
    y_j \in \{0, 1\} \quad \forall j = 1, \ldots, J
    \]
\end{itemize}

\subsection*{Output}
The output of the model will include:
\begin{itemize}
    \item Assignments: A matrix of size $J \times I$ where each element is $x_{j,i}$ indicating whether project $i$ is assigned to consultant $j$.
    \item Total Cost: The total cost $Z$ as defined in the objective function.
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'fixed_costs': [100, 150, 135], 'additional_costs': [[10, 12, 20], [10, 8, 12], [15, 8, 20], [10, 6, 15], [8, 10, 15]], 'max_projects_per_consultant': 3}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
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

#### Unpack data
f = data['fixed_costs']
c = data['additional_costs']
K = data['max_projects_per_consultant']

#### Dimensions
I = len(c)  #### Number of projects
J = len(f)  #### Number of consultants

#### Problem
problem = pulp.LpProblem("ConsultantAssignment", pulp.LpMinimize)

#### Decision variables
x = pulp.LpVariable.dicts('x', ((j, i) for j in range(J) for i in range(I)), cat='Binary')
y = pulp.LpVariable.dicts('y', (j for j in range(J)), cat='Binary')

#### Objective function
problem += pulp.lpSum(f[j] * y[j] for j in range(J)) + pulp.lpSum(c[i][j] * x[(j, i)] for i in range(I) for j in range(J))

#### Constraints
#### Each project must be assigned to exactly one consultant
for i in range(I):
    problem += pulp.lpSum(x[(j, i)] for j in range(J)) == 1

#### A consultant can only take on up to K projects
for j in range(J):
    problem += pulp.lpSum(x[(j, i)] for i in range(I)) <= K * y[j]

#### Solve the problem
problem.solve()

#### Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

#### Assignments matrix
assignments = [[int(x[(j, i)].varValue) for i in range(I)] for j in range(J)]

#### Print assignments
for j in range(J):
    for i in range(I):
        print(f'Consultant {j} assigned to Project {i}: {assignments[j][i]}')

#### Show total cost
print(f'Total Cost: {pulp.value(problem.objective)}')
```

