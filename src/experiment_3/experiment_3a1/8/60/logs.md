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

\section*{Mathematical Model for Project Assignment}

\subsection*{Sets}
\begin{itemize}
    \item $I$: Set of projects, indexed by $i \in \{1, 2, \ldots, I\}$
    \item $J$: Set of consultants, indexed by $j \in \{1, 2, \ldots, J\}$
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item $f_j$: Fixed cost of hiring consultant $j$
    \item $c_{i,j}$: Additional cost of assigning project $i$ to consultant $j$
    \item $K$: Maximum number of projects that can be assigned to each consultant
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $x_{j}$: Binary variable, $x_{j} = 1$ if consultant $j$ is hired, $0$ otherwise.
    \item $y_{i,j}$: Binary variable, $y_{i,j} = 1$ if project $i$ is assigned to consultant $j$, $0$ otherwise.
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost:

\[
\text{Minimize} \quad Z = \sum_{j=1}^{J} f_j x_j + \sum_{i=1}^{I} \sum_{j=1}^{J} c_{i,j} y_{i,j}
\]

\subsection*{Constraints}
\begin{enumerate}
    \item Each project must be assigned to exactly one consultant:
    \[
    \sum_{j=1}^{J} y_{i,j} = 1 \quad \forall i \in \{1, \ldots, I\}
    \]
    
    \item A consultant can only work on a project if they are hired:
    \[
    y_{i,j} \leq x_j \quad \forall i \in \{1, \ldots, I\}, j \in \{1, \ldots, J\}
    \]
    
    \item Maximum projects assigned to each consultant:
    \[
    \sum_{i=1}^{I} y_{i,j} \leq K x_j \quad \forall j \in \{1, \ldots, J\}
    \]
    
    \item Binary constraints:
    \[
    x_j \in \{0, 1\} \quad \forall j \in \{1, \ldots, J\}
    \]
    \[
    y_{i,j} \in \{0, 1\} \quad \forall i \in \{1, \ldots, I\}, j \in \{1, \ldots, J\}
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

\section*{Mathematical Model for Project Assignment}

\subsection*{Sets}
\begin{itemize}
    \item $I$: Set of projects, indexed by $i \in \{1, 2, \ldots, I\}$
    \item $J$: Set of consultants, indexed by $j \in \{1, 2, \ldots, J\}$
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item $f_j$: Fixed cost of hiring consultant $j$
    \item $c_{i,j}$: Additional cost of assigning project $i$ to consultant $j$
    \item $K$: Maximum number of projects that can be assigned to each consultant
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $x_{j}$: Binary variable, $x_{j} = 1$ if consultant $j$ is hired, $0$ otherwise.
    \item $y_{i,j}$: Binary variable, $y_{i,j} = 1$ if project $i$ is assigned to consultant $j$, $0$ otherwise.
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost:

\[
\text{Minimize} \quad Z = \sum_{j=1}^{J} f_j x_j + \sum_{i=1}^{I} \sum_{j=1}^{J} c_{i,j} y_{i,j}
\]

\subsection*{Constraints}
\begin{enumerate}
    \item Each project must be assigned to exactly one consultant:
    \[
    \sum_{j=1}^{J} y_{i,j} = 1 \quad \forall i \in \{1, \ldots, I\}
    \]
    
    \item A consultant can only work on a project if they are hired:
    \[
    y_{i,j} \leq x_j \quad \forall i \in \{1, \ldots, I\}, j \in \{1, \ldots, J\}
    \]
    
    \item Maximum projects assigned to each consultant:
    \[
    \sum_{i=1}^{I} y_{i,j} \leq K x_j \quad \forall j \in \{1, \ldots, J\}
    \]
    
    \item Binary constraints:
    \[
    x_j \in \{0, 1\} \quad \forall j \in \{1, \ldots, J\}
    \]
    \[
    y_{i,j} \in \{0, 1\} \quad \forall i \in \{1, \ldots, I\}, j \in \{1, \ldots, J\}
    \]
\end{enumerate}

\end{document}</MATH_MODEL>
<DATA>
{'fixed_costs': [100, 150, 135], 'additional_costs': [[10, 12, 20], [10, 8, 12], [15, 8, 20], [10, 6, 15], [8, 10, 15]], 'max_projects_per_consultant': 3}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

data = json.loads('{"fixed_costs": [100, 150, 135], "additional_costs": [[10, 12, 20], [10, 8, 12], [15, 8, 20], [10, 6, 15], [8, 10, 15]], "max_projects_per_consultant": 3}')

#### Extracting data
fixed_costs = data['fixed_costs']
additional_costs = data['additional_costs']
max_projects_per_consultant = data['max_projects_per_consultant']

I = len(additional_costs)      #### Number of projects
J = len(fixed_costs)           #### Number of consultants

#### Create the problem
problem = pulp.LpProblem("Project_Assignment", pulp.LpMinimize)

#### Decision Variables
x = pulp.LpVariable.dicts("x", range(J), cat='Binary')  #### Hiring decision for consultants
y = pulp.LpVariable.dicts("y", (range(I), range(J)), cat='Binary')  #### Assignment of projects

#### Objective Function
problem += pulp.lpSum(fixed_costs[j] * x[j] for j in range(J)) + pulp.lpSum(additional_costs[i][j] * y[i][j] for i in range(I) for j in range(J)), "Total Cost"

#### Constraints
#### Each project must be assigned to exactly one consultant
for i in range(I):
    problem += pulp.lpSum(y[i][j] for j in range(J)) == 1, f"Assign_Project_{i}"

#### A consultant can only work on a project if they are hired
for i in range(I):
    for j in range(J):
        problem += y[i][j] <= x[j], f"Consultant_Hired_{i}_{j}"

#### Maximum projects assigned to each consultant
for j in range(J):
    problem += pulp.lpSum(y[i][j] for i in range(I)) <= max_projects_per_consultant * x[j], f"Max_Projects_Consultant_{j}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

