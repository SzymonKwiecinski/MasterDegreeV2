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
To solve this problem, we need to create a mathematical model using Mixed Integer Linear Programming (MILP). We will define decision variables, the objective function, and constraints based on the problem description provided. Here is the mathematical model in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\section*{Mathematical Model}

\textbf{Sets and Indices:}
\begin{itemize}
    \item \(I\): Set of projects, indexed by \(i\).
    \item \(J\): Set of consultants, indexed by \(j\).
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item \(f_j\): Fixed cost of hiring consultant \(j\).
    \item \(c_{i,j}\): Additional cost of assigning project \(i\) to consultant \(j\).
    \item \(K\): Maximum number of projects that each consultant \(j\) can be assigned.
\end{itemize}

\textbf{Decision Variables:}
\begin{align*}
    & y_j = 
    \begin{cases} 
    1, & \text{if consultant } j \text{ is hired} \\
    0, & \text{otherwise}
    \end{cases} \\
    & x_{i,j} = 
    \begin{cases} 
    1, & \text{if project } i \text{ is assigned to consultant } j \\
    0, & \text{otherwise}
    \end{cases} 
\end{align*}

\textbf{Objective:}

Minimize the total cost:
\[
\min \sum_{j \in J} f_j y_j + \sum_{i \in I} \sum_{j \in J} c_{i,j} x_{i,j}
\]

\textbf{Constraints:}
\begin{align*}
    & \text{Each project is assigned to exactly one consultant:} \\
    & \sum_{j \in J} x_{i,j} = 1, \quad \forall i \in I \\
    & \text{A project can only be assigned to a hired consultant:} \\
    & x_{i,j} \leq y_j, \quad \forall i \in I, \forall j \in J \\
    & \text{Limit the number of projects per consultant:} \\
    & \sum_{i \in I} x_{i,j} \leq K y_j, \quad \forall j \in J \\
    & \text{Binary constraints:} \\
    & x_{i,j} \in \{0, 1\}, \quad \forall i \in I, \forall j \in J \\
    & y_j \in \{0, 1\}, \quad \forall j \in J
\end{align*}

\end{document}
```

This model represents a MILP problem where:

- The objective is to minimize the total cost of hiring consultants and assigning projects by considering both fixed and additional costs.
- Each project is exactly assigned to one consultant.
- A project can only be assigned if the consultant is hired.
- Each consultant can handle up to a specified number \( K \) of projects.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\section*{Mathematical Model}

\textbf{Sets and Indices:}
\begin{itemize}
    \item \(I\): Set of projects, indexed by \(i\).
    \item \(J\): Set of consultants, indexed by \(j\).
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item \(f_j\): Fixed cost of hiring consultant \(j\).
    \item \(c_{i,j}\): Additional cost of assigning project \(i\) to consultant \(j\).
    \item \(K\): Maximum number of projects that each consultant \(j\) can be assigned.
\end{itemize}

\textbf{Decision Variables:}
\begin{align*}
    & y_j = 
    \begin{cases} 
    1, & \text{if consultant } j \text{ is hired} \\
    0, & \text{otherwise}
    \end{cases} \\
    & x_{i,j} = 
    \begin{cases} 
    1, & \text{if project } i \text{ is assigned to consultant } j \\
    0, & \text{otherwise}
    \end{cases} 
\end{align*}

\textbf{Objective:}

Minimize the total cost:
\[
\min \sum_{j \in J} f_j y_j + \sum_{i \in I} \sum_{j \in J} c_{i,j} x_{i,j}
\]

\textbf{Constraints:}
\begin{align*}
    & \text{Each project is assigned to exactly one consultant:} \\
    & \sum_{j \in J} x_{i,j} = 1, \quad \forall i \in I \\
    & \text{A project can only be assigned to a hired consultant:} \\
    & x_{i,j} \leq y_j, \quad \forall i \in I, \forall j \in J \\
    & \text{Limit the number of projects per consultant:} \\
    & \sum_{i \in I} x_{i,j} \leq K y_j, \quad \forall j \in J \\
    & \text{Binary constraints:} \\
    & x_{i,j} \in \{0, 1\}, \quad \forall i \in I, \forall j \in J \\
    & y_j \in \{0, 1\}, \quad \forall j \in J
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'fixed_costs': [100, 150, 135], 'additional_costs': [[10, 12, 20], [10, 8, 12], [15, 8, 20], [10, 6, 15], [8, 10, 15]], 'max_projects_per_consultant': 3}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Extract the data from JSON
data = {
    'fixed_costs': [100, 150, 135],
    'additional_costs': [[10, 12, 20], [10, 8, 12], [15, 8, 20], [10, 6, 15], [8, 10, 15]],
    'max_projects_per_consultant': 3
}

fixed_costs = data['fixed_costs']
additional_costs = data['additional_costs']
K = data['max_projects_per_consultant']

#### Indices
I = range(len(additional_costs))  #### Projects
J = range(len(fixed_costs))  #### Consultants

#### Problem
problem = pulp.LpProblem("ConsultantAssignment", pulp.LpMinimize)

#### Decision Variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in I for j in J), cat='Binary')
y = pulp.LpVariable.dicts("y", J, cat='Binary')

#### Objective function
problem += pulp.lpSum(fixed_costs[j] * y[j] for j in J) + \
           pulp.lpSum(additional_costs[i][j] * x[i, j] for i in I for j in J)

#### Constraints
#### Each project is assigned to exactly one consultant
for i in I:
    problem += pulp.lpSum(x[i, j] for j in J) == 1

#### A project can only be assigned to a hired consultant
for i in I:
    for j in J:
        problem += x[i, j] <= y[j]

#### Limit the number of projects per consultant
for j in J:
    problem += pulp.lpSum(x[i, j] for i in I) <= K * y[j]

#### Solve the problem
problem.solve()

#### Output the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

