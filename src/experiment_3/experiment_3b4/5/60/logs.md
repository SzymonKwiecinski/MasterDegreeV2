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
To model this problem as a Mixed Integer Linear Program (MILP), we need to define the following decision variables, objective function and constraints:

######### Decision Variables
- \( y_j \): Binary variable indicating whether consultant \( j \) is hired. \( y_j = 1 \) if consultant \( j \) is hired, 0 otherwise.
- \( x_{i,j} \): Binary variable indicating whether project \( i \) is assigned to consultant \( j \). \( x_{i,j} = 1 \) if project \( i \) is assigned to consultant \( j \), 0 otherwise.

######### Objective Function
Minimize the total cost of hiring consultants and assigning projects:

\[
\text{Minimize} \quad \sum_{j=1}^{J} f_j y_j + \sum_{i=1}^{I} \sum_{j=1}^{J} c_{i,j} x_{i,j}
\]

######### Constraints
1. **Each project is assigned to exactly one consultant:**

   \[
   \sum_{j=1}^{J} x_{i,j} = 1 \quad \forall i = 1, \ldots, I
   \]

2. **A consultant can be assigned up to \( K \) projects:**

   \[
   \sum_{i=1}^{I} x_{i,j} \leq K y_j \quad \forall j = 1, \ldots, J
   \]

3. **\( x_{i,j} \) and \( y_j \) are binary variables:**

   \[
   x_{i,j} \in \{0, 1\}, \quad y_j \in \{0, 1\} \quad \forall i = 1, \ldots, I, \, j = 1, \ldots, J
   \]

Now, let's write this in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Mathematical Model:}

\textbf{Indices:}
\begin{align*}
i & = \text{project index, } i = 1, \ldots, I \\
j & = \text{consultant index, } j = 1, \ldots, J
\end{align*}

\textbf{Parameters:}
\begin{align*}
f_j & = \text{fixed cost of hiring consultant } j \\
c_{i,j} & = \text{cost of assigning project } i \text{ to consultant } j \\
K & = \text{maximum number of projects a consultant can handle}
\end{align*}

\textbf{Decision Variables:}
\begin{align*}
y_j & = 
\begin{cases} 
1, & \text{if consultant } j \text{ is hired} \\
0, & \text{otherwise}
\end{cases} \\
x_{i,j} & = 
\begin{cases} 
1, & \text{if project } i \text{ is assigned to consultant } j \\
0, & \text{otherwise}
\end{cases}
\end{align*}

\textbf{Objective:}
\[
\text{Minimize } \quad \sum_{j=1}^{J} f_j y_j + \sum_{i=1}^{I} \sum_{j=1}^{J} c_{i,j} x_{i,j}
\]

\textbf{Subject to:}
\begin{align*}
& \sum_{j=1}^{J} x_{i,j} = 1, \quad \forall i = 1, \ldots, I \\
& \sum_{i=1}^{I} x_{i,j} \leq K y_j, \quad \forall j = 1, \ldots, J \\
& x_{i,j} \in \{0, 1\}, \quad \forall i = 1, \ldots, I, \, j = 1, \ldots, J \\
& y_j \in \{0, 1\}, \quad \forall j = 1, \ldots, J
\end{align*}

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

\textbf{Mathematical Model:}

\textbf{Indices:}
\begin{align*}
i & = \text{project index, } i = 1, \ldots, I \\
j & = \text{consultant index, } j = 1, \ldots, J
\end{align*}

\textbf{Parameters:}
\begin{align*}
f_j & = \text{fixed cost of hiring consultant } j \\
c_{i,j} & = \text{cost of assigning project } i \text{ to consultant } j \\
K & = \text{maximum number of projects a consultant can handle}
\end{align*}

\textbf{Decision Variables:}
\begin{align*}
y_j & = 
\begin{cases} 
1, & \text{if consultant } j \text{ is hired} \\
0, & \text{otherwise}
\end{cases} \\
x_{i,j} & = 
\begin{cases} 
1, & \text{if project } i \text{ is assigned to consultant } j \\
0, & \text{otherwise}
\end{cases}
\end{align*}

\textbf{Objective:}
\[
\text{Minimize } \quad \sum_{j=1}^{J} f_j y_j + \sum_{i=1}^{I} \sum_{j=1}^{J} c_{i,j} x_{i,j}
\]

\textbf{Subject to:}
\begin{align*}
& \sum_{j=1}^{J} x_{i,j} = 1, \quad \forall i = 1, \ldots, I \\
& \sum_{i=1}^{I} x_{i,j} \leq K y_j, \quad \forall j = 1, \ldots, J \\
& x_{i,j} \in \{0, 1\}, \quad \forall i = 1, \ldots, I, \, j = 1, \ldots, J \\
& y_j \in \{0, 1\}, \quad \forall j = 1, \ldots, J
\end{align*}

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

fixed_costs = data['fixed_costs']
additional_costs = data['additional_costs']
max_projects_per_consultant = data['max_projects_per_consultant']

I = len(additional_costs)  #### Number of projects
J = len(fixed_costs)       #### Number of consultants

#### Problem
problem = pulp.LpProblem("Consultant_Assignment", pulp.LpMinimize)

#### Decision Variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(I) for j in range(J)), cat='Binary')
y = pulp.LpVariable.dicts("y", (j for j in range(J)), cat='Binary')

#### Objective Function
problem += pulp.lpSum(fixed_costs[j] * y[j] for j in range(J)) + \
           pulp.lpSum(additional_costs[i][j] * x[i, j] for i in range(I) for j in range(J))

#### Constraints
for i in range(I):
    problem += pulp.lpSum(x[i, j] for j in range(J)) == 1

for j in range(J):
    problem += pulp.lpSum(x[i, j] for i in range(I)) <= max_projects_per_consultant * y[j]

#### Solve
problem.solve()

#### Output the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

