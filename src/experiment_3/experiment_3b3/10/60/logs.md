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

\subsection*{Sets}
\begin{itemize}
    \item Let \( I \) be the set of projects, indexed by \( i \).
    \item Let \( J \) be the set of consultants, indexed by \( j \).
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( f_j \): Fixed cost of hiring consultant \( j \), for \( j \in J \).
    \item \( c_{i,j} \): Additional cost of assigning project \( i \) to consultant \( j \), for \( i \in I \) and \( j \in J \).
    \item \( K \): Maximum number of projects that can be assigned to a consultant.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( x_{j} \): Binary variable, \( x_{j} = 1 \) if consultant \( j \) is hired, and \( x_{j} = 0 \) otherwise.
    \item \( y_{i,j} \): Binary variable, \( y_{i,j} = 1 \) if project \( i \) is assigned to consultant \( j \), and \( y_{i,j} = 0 \) otherwise.
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost:
\[
\text{Minimize} \quad Z = \sum_{j \in J} f_j x_j + \sum_{i \in I} \sum_{j \in J} c_{i,j} y_{i,j}
\]

\subsection*{Constraints}
1. Each project must be assigned to exactly one consultant:
\[
\sum_{j \in J} y_{i,j} = 1 \quad \forall i \in I
\]

2. The number of projects assigned to each consultant cannot exceed \( K \):
\[
\sum_{i \in I} y_{i,j} \leq K x_j \quad \forall j \in J
\]

3. The assignments must be binary:
\[
x_j \in \{0,1\} \quad \forall j \in J
\]
\[
y_{i,j} \in \{0,1\} \quad \forall i \in I, \forall j \in J
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

\subsection*{Sets}
\begin{itemize}
    \item Let \( I \) be the set of projects, indexed by \( i \).
    \item Let \( J \) be the set of consultants, indexed by \( j \).
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( f_j \): Fixed cost of hiring consultant \( j \), for \( j \in J \).
    \item \( c_{i,j} \): Additional cost of assigning project \( i \) to consultant \( j \), for \( i \in I \) and \( j \in J \).
    \item \( K \): Maximum number of projects that can be assigned to a consultant.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( x_{j} \): Binary variable, \( x_{j} = 1 \) if consultant \( j \) is hired, and \( x_{j} = 0 \) otherwise.
    \item \( y_{i,j} \): Binary variable, \( y_{i,j} = 1 \) if project \( i \) is assigned to consultant \( j \), and \( y_{i,j} = 0 \) otherwise.
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost:
\[
\text{Minimize} \quad Z = \sum_{j \in J} f_j x_j + \sum_{i \in I} \sum_{j \in J} c_{i,j} y_{i,j}
\]

\subsection*{Constraints}
1. Each project must be assigned to exactly one consultant:
\[
\sum_{j \in J} y_{i,j} = 1 \quad \forall i \in I
\]

2. The number of projects assigned to each consultant cannot exceed \( K \):
\[
\sum_{i \in I} y_{i,j} \leq K x_j \quad \forall j \in J
\]

3. The assignments must be binary:
\[
x_j \in \{0,1\} \quad \forall j \in J
\]
\[
y_{i,j} \in \{0,1\} \quad \forall i \in I, \forall j \in J
\]

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

#### Sets
I = range(len(additional_costs))  #### Projects
J = range(len(fixed_costs))       #### Consultants

#### Create the LP problem
problem = pulp.LpProblem("Consultant_Assignment_Problem", pulp.LpMinimize)

#### Decision Variables
x = pulp.LpVariable.dicts("x", J, cat='Binary')  #### Binary hire decision for each consultant
y = pulp.LpVariable.dicts("y", (I, J), cat='Binary')  #### Binary assignment for each project to consultants

#### Objective Function
problem += pulp.lpSum([fixed_costs[j] * x[j] for j in J]) + \
           pulp.lpSum([additional_costs[i][j] * y[i][j] for i in I for j in J]), "Total Cost"

#### Constraints
#### Each project must be assigned to exactly one consultant
for i in I:
    problem += pulp.lpSum([y[i][j] for j in J]) == 1, f"Project_Assignment_{i}"

#### The number of projects assigned to each consultant cannot exceed max_projects_per_consultant
for j in J:
    problem += pulp.lpSum([y[i][j] for i in I]) <= max_projects_per_consultant * x[j], f"Max_Projects_{j}"

#### Solve the problem
problem.solve()

#### Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

