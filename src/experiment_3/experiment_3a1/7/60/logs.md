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

\section*{Mathematical Model for the Consultant Assignment Problem}

\textbf{Sets:}
\begin{itemize}
    \item $I$: Set of projects, indexed by $i = 1, \ldots, I$
    \item $J$: Set of consultants, indexed by $j = 1, \ldots, J$
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item $f_j$: Fixed cost for hiring consultant $j$, for $j \in J$
    \item $c_{i,j}$: Additional cost of assigning project $i$ to consultant $j$, for $i \in I$, $j \in J$
    \item $K$: Maximum number of projects that can be assigned to a consultant
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $x_{i,j}$: Binary variable, where $x_{i,j} = 1$ if project $i$ is assigned to consultant $j$, and $0$ otherwise
    \item $y_j$: Binary variable, where $y_j = 1$ if consultant $j$ is hired, and $0$ otherwise
\end{itemize}

\textbf{Objective Function:}
\[
\text{Minimize } Z = \sum_{j=1}^J f_j y_j + \sum_{i=1}^I \sum_{j=1}^J c_{i,j} x_{i,j}
\]

\textbf{Constraints:}
1. Each project must be assigned to exactly one consultant:
\[
\sum_{j=1}^J x_{i,j} = 1, \quad \forall i \in I
\]
2. A consultant can only take projects if they are hired:
\[
x_{i,j} \leq y_j, \quad \forall i \in I, \quad \forall j \in J
\]
3. A consultant can take at most $K$ projects:
\[
\sum_{i=1}^I x_{i,j} \leq K y_j, \quad \forall j \in J
\]
4. Binary constraints for decision variables:
\[
x_{i,j} \in \{0, 1\}, \quad \forall i \in I, \forall j \in J
\]
\[
y_j \in \{0, 1\}, \quad \forall j \in J
\]

\textbf{Output:}
The assignment of projects to consultants and the total cost will be represented as:
\[
\text{Output} = \{ \text{"assignments"}: [x_{j,i}] \text{ for } j \in J, i \in I, \text{"total\_cost"}: Z \}
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

\section*{Mathematical Model for the Consultant Assignment Problem}

\textbf{Sets:}
\begin{itemize}
    \item $I$: Set of projects, indexed by $i = 1, \ldots, I$
    \item $J$: Set of consultants, indexed by $j = 1, \ldots, J$
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item $f_j$: Fixed cost for hiring consultant $j$, for $j \in J$
    \item $c_{i,j}$: Additional cost of assigning project $i$ to consultant $j$, for $i \in I$, $j \in J$
    \item $K$: Maximum number of projects that can be assigned to a consultant
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $x_{i,j}$: Binary variable, where $x_{i,j} = 1$ if project $i$ is assigned to consultant $j$, and $0$ otherwise
    \item $y_j$: Binary variable, where $y_j = 1$ if consultant $j$ is hired, and $0$ otherwise
\end{itemize}

\textbf{Objective Function:}
\[
\text{Minimize } Z = \sum_{j=1}^J f_j y_j + \sum_{i=1}^I \sum_{j=1}^J c_{i,j} x_{i,j}
\]

\textbf{Constraints:}
1. Each project must be assigned to exactly one consultant:
\[
\sum_{j=1}^J x_{i,j} = 1, \quad \forall i \in I
\]
2. A consultant can only take projects if they are hired:
\[
x_{i,j} \leq y_j, \quad \forall i \in I, \quad \forall j \in J
\]
3. A consultant can take at most $K$ projects:
\[
\sum_{i=1}^I x_{i,j} \leq K y_j, \quad \forall j \in J
\]
4. Binary constraints for decision variables:
\[
x_{i,j} \in \{0, 1\}, \quad \forall i \in I, \forall j \in J
\]
\[
y_j \in \{0, 1\}, \quad \forall j \in J
\]

\textbf{Output:}
The assignment of projects to consultants and the total cost will be represented as:
\[
\text{Output} = \{ \text{"assignments"}: [x_{j,i}] \text{ for } j \in J, i \in I, \text{"total\_cost"}: Z \}
\]

\end{document}</MATH_MODEL>
<DATA>
{'fixed_costs': [100, 150, 135], 'additional_costs': [[10, 12, 20], [10, 8, 12], [15, 8, 20], [10, 6, 15], [8, 10, 15]], 'max_projects_per_consultant': 3}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data from JSON input
data = json.loads("{'fixed_costs': [100, 150, 135], 'additional_costs': [[10, 12, 20], [10, 8, 12], [15, 8, 20], [10, 6, 15], [8, 10, 15]], 'max_projects_per_consultant': 3}")
fixed_costs = data['fixed_costs']
additional_costs = data['additional_costs']
K = data['max_projects_per_consultant']

#### Sets
I = len(additional_costs)  #### Number of projects
J = len(fixed_costs)       #### Number of consultants

#### Create the problem
problem = pulp.LpProblem("ConsultantAssignmentProblem", pulp.LpMinimize)

#### Decision Variables
x = pulp.LpVariable.dicts('x', (range(I), range(J)), cat='Binary')  #### x[i][j] = 1 if project i is assigned to consultant j
y = pulp.LpVariable.dicts('y', range(J), cat='Binary')              #### y[j] = 1 if consultant j is hired

#### Objective Function
problem += (pulp.lpSum(fixed_costs[j] * y[j] for j in range(J)) +
             pulp.lpSum(additional_costs[i][j] * x[i][j] for i in range(I) for j in range(J))), "Total_Cost"

#### Constraints
#### 1. Each project must be assigned to exactly one consultant
for i in range(I):
    problem += pulp.lpSum(x[i][j] for j in range(J)) == 1, f"Project_Assignment_{i}"

#### 2. A consultant can only take projects if they are hired
for i in range(I):
    for j in range(J):
        problem += x[i][j] <= y[j], f"Consultant_Hired_{i}_{j}"

#### 3. A consultant can take at most K projects
for j in range(J):
    problem += pulp.lpSum(x[i][j] for i in range(I)) <= K * y[j], f"Max_Projects_Consultant_{j}"

#### Solve the problem
problem.solve()

#### Output results
assignments = [[int(x[i][j].varValue) for i in range(I)] for j in range(J)]
total_cost = pulp.value(problem.objective)

output = {
    "assignments": assignments,
    "total_cost": total_cost
}

print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')
```

