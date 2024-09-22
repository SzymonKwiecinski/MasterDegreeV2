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
    \item \( I \): Number of projects
    \item \( J \): Number of consultants
    \item \( K \): Maximum number of projects that can be assigned to a consultant
    \item \( f_j \): Fixed cost for hiring consultant \( j \), for \( j = 1, \ldots, J \)
    \item \( c_{i,j} \): Additional cost of assigning project \( i \) to consultant \( j \), for \( i = 1, \ldots, I \) and \( j = 1, \ldots, J \)
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( x_{j} \): Binary variable indicating whether consultant \( j \) is hired (1) or not (0) for \( j = 1, \ldots, J \)
    \item \( a_{i,j} \): Binary variable indicating whether project \( i \) is assigned to consultant \( j \) (1) or not (0) for \( i = 1, \ldots, I \) and \( j = 1, \ldots, J \)
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost:
\[
\text{Minimize } Z = \sum_{j=1}^{J} f_j x_j + \sum_{i=1}^{I} \sum_{j=1}^{J} c_{i,j} a_{i,j}
\]

\subsection*{Constraints}
1. Each project must be assigned to exactly one consultant:
\[
\sum_{j=1}^{J} a_{i,j} = 1, \quad \forall i = 1, \ldots, I
\]

2. A consultant can only be assigned projects if they are hired:
\[
a_{i,j} \leq x_j, \quad \forall i = 1, \ldots, I, \quad j = 1, \ldots, J
\]

3. A consultant can take on at most \( K \) projects:
\[
\sum_{i=1}^{I} a_{i,j} \leq K x_j, \quad \forall j = 1, \ldots, J
\]

4. Binary constraints:
\[
x_j \in \{0, 1\}, \quad \forall j = 1, \ldots, J
\]
\[
a_{i,j} \in \{0, 1\}, \quad \forall i = 1, \ldots, I, \quad j = 1, \ldots, J
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

\section*{Mathematical Model for Consultant Assignment Problem}

\subsection*{Parameters}
\begin{itemize}
    \item \( I \): Number of projects
    \item \( J \): Number of consultants
    \item \( K \): Maximum number of projects that can be assigned to a consultant
    \item \( f_j \): Fixed cost for hiring consultant \( j \), for \( j = 1, \ldots, J \)
    \item \( c_{i,j} \): Additional cost of assigning project \( i \) to consultant \( j \), for \( i = 1, \ldots, I \) and \( j = 1, \ldots, J \)
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( x_{j} \): Binary variable indicating whether consultant \( j \) is hired (1) or not (0) for \( j = 1, \ldots, J \)
    \item \( a_{i,j} \): Binary variable indicating whether project \( i \) is assigned to consultant \( j \) (1) or not (0) for \( i = 1, \ldots, I \) and \( j = 1, \ldots, J \)
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost:
\[
\text{Minimize } Z = \sum_{j=1}^{J} f_j x_j + \sum_{i=1}^{I} \sum_{j=1}^{J} c_{i,j} a_{i,j}
\]

\subsection*{Constraints}
1. Each project must be assigned to exactly one consultant:
\[
\sum_{j=1}^{J} a_{i,j} = 1, \quad \forall i = 1, \ldots, I
\]

2. A consultant can only be assigned projects if they are hired:
\[
a_{i,j} \leq x_j, \quad \forall i = 1, \ldots, I, \quad j = 1, \ldots, J
\]

3. A consultant can take on at most \( K \) projects:
\[
\sum_{i=1}^{I} a_{i,j} \leq K x_j, \quad \forall j = 1, \ldots, J
\]

4. Binary constraints:
\[
x_j \in \{0, 1\}, \quad \forall j = 1, \ldots, J
\]
\[
a_{i,j} \in \{0, 1\}, \quad \forall i = 1, \ldots, I, \quad j = 1, \ldots, J
\]

\end{document}</MATH_MODEL>
<DATA>
{'fixed_costs': [100, 150, 135], 'additional_costs': [[10, 12, 20], [10, 8, 12], [15, 8, 20], [10, 6, 15], [8, 10, 15]], 'max_projects_per_consultant': 3}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the provided JSON-like format
data = {
    'fixed_costs': [100, 150, 135],
    'additional_costs': [[10, 12, 20], [10, 8, 12], [15, 8, 20], [10, 6, 15], [8, 10, 15]],
    'max_projects_per_consultant': 3
}

#### Parameters
I = len(data['additional_costs'])  #### Number of projects
J = len(data['fixed_costs'])        #### Number of consultants
K = data['max_projects_per_consultant']  #### Max projects per consultant

#### Create the problem
problem = pulp.LpProblem("Consultant_Assignment_Problem", pulp.LpMinimize)

#### Decision Variables
x = pulp.LpVariable.dicts("x", range(J), cat='Binary')  #### Consultant hired
a = pulp.LpVariable.dicts("a", (range(I), range(J)), cat='Binary')  #### Project assignment

#### Objective Function
problem += pulp.lpSum(data['fixed_costs'][j] * x[j] for j in range(J)) + \
           pulp.lpSum(data['additional_costs'][i][j] * a[i][j] for i in range(I) for j in range(J))

#### Constraints

#### Each project must be assigned to exactly one consultant
for i in range(I):
    problem += pulp.lpSum(a[i][j] for j in range(J)) == 1
    
#### A consultant can only be assigned projects if they are hired
for i in range(I):
    for j in range(J):
        problem += a[i][j] <= x[j]
        
#### A consultant can take on at most K projects
for j in range(J):
    problem += pulp.lpSum(a[i][j] for i in range(I)) <= K * x[j]

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

