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
    \item \( I \): Set of projects, indexed by \( i \) (where \( i = 1, 2, \ldots, I \))
    \item \( J \): Set of consultants, indexed by \( j \) (where \( j = 1, 2, \ldots, J \))
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( f_j \): Fixed cost of hiring consultant \( j \) for \( j \in J \)
    \item \( c_{i,j} \): Additional cost of assigning project \( i \) to consultant \( j \) for \( i \in I, j \in J \)
    \item \( K \): Maximum number of projects that can be assigned to each consultant
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( x_{j} \): Binary variable that indicates whether consultant \( j \) is hired (1) or not (0) for \( j \in J \)
    \item \( assignment_{j,i} \): Binary variable that indicates whether project \( i \) is assigned to consultant \( j \) (1) or not (0) for \( i \in I, j \in J \)
\end{itemize}

\subsection*{Objective Function}
The objective is to minimize the total cost, which can be expressed as:
\[
\text{Minimize } Z = \sum_{j=1}^{J} f_j \cdot x_j + \sum_{i=1}^{I} \sum_{j=1}^{J} c_{i,j} \cdot assignment_{j,i}
\]

\subsection*{Constraints}
\begin{enumerate}
    \item Each project can be assigned to at most one consultant:
    \[
    \sum_{j=1}^{J} assignment_{j,i} \leq 1, \quad \forall i \in I
    \]

    \item A consultant can be assigned to a maximum of \( K \) projects:
    \[
    \sum_{i=1}^{I} assignment_{j,i} \leq K \cdot x_j, \quad \forall j \in J
    \]

    \item A project can only be assigned to a consultant if that consultant is hired:
    \[
    assignment_{j,i} \leq x_j, \quad \forall i \in I, \forall j \in J
    \]

    \item Binary constraints on the decision variables:
    \[
    x_j \in \{0, 1\}, \quad \forall j \in J
    \]
    \[
    assignment_{j,i} \in \{0, 1\}, \quad \forall i \in I, \forall j \in J
    \]
\end{enumerate}

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
    \item \( I \): Set of projects, indexed by \( i \) (where \( i = 1, 2, \ldots, I \))
    \item \( J \): Set of consultants, indexed by \( j \) (where \( j = 1, 2, \ldots, J \))
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( f_j \): Fixed cost of hiring consultant \( j \) for \( j \in J \)
    \item \( c_{i,j} \): Additional cost of assigning project \( i \) to consultant \( j \) for \( i \in I, j \in J \)
    \item \( K \): Maximum number of projects that can be assigned to each consultant
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( x_{j} \): Binary variable that indicates whether consultant \( j \) is hired (1) or not (0) for \( j \in J \)
    \item \( assignment_{j,i} \): Binary variable that indicates whether project \( i \) is assigned to consultant \( j \) (1) or not (0) for \( i \in I, j \in J \)
\end{itemize}

\subsection*{Objective Function}
The objective is to minimize the total cost, which can be expressed as:
\[
\text{Minimize } Z = \sum_{j=1}^{J} f_j \cdot x_j + \sum_{i=1}^{I} \sum_{j=1}^{J} c_{i,j} \cdot assignment_{j,i}
\]

\subsection*{Constraints}
\begin{enumerate}
    \item Each project can be assigned to at most one consultant:
    \[
    \sum_{j=1}^{J} assignment_{j,i} \leq 1, \quad \forall i \in I
    \]

    \item A consultant can be assigned to a maximum of \( K \) projects:
    \[
    \sum_{i=1}^{I} assignment_{j,i} \leq K \cdot x_j, \quad \forall j \in J
    \]

    \item A project can only be assigned to a consultant if that consultant is hired:
    \[
    assignment_{j,i} \leq x_j, \quad \forall i \in I, \forall j \in J
    \]

    \item Binary constraints on the decision variables:
    \[
    x_j \in \{0, 1\}, \quad \forall j \in J
    \]
    \[
    assignment_{j,i} \in \{0, 1\}, \quad \forall i \in I, \forall j \in J
    \]
\end{enumerate}

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

#### Sets
I = range(len(data['additional_costs']))  #### Projects
J = range(len(data['fixed_costs']))       #### Consultants

#### Parameters
f = data['fixed_costs']
c = data['additional_costs']
K = data['max_projects_per_consultant']

#### Problem
problem = pulp.LpProblem("Consultant_Assignment", pulp.LpMinimize)

#### Decision Variables
x = pulp.LpVariable.dicts("Hire", J, cat=pulp.LpBinary)
assignment = pulp.LpVariable.dicts("Assign", ((j, i) for j in J for i in I), cat=pulp.LpBinary)

#### Objective Function
problem += pulp.lpSum(f[j] * x[j] for j in J) + pulp.lpSum(c[i][j] * assignment[j, i] for i in I for j in J)

#### Constraints
#### Each project assigned to at most one consultant
for i in I:
    problem += pulp.lpSum(assignment[j, i] for j in J) <= 1

#### Each consultant assigned to maximum K projects
for j in J:
    problem += pulp.lpSum(assignment[j, i] for i in I) <= K * x[j]

#### A project only assigned if consultant is hired
for i in I:
    for j in J:
        problem += assignment[j, i] <= x[j]

#### Solve the problem
problem.solve()

#### Output the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

