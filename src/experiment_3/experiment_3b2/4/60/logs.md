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
To create a mathematical model for this problem, we will use a Mixed Integer Linear Programming (MILP) approach. We'll define binary variables to represent the assignment of projects to consultants, as well as the hiring status of each consultant. The goal is to minimize the total cost, which includes both the fixed costs of hiring consultants and the additional costs of assigning projects to consultants.

Below is the LATEX code for the formulation of the MILP problem:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{MILP Formulation}

\subsection*{Sets and Indices}
\begin{itemize}
    \item \( I \): Set of projects, indexed by \( i \).
    \item \( J \): Set of consultants, indexed by \( j \).
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( f_j \): Fixed cost of hiring consultant \( j \).
    \item \( c_{i,j} \): Additional cost of assigning project \( i \) to consultant \( j \).
    \item \( K \): Maximum number of projects a consultant can be assigned.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( x_{i,j} \): Binary variable, \( x_{i,j} = 1 \) if project \( i \) is assigned to consultant \( j \), 0 otherwise.
    \item \( y_j \): Binary variable, \( y_j = 1 \) if consultant \( j \) is hired, 0 otherwise.
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost:
\[
\min \sum_{j \in J} f_j y_j + \sum_{i \in I} \sum_{j \in J} c_{i,j} x_{i,j}
\]

\subsection*{Constraints}
\begin{align}
    & \sum_{j \in J} x_{i,j} = 1, \quad \forall i \in I & \text{(Each project is assigned to exactly one consultant)} \\
    & \sum_{i \in I} x_{i,j} \leq K y_j, \quad \forall j \in J & \text{(Limit the number of projects per consultant)} \\
    & x_{i,j} \leq y_j, \quad \forall i \in I, \forall j \in J & \text{(Project can only be assigned if consultant is hired)} \\
    & x_{i,j} \in \{0,1\}, \quad \forall i \in I, \forall j \in J & \text{(Binary variables for assignment)} \\
    & y_j \in \{0,1\}, \quad \forall j \in J & \text{(Binary variables for hiring)}
\end{align}

\end{document}
```

This model ensures each project is assigned to exactly one consultant while respecting the maximum number of projects a consultant can handle. The objective function seeks to minimize the combined fixed and additional costs. The constraints ensure feasible project assignments in accordance with the problem's requirements.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{MILP Formulation}

\subsection*{Sets and Indices}
\begin{itemize}
    \item \( I \): Set of projects, indexed by \( i \).
    \item \( J \): Set of consultants, indexed by \( j \).
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( f_j \): Fixed cost of hiring consultant \( j \).
    \item \( c_{i,j} \): Additional cost of assigning project \( i \) to consultant \( j \).
    \item \( K \): Maximum number of projects a consultant can be assigned.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( x_{i,j} \): Binary variable, \( x_{i,j} = 1 \) if project \( i \) is assigned to consultant \( j \), 0 otherwise.
    \item \( y_j \): Binary variable, \( y_j = 1 \) if consultant \( j \) is hired, 0 otherwise.
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost:
\[
\min \sum_{j \in J} f_j y_j + \sum_{i \in I} \sum_{j \in J} c_{i,j} x_{i,j}
\]

\subsection*{Constraints}
\begin{align}
    & \sum_{j \in J} x_{i,j} = 1, \quad \forall i \in I & \text{(Each project is assigned to exactly one consultant)} \\
    & \sum_{i \in I} x_{i,j} \leq K y_j, \quad \forall j \in J & \text{(Limit the number of projects per consultant)} \\
    & x_{i,j} \leq y_j, \quad \forall i \in I, \forall j \in J & \text{(Project can only be assigned if consultant is hired)} \\
    & x_{i,j} \in \{0,1\}, \quad \forall i \in I, \forall j \in J & \text{(Binary variables for assignment)} \\
    & y_j \in \{0,1\}, \quad \forall j \in J & \text{(Binary variables for hiring)}
\end{align}

\end{document}</MATH_MODEL>
<DATA>
{'fixed_costs': [100, 150, 135], 'additional_costs': [[10, 12, 20], [10, 8, 12], [15, 8, 20], [10, 6, 15], [8, 10, 15]], 'max_projects_per_consultant': 3}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data input
data = {
    'fixed_costs': [100, 150, 135],
    'additional_costs': [[10, 12, 20], [10, 8, 12], [15, 8, 20], [10, 6, 15], [8, 10, 15]],
    'max_projects_per_consultant': 3
}

#### Sets and indices
I = range(len(data['additional_costs']))  #### Projects
J = range(len(data['fixed_costs']))       #### Consultants

#### Parameters
f = data['fixed_costs']                              #### Fixed costs
c = data['additional_costs']                         #### Additional costs
K = data['max_projects_per_consultant']              #### Maximum projects per consultant

#### Decision Variables
x = pulp.LpVariable.dicts("x", (I, J), cat='Binary')  #### Project assignment variables
y = pulp.LpVariable.dicts("y", J, cat='Binary')       #### Consultant hiring variables

#### Problem definition
problem = pulp.LpProblem("Consultant_Allocation_Problem", pulp.LpMinimize)

#### Objective Function
problem += (pulp.lpSum(f[j] * y[j] for j in J) + 
            pulp.lpSum(c[i][j] * x[i][j] for i in I for j in J))

#### Constraints
#### Each project is assigned to exactly one consultant
for i in I:
    problem += pulp.lpSum(x[i][j] for j in J) == 1

#### Limit the number of projects per consultant
for j in J:
    problem += pulp.lpSum(x[i][j] for i in I) <= K * y[j]

#### Project can only be assigned if the consultant is hired
for i in I:
    for j in J:
        problem += x[i][j] <= y[j]

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

