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
To address this problem, we can create a Mixed Integer Linear Programming (MILP) model. The goal is to minimize the total cost, which includes both the fixed costs of hiring consultants and the additional costs of assigning projects to them. Below is the mathematical model for this problem:

Define the decision variables:
- \( y_j \): Binary variable indicating whether consultant \( j \) is hired (1 if hired, 0 otherwise).
- \( x_{i,j} \): Binary variable indicating whether project \( i \) is assigned to consultant \( j \) (1 if assigned, 0 otherwise).

Objective Function:
Minimize the total cost, which includes both hiring and assignment costs.

######### MILP Model:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:}
\[
\text{Minimize } \sum_{j=1}^{J} f_j y_j + \sum_{i=1}^{I} \sum_{j=1}^{J} c_{i,j} x_{i,j}
\]

\textbf{Subject to:}

1. Each project must be assigned to exactly one consultant:
\[
\sum_{j=1}^{J} x_{i,j} = 1, \quad \forall i \in \{1, \ldots, I\}
\]

2. A consultant can handle at most \( K \) projects:
\[
\sum_{i=1}^{I} x_{i,j} \leq K y_j, \quad \forall j \in \{1, \ldots, J\}
\]

3. The assignment variable is binary:
\[
x_{i,j} \in \{0, 1\}, \quad \forall i \in \{1, \ldots, I\}, \forall j \in \{1, \ldots, J\}
\]

4. The hiring variable is binary:
\[
y_j \in \{0, 1\}, \quad \forall j \in \{1, \ldots, J\}
\]

\end{document}
```

######### Explanation:
- **Objective Function**: The goal is to minimize the sum of both fixed costs and additional assignment costs.
- **Constraint 1**: Ensures that each project is assigned to exactly one consultant.
- **Constraint 2**: Limits the number of projects a consultant can take to \( K \), and ensures that a consultant is only assigned projects if they are hired.
- **Constraints 3 and 4**: Define the binary nature of the decision variables.

This MILP model can be solved using optimization software that supports integer programming, such as CPLEX, Gurobi, or open-source solvers like CBC.

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
\text{Minimize } \sum_{j=1}^{J} f_j y_j + \sum_{i=1}^{I} \sum_{j=1}^{J} c_{i,j} x_{i,j}
\]

\textbf{Subject to:}

1. Each project must be assigned to exactly one consultant:
\[
\sum_{j=1}^{J} x_{i,j} = 1, \quad \forall i \in \{1, \ldots, I\}
\]

2. A consultant can handle at most \( K \) projects:
\[
\sum_{i=1}^{I} x_{i,j} \leq K y_j, \quad \forall j \in \{1, \ldots, J\}
\]

3. The assignment variable is binary:
\[
x_{i,j} \in \{0, 1\}, \quad \forall i \in \{1, \ldots, I\}, \forall j \in \{1, \ldots, J\}
\]

4. The hiring variable is binary:
\[
y_j \in \{0, 1\}, \quad \forall j \in \{1, \ldots, J\}
\]

\end{document}</MATH_MODEL>
<DATA>
{'fixed_costs': [100, 150, 135], 'additional_costs': [[10, 12, 20], [10, 8, 12], [15, 8, 20], [10, 6, 15], [8, 10, 15]], 'max_projects_per_consultant': 3}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data extracted from the provided JSON format
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

#### Define parameters
I = len(data['additional_costs'])  #### Number of projects
J = len(data['fixed_costs'])        #### Number of consultants
K = data['max_projects_per_consultant']  #### Max projects per consultant

#### Create the problem
problem = pulp.LpProblem("Consultant_Assignment", pulp.LpMinimize)

#### Decision variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(I) for j in range(J)), cat='Binary')  #### Project i assigned to consultant j
y = pulp.LpVariable.dicts("y", range(J), cat='Binary')  #### Consultant j is hired

#### Objective function
problem += (
    pulp.lpSum(data['fixed_costs'][j] * y[j] for j in range(J)) +
    pulp.lpSum(data['additional_costs'][i][j] * x[i, j] for i in range(I) for j in range(J))
)

#### Constraints
#### Each project must be assigned to exactly one consultant
for i in range(I):
    problem += pulp.lpSum(x[i, j] for j in range(J)) == 1

#### A consultant can handle at most K projects
for j in range(J):
    problem += pulp.lpSum(x[i, j] for i in range(I)) <= K * y[j]

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

