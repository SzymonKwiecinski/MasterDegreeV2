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
To solve this mixed-integer linear programming (MILP) problem, we need to create a mathematical model that minimizes the total cost of hiring consultants and assigning them to projects while respecting the constraints. Here's how the model can be formulated:

**Decision Variables:**

- \( x_{i,j} \): A binary variable that is 1 if project \( i \) is assigned to consultant \( j \), and 0 otherwise.
- \( y_j \): A binary variable that is 1 if consultant \( j \) is hired, and 0 otherwise.

**Objective Function:**

Minimize the total cost, which includes both the fixed costs of hiring consultants and the additional costs of assigning projects:

\[ \text{Minimize} \quad \sum_{j=1}^{J} f_j y_j + \sum_{i=1}^{I} \sum_{j=1}^{J} c_{i,j} x_{i,j} \]

**Constraints:**

1. Each project is assigned to exactly one consultant:

   \[
   \sum_{j=1}^{J} x_{i,j} = 1, \quad \forall i = 1, \ldots, I
   \]

2. A consultant can be assigned up to \( K \) projects:

   \[
   \sum_{i=1}^{I} x_{i,j} \leq K y_j, \quad \forall j = 1, \ldots, J
   \]

3. A project can only be assigned to a hired consultant:

   \[
   x_{i,j} \leq y_j, \quad \forall i = 1, \ldots, I, \forall j = 1, \ldots, J
   \]

4. Binary constraints on decision variables:

   \[
   x_{i,j} \in \{0, 1\}, \quad y_j \in \{0, 1\}
   \]

Now, let's write the above model in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:}
\[
\text{Minimize} \quad \sum_{j=1}^{J} f_j y_j + \sum_{i=1}^{I} \sum_{j=1}^{J} c_{i,j} x_{i,j}
\]

\textbf{Subject to:}

\begin{align}
& \sum_{j=1}^{J} x_{i,j} = 1, && \forall i = 1, \ldots, I \\
& \sum_{i=1}^{I} x_{i,j} \leq K y_j, && \forall j = 1, \ldots, J \\
& x_{i,j} \leq y_j, && \forall i = 1, \ldots, I, \forall j = 1, \ldots, J \\
& x_{i,j} \in \{0, 1\}, \quad y_j \in \{0, 1\} && \forall i = 1, \ldots, I, \forall j = 1, \ldots, J
\end{align}

\end{document}
```

This LaTeX code represents the MILP mathematical model for the given problem. It includes the objective function to minimize total costs and the constraints that ensure each project is assigned correctly, no consultant is overloaded, and consultants are only paid if they are assigned projects.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:}
\[
\text{Minimize} \quad \sum_{j=1}^{J} f_j y_j + \sum_{i=1}^{I} \sum_{j=1}^{J} c_{i,j} x_{i,j}
\]

\textbf{Subject to:}

\begin{align}
& \sum_{j=1}^{J} x_{i,j} = 1, && \forall i = 1, \ldots, I \\
& \sum_{i=1}^{I} x_{i,j} \leq K y_j, && \forall j = 1, \ldots, J \\
& x_{i,j} \leq y_j, && \forall i = 1, \ldots, I, \forall j = 1, \ldots, J \\
& x_{i,j} \in \{0, 1\}, \quad y_j \in \{0, 1\} && \forall i = 1, \ldots, I, \forall j = 1, \ldots, J
\end{align}

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

fixed_costs = data['fixed_costs']
additional_costs = data['additional_costs']
K = data['max_projects_per_consultant']

I = len(additional_costs)
J = len(fixed_costs)

#### Define the problem
problem = pulp.LpProblem("Consultant_Assignment", pulp.LpMinimize)

#### Decision variables
x = pulp.LpVariable.dicts("assignment", (range(I), range(J)), cat='Binary')
y = pulp.LpVariable.dicts("consultant_used", range(J), cat='Binary')

#### Objective function
problem += pulp.lpSum(fixed_costs[j] * y[j] for j in range(J)) + \
           pulp.lpSum(additional_costs[i][j] * x[i][j] for i in range(I) for j in range(J))

#### Constraints
#### Each project is assigned to exactly one consultant
for i in range(I):
    problem += pulp.lpSum(x[i][j] for j in range(J)) == 1

#### Consultant capacity
for j in range(J):
    problem += pulp.lpSum(x[i][j] for i in range(I)) <= K * y[j]

#### If a project is assigned to a consultant, the consultant must be used
for i in range(I):
    for j in range(J):
        problem += x[i][j] <= y[j]

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

