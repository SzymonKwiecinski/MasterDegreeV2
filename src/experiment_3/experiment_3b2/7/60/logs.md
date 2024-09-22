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
To solve this problem, we will define a Mixed Integer Linear Programming (MILP) model. The goal is to minimize the total cost associated with hiring consultants and assigning them to projects, subject to the constraints outlined in the problem description.

Let's create a mathematical model for the problem:

######### Decision Variables:
- \( x_{i,j} \): Binary variable, equals 1 if project \( i \) is assigned to consultant \( j \), 0 otherwise.
- \( y_j \): Binary variable, equals 1 if consultant \( j \) is hired, 0 otherwise.

######### Model Formulation:
Objective Function: Minimize the total cost, which includes the fixed hiring cost for consultants and the additional cost for assigning projects to consultants.

\[
\text{Minimize } Z = \sum_{j=1}^{J} f_j y_j + \sum_{i=1}^{I} \sum_{j=1}^{J} c_{i,j} x_{i,j}
\]

Subject to:

1. Each project is assigned to exactly one consultant:
   \[
   \sum_{j=1}^{J} x_{i,j} = 1, \quad \forall i = 1, \ldots, I
   \]

2. A consultant can be assigned at most \( K \) projects:
   \[
   \sum_{i=1}^{I} x_{i,j} \leq K \cdot y_j, \quad \forall j = 1, \ldots, J
   \]

3. If a project \( i \) is assigned to a consultant \( j \), then consultant \( j \) must be hired:
   \[
   x_{i,j} \leq y_j, \quad \forall i = 1, \ldots, I, \quad \forall j = 1, \ldots, J
   \]

4. Binary constraints for decision variables:
   \[
   x_{i,j} \in \{0, 1\}, \quad \forall i = 1, \ldots, I, \quad j = 1, \ldots, J
   \]
   \[
   y_j \in \{0, 1\}, \quad \forall j = 1, \ldots, J
   \]

Let's write this model using LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective Function:}
\[
\text{Minimize } Z = \sum_{j=1}^{J} f_j y_j + \sum_{i=1}^{I} \sum_{j=1}^{J} c_{i,j} x_{i,j}
\]

\textbf{Subject to:}

1. Each project is assigned to exactly one consultant:
\[
\sum_{j=1}^{J} x_{i,j} = 1, \quad \forall i = 1, \ldots, I
\]

2. A consultant can be assigned at most \( K \) projects:
\[
\sum_{i=1}^{I} x_{i,j} \leq K \cdot y_j, \quad \forall j = 1, \ldots, J
\]

3. If a project \( i \) is assigned to a consultant \( j \), then consultant \( j \) must be hired:
\[
x_{i,j} \leq y_j, \quad \forall i = 1, \ldots, I, \quad \forall j = 1, \ldots, J
\]

4. Binary constraints for decision variables:
\[
x_{i,j} \in \{0, 1\}, \quad \forall i = 1, \ldots, I, \quad j = 1, \ldots, J
\]
\[
y_j \in \{0, 1\}, \quad \forall j = 1, \ldots, J
\]

\end{document}
```

This model will solve the problem by finding the optimal assignment of projects to consultants while minimizing the total cost.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective Function:}
\[
\text{Minimize } Z = \sum_{j=1}^{J} f_j y_j + \sum_{i=1}^{I} \sum_{j=1}^{J} c_{i,j} x_{i,j}
\]

\textbf{Subject to:}

1. Each project is assigned to exactly one consultant:
\[
\sum_{j=1}^{J} x_{i,j} = 1, \quad \forall i = 1, \ldots, I
\]

2. A consultant can be assigned at most \( K \) projects:
\[
\sum_{i=1}^{I} x_{i,j} \leq K \cdot y_j, \quad \forall j = 1, \ldots, J
\]

3. If a project \( i \) is assigned to a consultant \( j \), then consultant \( j \) must be hired:
\[
x_{i,j} \leq y_j, \quad \forall i = 1, \ldots, I, \quad \forall j = 1, \ldots, J
\]

4. Binary constraints for decision variables:
\[
x_{i,j} \in \{0, 1\}, \quad \forall i = 1, \ldots, I, \quad j = 1, \ldots, J
\]
\[
y_j \in \{0, 1\}, \quad \forall j = 1, \ldots, J
\]

\end{document}</MATH_MODEL>
<DATA>
{'fixed_costs': [100, 150, 135], 'additional_costs': [[10, 12, 20], [10, 8, 12], [15, 8, 20], [10, 6, 15], [8, 10, 15]], 'max_projects_per_consultant': 3}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON format
data = {
    'fixed_costs': [100, 150, 135],
    'additional_costs': [[10, 12, 20], [10, 8, 12], [15, 8, 20], [10, 6, 15], [8, 10, 15]],
    'max_projects_per_consultant': 3
}

#### Number of projects and consultants
I = len(data['additional_costs'])
J = len(data['fixed_costs'])
K = data['max_projects_per_consultant']

#### Create the problem
problem = pulp.LpProblem("Consultant_Assignment_Problem", pulp.LpMinimize)

#### Decision variables
x = pulp.LpVariable.dicts("x", (range(I), range(J)), cat='Binary')  #### Project i assigned to Consultant j
y = pulp.LpVariable.dicts("y", range(J), cat='Binary')  #### Consultant j hired

#### Objective Function
fixed_costs = data['fixed_costs']
additional_costs = data['additional_costs']
problem += pulp.lpSum(fixed_costs[j] * y[j] for j in range(J)) + \
           pulp.lpSum(additional_costs[i][j] * x[i][j] for i in range(I) for j in range(J)), "Total_Cost"

#### Constraints

#### Each project is assigned to exactly one consultant
for i in range(I):
    problem += pulp.lpSum(x[i][j] for j in range(J)) == 1, f"One_consultant_per_project_{i}"

#### A consultant can be assigned at most K projects
for j in range(J):
    problem += pulp.lpSum(x[i][j] for i in range(I)) <= K * y[j], f"Max_projects_per_consultant_{j}"

#### If a project is assigned to a consultant, then consultant must be hired
for i in range(I):
    for j in range(J):
        problem += x[i][j] <= y[j], f"Hire_consultant_if_assigned_{i}_{j}"

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

