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
To model this problem as a Mixed-Integer Linear Programming (MILP) problem, we need to define our variables, objective function, and constraints clearly. Here's the mathematical formulation of the problem in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{MILP Formulation for Consultant Assignment Problem}

\subsection*{Indices and Sets}
\begin{itemize}
    \item $I$: Set of projects, indexed by $i$.
    \item $J$: Set of consultants, indexed by $j$.
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item $f_j$: Fixed cost of hiring consultant $j$, for each $j \in J$.
    \item $c_{i,j}$: Additional cost of assigning project $i$ to consultant $j$, for each $i \in I$, $j \in J$.
    \item $K$: Maximum number of projects a consultant can be assigned.
\end{itemize}

\subsection*{Decision Variables}
\begin{align*}
    x_{i,j} &= 
    \begin{cases} 
    1, & \text{if project $i$ is assigned to consultant $j$} \\ 
    0, & \text{otherwise}
    \end{cases} \quad \forall i \in I, \forall j \in J \\
    y_j &= 
    \begin{cases} 
    1, & \text{if consultant $j$ is hired} \\ 
    0, & \text{otherwise}
    \end{cases} \quad \forall j \in J
\end{align*}

\subsection*{Objective Function}
Minimize the total cost:
\[
\text{Minimize} \quad \sum_{j \in J} f_j y_j + \sum_{i \in I} \sum_{j \in J} c_{i,j} x_{i,j}
\]

\subsection*{Constraints}
\begin{align}
    &\sum_{j \in J} x_{i,j} = 1, &\forall i \in I \quad &\text{(Each project is assigned to one consultant)} \\
    &\sum_{i \in I} x_{i,j} \leq K y_j, &\forall j \in J \quad &\text{(Each consultant is assigned up to $K$ projects)} \\
    &x_{i,j} \leq y_j, &\forall i \in I, \forall j \in J \quad &\text{(Projects assigned only if consultant is hired)} \\
    &x_{i,j}, y_j \in \{0, 1\}, &\forall i \in I, \forall j \in J &\text{(Binary decision variables)}
\end{align}

\end{document}
```

This LaTeX code models the problem, enforcing that each project must be assigned to exactly one consultant, a consultant can handle up to a maximum number of projects \( K \), and consultants are only assigned projects if hired, optimizing to minimize the total costs.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{MILP Formulation for Consultant Assignment Problem}

\subsection*{Indices and Sets}
\begin{itemize}
    \item $I$: Set of projects, indexed by $i$.
    \item $J$: Set of consultants, indexed by $j$.
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item $f_j$: Fixed cost of hiring consultant $j$, for each $j \in J$.
    \item $c_{i,j}$: Additional cost of assigning project $i$ to consultant $j$, for each $i \in I$, $j \in J$.
    \item $K$: Maximum number of projects a consultant can be assigned.
\end{itemize}

\subsection*{Decision Variables}
\begin{align*}
    x_{i,j} &= 
    \begin{cases} 
    1, & \text{if project $i$ is assigned to consultant $j$} \\ 
    0, & \text{otherwise}
    \end{cases} \quad \forall i \in I, \forall j \in J \\
    y_j &= 
    \begin{cases} 
    1, & \text{if consultant $j$ is hired} \\ 
    0, & \text{otherwise}
    \end{cases} \quad \forall j \in J
\end{align*}

\subsection*{Objective Function}
Minimize the total cost:
\[
\text{Minimize} \quad \sum_{j \in J} f_j y_j + \sum_{i \in I} \sum_{j \in J} c_{i,j} x_{i,j}
\]

\subsection*{Constraints}
\begin{align}
    &\sum_{j \in J} x_{i,j} = 1, &\forall i \in I \quad &\text{(Each project is assigned to one consultant)} \\
    &\sum_{i \in I} x_{i,j} \leq K y_j, &\forall j \in J \quad &\text{(Each consultant is assigned up to $K$ projects)} \\
    &x_{i,j} \leq y_j, &\forall i \in I, \forall j \in J \quad &\text{(Projects assigned only if consultant is hired)} \\
    &x_{i,j}, y_j \in \{0, 1\}, &\forall i \in I, \forall j \in J &\text{(Binary decision variables)}
\end{align}

\end{document}</MATH_MODEL>
<DATA>
{'fixed_costs': [100, 150, 135], 'additional_costs': [[10, 12, 20], [10, 8, 12], [15, 8, 20], [10, 6, 15], [8, 10, 15]], 'max_projects_per_consultant': 3}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the JSON
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

#### Sets
I = range(len(data['additional_costs']))  #### Set of projects
J = range(len(data['fixed_costs']))       #### Set of consultants

#### Parameters
f_j = data['fixed_costs']
c_ij = data['additional_costs']
K = data['max_projects_per_consultant']

#### Problem
problem = pulp.LpProblem("Consultant_Assignment_Problem", pulp.LpMinimize)

#### Decision Variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in I for j in J), cat='Binary')
y = pulp.LpVariable.dicts("y", (j for j in J), cat='Binary')

#### Objective Function
problem += pulp.lpSum(f_j[j] * y[j] for j in J) + pulp.lpSum(c_ij[i][j] * x[i, j] for i in I for j in J)

#### Constraints
#### Each project is assigned to exactly one consultant
for i in I:
    problem += pulp.lpSum(x[i, j] for j in J) == 1, f"One_Consultant_Per_Project_{i}"

#### Each consultant is assigned up to K projects
for j in J:
    problem += pulp.lpSum(x[i, j] for i in I) <= K * y[j], f"Max_Projects_Per_Consultant_{j}"

#### Projects assigned only if consultant is hired
for i in I:
    for j in J:
        problem += x[i, j] <= y[j], f"Assign_Project_Only_If_Hired_{i}_{j}"

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

