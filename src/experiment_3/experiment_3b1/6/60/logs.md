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
    \item Let \( I \) be the number of projects.
    \item Let \( J \) be the number of consultants.
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( f_j \): Fixed cost of hiring consultant \( j \) for \( j = 1, \ldots, J \).
    \item \( c_{i,j} \): Additional cost of assigning project \( i \) to consultant \( j \) for \( i = 1, \ldots, I \) and \( j = 1, \ldots, J \).
    \item \( K \): Maximum number of projects that can be assigned to each consultant.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( x_{i,j} \): Binary variable equal to 1 if project \( i \) is assigned to consultant \( j \), and 0 otherwise.
    \item \( y_j \): Binary variable equal to 1 if consultant \( j \) is hired, and 0 otherwise.
\end{itemize}

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

2. A consultant can only work on a maximum of \( K \) projects:
\[
\sum_{i=1}^{I} x_{i,j} \leq K y_j, \quad \forall j = 1, \ldots, J
\]

3. A project can only be assigned to a consultant if that consultant is hired:
\[
x_{i,j} \leq y_j, \quad \forall i = 1, \ldots, I, \forall j = 1, \ldots, J
\]

4. Binary constraints on decision variables:
\[
x_{i,j} \in \{0, 1\}, \quad \forall i = 1, \ldots, I, \forall j = 1, \ldots, J
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

\section*{Mathematical Model for Consultant Assignment Problem}

\subsection*{Sets}
\begin{itemize}
    \item Let \( I \) be the number of projects.
    \item Let \( J \) be the number of consultants.
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( f_j \): Fixed cost of hiring consultant \( j \) for \( j = 1, \ldots, J \).
    \item \( c_{i,j} \): Additional cost of assigning project \( i \) to consultant \( j \) for \( i = 1, \ldots, I \) and \( j = 1, \ldots, J \).
    \item \( K \): Maximum number of projects that can be assigned to each consultant.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( x_{i,j} \): Binary variable equal to 1 if project \( i \) is assigned to consultant \( j \), and 0 otherwise.
    \item \( y_j \): Binary variable equal to 1 if consultant \( j \) is hired, and 0 otherwise.
\end{itemize}

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

2. A consultant can only work on a maximum of \( K \) projects:
\[
\sum_{i=1}^{I} x_{i,j} \leq K y_j, \quad \forall j = 1, \ldots, J
\]

3. A project can only be assigned to a consultant if that consultant is hired:
\[
x_{i,j} \leq y_j, \quad \forall i = 1, \ldots, I, \forall j = 1, \ldots, J
\]

4. Binary constraints on decision variables:
\[
x_{i,j} \in \{0, 1\}, \quad \forall i = 1, \ldots, I, \forall j = 1, \ldots, J
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

#### Data initialization from provided JSON
data = {
    'fixed_costs': [100, 150, 135],
    'additional_costs': [[10, 12, 20], [10, 8, 12], [15, 8, 20], [10, 6, 15], [8, 10, 15]],
    'max_projects_per_consultant': 3
}

#### Define sets
I = len(data['additional_costs'])  #### Number of projects
J = len(data['fixed_costs'])        #### Number of consultants

#### Fixed costs and additional costs
f = data['fixed_costs']
c = data['additional_costs']
K = data['max_projects_per_consultant']

#### Create the problem
problem = pulp.LpProblem("Consultant_Assignment_Problem", pulp.LpMinimize)

#### Decision variables
x = pulp.LpVariable.dicts("x", (range(I), range(J)), cat='Binary')  #### Project assignment
y = pulp.LpVariable.dicts("y", range(J), cat='Binary')              #### Consultant hiring

#### Objective function
problem += pulp.lpSum(f[j] * y[j] for j in range(J)) + pulp.lpSum(c[i][j] * x[i][j] for i in range(I) for j in range(J)), "Total_Cost"

#### Constraints
#### Each project must be assigned to exactly one consultant
for i in range(I):
    problem += pulp.lpSum(x[i][j] for j in range(J)) == 1, f"Assign_Project_{i}"

#### A consultant can only work on a maximum of K projects
for j in range(J):
    problem += pulp.lpSum(x[i][j] for i in range(I)) <= K * y[j], f"Max_Projects_Consultant_{j}"

#### A project can only be assigned to a consultant if that consultant is hired
for i in range(I):
    for j in range(J):
        problem += x[i][j] <= y[j], f"Project_Assignment_Consultant_{i}_{j}"

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

