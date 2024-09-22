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

\section*{Mathematical Model for Project Assignment Problem}

\subsection*{Sets}
\begin{itemize}
    \item Let \( I \) be the set of projects, indexed by \( i \).
    \item Let \( J \) be the set of consultants, indexed by \( j \).
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( f_j \): Fixed cost of hiring consultant \( j \).
    \item \( c_{i,j} \): Additional cost of assigning project \( i \) to consultant \( j \).
    \item \( K \): Maximum number of projects that can be assigned to any consultant.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( x_{j} \): Binary variable, \( x_{j} = 1 \) if consultant \( j \) is hired, \( 0 \) otherwise.
    \item \( a_{i,j} \): Binary variable, \( a_{i,j} = 1 \) if project \( i \) is assigned to consultant \( j \), \( 0 \) otherwise.
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost:

\[
\text{minimize} \quad Z = \sum_{j=1}^{J} f_j x_j + \sum_{i=1}^{I} \sum_{j=1}^{J} c_{i,j} a_{i,j}
\]

\subsection*{Constraints}
\begin{itemize}
    \item Each project must be assigned to exactly one consultant:
    \[
    \sum_{j=1}^{J} a_{i,j} = 1, \quad \forall i \in I
    \]

    \item A consultant can only assign projects if they are hired:
    \[
    a_{i,j} \leq x_j, \quad \forall i \in I, \forall j \in J
    \]

    \item Each consultant can be assigned a maximum of \( K \) projects:
    \[
    \sum_{i=1}^{I} a_{i,j} \leq K x_j, \quad \forall j \in J
    \]

    \item Binary constraints on decision variables:
    \[
    x_j \in \{0, 1\}, \quad a_{i,j} \in \{0, 1\}, \quad \forall i \in I, \forall j \in J
    \]
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

\section*{Mathematical Model for Project Assignment Problem}

\subsection*{Sets}
\begin{itemize}
    \item Let \( I \) be the set of projects, indexed by \( i \).
    \item Let \( J \) be the set of consultants, indexed by \( j \).
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( f_j \): Fixed cost of hiring consultant \( j \).
    \item \( c_{i,j} \): Additional cost of assigning project \( i \) to consultant \( j \).
    \item \( K \): Maximum number of projects that can be assigned to any consultant.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( x_{j} \): Binary variable, \( x_{j} = 1 \) if consultant \( j \) is hired, \( 0 \) otherwise.
    \item \( a_{i,j} \): Binary variable, \( a_{i,j} = 1 \) if project \( i \) is assigned to consultant \( j \), \( 0 \) otherwise.
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost:

\[
\text{minimize} \quad Z = \sum_{j=1}^{J} f_j x_j + \sum_{i=1}^{I} \sum_{j=1}^{J} c_{i,j} a_{i,j}
\]

\subsection*{Constraints}
\begin{itemize}
    \item Each project must be assigned to exactly one consultant:
    \[
    \sum_{j=1}^{J} a_{i,j} = 1, \quad \forall i \in I
    \]

    \item A consultant can only assign projects if they are hired:
    \[
    a_{i,j} \leq x_j, \quad \forall i \in I, \forall j \in J
    \]

    \item Each consultant can be assigned a maximum of \( K \) projects:
    \[
    \sum_{i=1}^{I} a_{i,j} \leq K x_j, \quad \forall j \in J
    \]

    \item Binary constraints on decision variables:
    \[
    x_j \in \{0, 1\}, \quad a_{i,j} \in \{0, 1\}, \quad \forall i \in I, \forall j \in J
    \]
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'fixed_costs': [100, 150, 135], 'additional_costs': [[10, 12, 20], [10, 8, 12], [15, 8, 20], [10, 6, 15], [8, 10, 15]], 'max_projects_per_consultant': 3}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
fixed_costs = [100, 150, 135]  #### Fixed costs for consultants
additional_costs = [[10, 12, 20], [10, 8, 12], [15, 8, 20], [10, 6, 15], [8, 10, 15]]  #### Additional costs for projects
max_projects_per_consultant = 3  #### Maximum projects per consultant

#### Sets
I = range(len(additional_costs))  #### Projects
J = range(len(fixed_costs))  #### Consultants

#### Create the problem
problem = pulp.LpProblem("Project Assignment Problem", pulp.LpMinimize)

#### Decision Variables
x = pulp.LpVariable.dicts("x", J, cat='Binary')  #### Consultant hired
a = pulp.LpVariable.dicts("a", (I, J), cat='Binary')  #### Project i assigned to consultant j

#### Objective Function
problem += pulp.lpSum([fixed_costs[j] * x[j] for j in J]) + \
           pulp.lpSum([additional_costs[i][j] * a[i][j] for i in I for j in J]), "Total Cost"

#### Constraints
#### Each project must be assigned to exactly one consultant
for i in I:
    problem += pulp.lpSum([a[i][j] for j in J]) == 1, f"Project_Assignment_{i}"

#### A consultant can only assign projects if they are hired
for i in I:
    for j in J:
        problem += a[i][j] <= x[j], f"Consultant_Hired_{i}_{j}"

#### Each consultant can be assigned a maximum of K projects
for j in J:
    problem += pulp.lpSum([a[i][j] for i in I]) <= max_projects_per_consultant * x[j], f"Max_Projects_Consultant_{j}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

# START: PY_F 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Fix syntax error in python code which is implementation of matematical model. You receive wrong code between: <WRONG_CODE></WRONG_CODE> You receive error messages between: <CODE_ERROR></CODE_ERROR> Do not change data format! Do not use `while` loop in python code! Do not change code business logic, fix only syntax errors! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<WRONG_CODE>
```python
import pulp

#### Data
fixed_costs = [100, 150, 135]  #### Fixed costs for consultants
additional_costs = [[10, 12, 20], [10, 8, 12], [15, 8, 20], [10, 6, 15], [8, 10, 15]]  #### Additional costs for projects
max_projects_per_consultant = 3  #### Maximum projects per consultant

#### Sets
I = range(len(additional_costs))  #### Projects
J = range(len(fixed_costs))  #### Consultants

#### Create the problem
problem = pulp.LpProblem("Project Assignment Problem", pulp.LpMinimize)

#### Decision Variables
x = pulp.LpVariable.dicts("x", J, cat='Binary')  #### Consultant hired
a = pulp.LpVariable.dicts("a", (I, J), cat='Binary')  #### Project i assigned to consultant j

#### Objective Function
problem += pulp.lpSum([fixed_costs[j] * x[j] for j in J]) + \
           pulp.lpSum([additional_costs[i][j] * a[i][j] for i in I for j in J]), "Total Cost"

#### Constraints
#### Each project must be assigned to exactly one consultant
for i in I:
    problem += pulp.lpSum([a[i][j] for j in J]) == 1, f"Project_Assignment_{i}"

#### A consultant can only assign projects if they are hired
for i in I:
    for j in J:
        problem += a[i][j] <= x[j], f"Consultant_Hired_{i}_{j}"

#### Each consultant can be assigned a maximum of K projects
for j in J:
    problem += pulp.lpSum([a[i][j] for i in I]) <= max_projects_per_consultant * x[j], f"Max_Projects_Consultant_{j}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')```
</WRONG_CODE>
<CODE_ERROR>
/Users/kwiecs01/PrivProjects/MasterDegreeV2/venv/lib/python3.11/site-packages/pulp/pulp.py:1298: UserWarning: Spaces are not permitted in the name. Converted to '_'
  warnings.warn("Spaces are not permitted in the name. Converted to '_'")
</CODE_ERROR>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
fixed_costs = [100, 150, 135]  #### Fixed costs for consultants
additional_costs = [[10, 12, 20], [10, 8, 12], [15, 8, 20], [10, 6, 15], [8, 10, 15]]  #### Additional costs for projects
max_projects_per_consultant = 3  #### Maximum projects per consultant

#### Sets
I = range(len(additional_costs))  #### Projects
J = range(len(fixed_costs))  #### Consultants

#### Create the problem
problem = pulp.LpProblem("Project_Assignment_Problem", pulp.LpMinimize)

#### Decision Variables
x = pulp.LpVariable.dicts("x", J, cat='Binary')  #### Consultant hired
a = pulp.LpVariable.dicts("a", (I, J), cat='Binary')  #### Project i assigned to consultant j

#### Objective Function
problem += pulp.lpSum([fixed_costs[j] * x[j] for j in J]) + \
           pulp.lpSum([additional_costs[i][j] * a[i][j] for i in I for j in J]), "Total_Cost"

#### Constraints
#### Each project must be assigned to exactly one consultant
for i in I:
    problem += pulp.lpSum([a[i][j] for j in J]) == 1, f"Project_Assignment_{i}"

#### A consultant can only assign projects if they are hired
for i in I:
    for j in J:
        problem += a[i][j] <= x[j], f"Consultant_Hired_{i}_{j}"

#### Each consultant can be assigned a maximum of K projects
for j in J:
    problem += pulp.lpSum([a[i][j] for i in I]) <= max_projects_per_consultant * x[j], f"Max_Projects_Consultant_{j}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

