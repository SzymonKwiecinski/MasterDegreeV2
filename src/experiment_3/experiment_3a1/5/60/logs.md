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

\subsection*{Parameters}
\begin{itemize}
    \item Let \( I \) be the number of projects.
    \item Let \( J \) be the number of consultants.
    \item Let \( K \) be the maximum number of projects that can be assigned to a single consultant.
    \item Let \( f_j \) be the fixed cost incurred by hiring consultant \( j \).
    \item Let \( c_{i,j} \) be the additional cost incurred by assigning project \( i \) to consultant \( j \).
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item Let \( x_{j} \) be a binary variable that indicates whether consultant \( j \) is hired (\( x_{j} = 1 \)) or not (\( x_{j} = 0 \)).
    \item Let \( assignment_{j,i} \) be a binary variable that indicates whether project \( i \) is assigned to consultant \( j \) (\( assignment_{j,i} = 1 \)) or not (\( assignment_{j,i} = 0 \)).
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost:
\[
\text{Minimize } Z = \sum_{j=1}^{J} f_j x_j + \sum_{i=1}^{I} \sum_{j=1}^{J} c_{i,j} assignment_{j,i}
\]

\subsection*{Constraints}
1. Each project must be assigned to exactly one consultant:
\[
\sum_{j=1}^{J} assignment_{j,i} = 1 \quad \forall i = 1, \ldots, I
\]
2. Each consultant can be assigned up to \( K \) projects:
\[
\sum_{i=1}^{I} assignment_{j,i} \leq K x_j \quad \forall j = 1, \ldots, J
\]
3. Relationship between assignment and hiring:
\[
assignment_{j,i} \leq x_j \quad \forall i = 1, \ldots, I, \forall j = 1, \ldots, J
\]
4. Binary constraints:
\[
x_j \in \{0, 1\} \quad \forall j = 1, \ldots, J
\]
\[
assignment_{j,i} \in \{0, 1\} \quad \forall i = 1, \ldots, I, \forall j = 1, \ldots, J
\]

\subsection*{Output}
The output should include:
\begin{itemize}
    \item The assignments of projects to consultants \( assignment_{j,i} \).
    \item The total cost \( Z \).
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

\section*{Mathematical Model for the Consultant Assignment Problem}

\subsection*{Parameters}
\begin{itemize}
    \item Let \( I \) be the number of projects.
    \item Let \( J \) be the number of consultants.
    \item Let \( K \) be the maximum number of projects that can be assigned to a single consultant.
    \item Let \( f_j \) be the fixed cost incurred by hiring consultant \( j \).
    \item Let \( c_{i,j} \) be the additional cost incurred by assigning project \( i \) to consultant \( j \).
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item Let \( x_{j} \) be a binary variable that indicates whether consultant \( j \) is hired (\( x_{j} = 1 \)) or not (\( x_{j} = 0 \)).
    \item Let \( assignment_{j,i} \) be a binary variable that indicates whether project \( i \) is assigned to consultant \( j \) (\( assignment_{j,i} = 1 \)) or not (\( assignment_{j,i} = 0 \)).
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost:
\[
\text{Minimize } Z = \sum_{j=1}^{J} f_j x_j + \sum_{i=1}^{I} \sum_{j=1}^{J} c_{i,j} assignment_{j,i}
\]

\subsection*{Constraints}
1. Each project must be assigned to exactly one consultant:
\[
\sum_{j=1}^{J} assignment_{j,i} = 1 \quad \forall i = 1, \ldots, I
\]
2. Each consultant can be assigned up to \( K \) projects:
\[
\sum_{i=1}^{I} assignment_{j,i} \leq K x_j \quad \forall j = 1, \ldots, J
\]
3. Relationship between assignment and hiring:
\[
assignment_{j,i} \leq x_j \quad \forall i = 1, \ldots, I, \forall j = 1, \ldots, J
\]
4. Binary constraints:
\[
x_j \in \{0, 1\} \quad \forall j = 1, \ldots, J
\]
\[
assignment_{j,i} \in \{0, 1\} \quad \forall i = 1, \ldots, I, \forall j = 1, \ldots, J
\]

\subsection*{Output}
The output should include:
\begin{itemize}
    \item The assignments of projects to consultants \( assignment_{j,i} \).
    \item The total cost \( Z \).
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'fixed_costs': [100, 150, 135], 'additional_costs': [[10, 12, 20], [10, 8, 12], [15, 8, 20], [10, 6, 15], [8, 10, 15]], 'max_projects_per_consultant': 3}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data from the provided JSON format
data = json.loads("{'fixed_costs': [100, 150, 135], 'additional_costs': [[10, 12, 20], [10, 8, 12], [15, 8, 20], [10, 6, 15], [8, 10, 15]], 'max_projects_per_consultant': 3}")

#### Parameters
fixed_costs = data['fixed_costs']
additional_costs = data['additional_costs']
K = data['max_projects_per_consultant']

I = len(additional_costs)  #### number of projects
J = len(fixed_costs)       #### number of consultants

#### Create the problem
problem = pulp.LpProblem("Consultant_Assignment_Problem", pulp.LpMinimize)

#### Decision Variables
x = pulp.LpVariable.dicts("x", range(J), cat='Binary')  #### consultant hired
assignment = pulp.LpVariable.dicts("assignment", (range(J), range(I)), cat='Binary')  #### assignments

#### Objective Function
problem += pulp.lpSum(fixed_costs[j] * x[j] for j in range(J)) + pulp.lpSum(additional_costs[i][j] * assignment[j][i] for i in range(I) for j in range(J)), "Total_Cost"

#### Constraints
#### Each project must be assigned to exactly one consultant
for i in range(I):
    problem += pulp.lpSum(assignment[j][i] for j in range(J)) == 1, f"Project_Assignment_{i}"

#### Each consultant can be assigned up to K projects
for j in range(J):
    problem += pulp.lpSum(assignment[j][i] for i in range(I)) <= K * x[j], f"Consultant_Capacity_{j}"

#### Relationship between assignment and hiring
for i in range(I):
    for j in range(J):
        problem += assignment[j][i] <= x[j], f"Assignment_Hiring_{j}_{i}"

#### Solve the problem
problem.solve()

#### Output the assignments and objective value
assignments = [[pulp.value(assignment[j][i]) for i in range(I)] for j in range(J)]
total_cost = pulp.value(problem.objective)

#### Print the results
print("Assignments of projects to consultants:")
for j in range(J):
    print(f'Consultant {j + 1}: ' + ', '.join(f'Project {i + 1} assigned' if pulp.value(assignment[j][i]) == 1 else f'Project {i + 1} not assigned' for i in range(I)))

print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')
```

