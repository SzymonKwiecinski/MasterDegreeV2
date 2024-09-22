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
To solve this problem, we need to create a mathematical model using Mixed-Integer Linear Programming (MILP). Our goal is to minimize the total cost of assigning projects to consultants, which includes both the fixed hiring costs and the additional assignment costs.

Here's the mathematical model in LATEX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Indices:}
\begin{align*}
& i = 1, 2, \ldots, I \quad \text{(projects)} \\
& j = 1, 2, \ldots, J \quad \text{(consultants)}
\end{align*}

\textbf{Parameters:}
\begin{align*}
& f_j \quad \text{= fixed cost for hiring consultant } j \\
& c_{i,j} \quad \text{= additional cost for assigning project } i \text{ to consultant } j \\
& K \quad \text{= maximum number of projects a consultant can be assigned}
\end{align*}

\textbf{Decision Variables:}
\begin{align*}
& x_{i,j} \quad \text{= 1, if project } i \text{ is assigned to consultant } j, \text{ 0 otherwise} \\
& y_j \quad \text{= 1, if consultant } j \text{ is hired, \text{ 0 otherwise}}
\end{align*}

\textbf{Objective:}
\[
\text{Minimize} \quad Z = \sum_{j=1}^J f_j y_j + \sum_{i=1}^I \sum_{j=1}^J c_{i,j} x_{i,j}
\]

\textbf{Constraints:}
\begin{align*}
& \sum_{j=1}^J x_{i,j} = 1, \quad \forall i = 1, \ldots, I \quad \text{(Each project must be assigned to exactly one consultant)} \\
& \sum_{i=1}^I x_{i,j} \leq K y_j, \quad \forall j = 1, \ldots, J \quad \text{(Consultants can handle at most } K \text{ projects)} \\
& x_{i,j} \leq y_j, \quad \forall i = 1, \ldots, I, \quad j = 1, \ldots, J \quad \text{(Project can be assigned only if the consultant is hired)} \\
& x_{i,j} \in \{0, 1\}, \quad \forall i = 1, \ldots, I, \quad j = 1, \ldots, J \\
& y_j \in \{0, 1\}, \quad \forall j = 1, \ldots, J
\end{align*}

\end{document}
```

This model includes:
1. An objective function minimizing total cost, which is the sum of fixed costs for hiring consultants and additional costs for their project assignments.
2. A constraint ensuring each project is assigned to exactly one consultant.
3. A constraint limiting the number of projects per consultant to the maximum allowable number \( K \).
4. A constraint ensuring a project is only assigned if the consultant is hired.
5. Binary constraints for both decision variables. 

The solution to this model provides the optimal assignments that minimize costs while satisfying all constraints.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Indices:}
\begin{align*}
& i = 1, 2, \ldots, I \quad \text{(projects)} \\
& j = 1, 2, \ldots, J \quad \text{(consultants)}
\end{align*}

\textbf{Parameters:}
\begin{align*}
& f_j \quad \text{= fixed cost for hiring consultant } j \\
& c_{i,j} \quad \text{= additional cost for assigning project } i \text{ to consultant } j \\
& K \quad \text{= maximum number of projects a consultant can be assigned}
\end{align*}

\textbf{Decision Variables:}
\begin{align*}
& x_{i,j} \quad \text{= 1, if project } i \text{ is assigned to consultant } j, \text{ 0 otherwise} \\
& y_j \quad \text{= 1, if consultant } j \text{ is hired, \text{ 0 otherwise}}
\end{align*}

\textbf{Objective:}
\[
\text{Minimize} \quad Z = \sum_{j=1}^J f_j y_j + \sum_{i=1}^I \sum_{j=1}^J c_{i,j} x_{i,j}
\]

\textbf{Constraints:}
\begin{align*}
& \sum_{j=1}^J x_{i,j} = 1, \quad \forall i = 1, \ldots, I \quad \text{(Each project must be assigned to exactly one consultant)} \\
& \sum_{i=1}^I x_{i,j} \leq K y_j, \quad \forall j = 1, \ldots, J \quad \text{(Consultants can handle at most } K \text{ projects)} \\
& x_{i,j} \leq y_j, \quad \forall i = 1, \ldots, I, \quad j = 1, \ldots, J \quad \text{(Project can be assigned only if the consultant is hired)} \\
& x_{i,j} \in \{0, 1\}, \quad \forall i = 1, \ldots, I, \quad j = 1, \ldots, J \\
& y_j \in \{0, 1\}, \quad \forall j = 1, \ldots, J
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'fixed_costs': [100, 150, 135], 'additional_costs': [[10, 12, 20], [10, 8, 12], [15, 8, 20], [10, 6, 15], [8, 10, 15]], 'max_projects_per_consultant': 3}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the provided JSON
data = {
    'fixed_costs': [100, 150, 135],
    'additional_costs': [[10, 12, 20], [10, 8, 12], [15, 8, 20], [10, 6, 15], [8, 10, 15]],
    'max_projects_per_consultant': 3
}

#### Number of projects and consultants
I = len(data['additional_costs'])  #### number of projects
J = len(data['fixed_costs'])        #### number of consultants
K = data['max_projects_per_consultant']

#### Create the problem
problem = pulp.LpProblem("ConsultantAssignment", pulp.LpMinimize)

#### Decision Variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(I) for j in range(J)), cat='Binary')
y = pulp.LpVariable.dicts("y", range(J), cat='Binary')

#### Objective Function
problem += (pulp.lpSum(data['fixed_costs'][j] * y[j] for j in range(J)) +
            pulp.lpSum(data['additional_costs'][i][j] * x[i, j] for i in range(I) for j in range(J)))

#### Constraints
#### Each project must be assigned to exactly one consultant
for i in range(I):
    problem += pulp.lpSum(x[i, j] for j in range(J)) == 1

#### Consultants can handle at most K projects
for j in range(J):
    problem += pulp.lpSum(x[i, j] for i in range(I)) <= K * y[j]

#### Project can be assigned only if the consultant is hired
for i in range(I):
    for j in range(J):
        problem += x[i, j] <= y[j]

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

