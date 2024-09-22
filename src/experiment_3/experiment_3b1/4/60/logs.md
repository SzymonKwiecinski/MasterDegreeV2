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

\section*{Mixed Integer Linear Programming Model}

\subsection*{Sets}
\begin{itemize}
    \item \( I \): Set of projects, indexed by \( i \).
    \item \( J \): Set of consultants, indexed by \( j \).
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( f_j \): Fixed cost of hiring consultant \( j \).
    \item \( c_{i,j} \): Additional cost of assigning project \( i \) to consultant \( j \).
    \item \( K \): Maximum number of projects that can be assigned to a single consultant.
\end{itemize}

\subsection*{Variables}
\begin{itemize}
    \item \( x_j \): Binary variable that equals 1 if consultant \( j \) is hired, 0 otherwise.
    \item \( y_{i,j} \): Binary variable that equals 1 if project \( i \) is assigned to consultant \( j \), 0 otherwise.
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost:
\[
\text{Minimize } Z = \sum_{j=1}^{J} f_j x_j + \sum_{i=1}^{I} \sum_{j=1}^{J} c_{i,j} y_{i,j}
\]

\subsection*{Constraints}
1. Each project must be assigned to exactly one consultant:
\[
\sum_{j=1}^{J} y_{i,j} = 1 \quad \forall i \in I
\]
  
2. A consultant can only take on projects if they are hired:
\[
y_{i,j} \leq x_j \quad \forall i \in I, \forall j \in J
\]

3. A consultant can handle at most \( K \) projects:
\[
\sum_{i=1}^{I} y_{i,j} \leq K \cdot x_j \quad \forall j \in J
\]

4. Binary constraints:
\[
x_j \in \{0, 1\} \quad \forall j \in J
\]
\[
y_{i,j} \in \{0, 1\} \quad \forall i \in I, \forall j \in J
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

\section*{Mixed Integer Linear Programming Model}

\subsection*{Sets}
\begin{itemize}
    \item \( I \): Set of projects, indexed by \( i \).
    \item \( J \): Set of consultants, indexed by \( j \).
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( f_j \): Fixed cost of hiring consultant \( j \).
    \item \( c_{i,j} \): Additional cost of assigning project \( i \) to consultant \( j \).
    \item \( K \): Maximum number of projects that can be assigned to a single consultant.
\end{itemize}

\subsection*{Variables}
\begin{itemize}
    \item \( x_j \): Binary variable that equals 1 if consultant \( j \) is hired, 0 otherwise.
    \item \( y_{i,j} \): Binary variable that equals 1 if project \( i \) is assigned to consultant \( j \), 0 otherwise.
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost:
\[
\text{Minimize } Z = \sum_{j=1}^{J} f_j x_j + \sum_{i=1}^{I} \sum_{j=1}^{J} c_{i,j} y_{i,j}
\]

\subsection*{Constraints}
1. Each project must be assigned to exactly one consultant:
\[
\sum_{j=1}^{J} y_{i,j} = 1 \quad \forall i \in I
\]
  
2. A consultant can only take on projects if they are hired:
\[
y_{i,j} \leq x_j \quad \forall i \in I, \forall j \in J
\]

3. A consultant can handle at most \( K \) projects:
\[
\sum_{i=1}^{I} y_{i,j} \leq K \cdot x_j \quad \forall j \in J
\]

4. Binary constraints:
\[
x_j \in \{0, 1\} \quad \forall j \in J
\]
\[
y_{i,j} \in \{0, 1\} \quad \forall i \in I, \forall j \in J
\]

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
    'additional_costs': [[10, 12, 20], [10, 8, 12], [15, 8, 20], [10, 6, 15], [8, 10, 15]],
    'max_projects_per_consultant': 3
}

#### Sets
I = range(len(data['additional_costs']))  #### Projects
J = range(len(data['fixed_costs']))        #### Consultants

#### Parameters
f = data['fixed_costs']                         #### Fixed costs
c = data['additional_costs']                     #### Additional costs
K = data['max_projects_per_consultant']         #### Max projects per consultant

#### Problem definition
problem = pulp.LpProblem("Consultant_Assignment", pulp.LpMinimize)

#### Variables
x = pulp.LpVariable.dicts("hire", J, cat='Binary')  #### Hiring consultants
y = pulp.LpVariable.dicts("assign", (I, J), cat='Binary')  #### Project assignment

#### Objective function
problem += pulp.lpSum(f[j] * x[j] for j in J) + pulp.lpSum(c[i][j] * y[i][j] for i in I for j in J)

#### Constraints
#### Each project must be assigned to exactly one consultant
for i in I:
    problem += pulp.lpSum(y[i][j] for j in J) == 1

#### A consultant can only take on projects if they are hired
for i in I:
    for j in J:
        problem += y[i][j] <= x[j]

#### A consultant can handle at most K projects
for j in J:
    problem += pulp.lpSum(y[i][j] for i in I) <= K * x[j]

#### Solve the problem
problem.solve()

#### Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

