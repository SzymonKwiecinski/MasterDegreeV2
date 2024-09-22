# START: OnePrompt 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Python. Based on description you solve given problem using Pulp python library. Python code place between ```python and ```. You receive the data in json format between: <DATA></DATA>. Do not change data format! Do not use `while` loop in python code! Do not include 'pip install' in script. Assume every python package is installed Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')`  
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
<DATA>
{'fixed_costs': [100, 150, 135], 'additional_costs': [[10, 12, 20], [10, 8, 12], [15, 8, 20], [10, 6, 15], [8, 10, 15]], 'max_projects_per_consultant': 3}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import json
import pulp

#### Input data
data = {'fixed_costs': [100, 150, 135], 
        'additional_costs': [[10, 12, 20], 
                             [10, 8, 12], 
                             [15, 8, 20], 
                             [10, 6, 15], 
                             [8, 10, 15]], 
        'max_projects_per_consultant': 3}

#### Define problem
I = len(data['additional_costs'])  #### Number of projects
J = len(data['fixed_costs'])        #### Number of consultants
K = data['max_projects_per_consultant']  #### Max projects per consultant

#### Create the problem variable
problem = pulp.LpProblem("Consultant_Assignment", pulp.LpMinimize)

#### Decision variables
assignments = pulp.LpVariable.dicts("assignment", 
                                     ((j, i) for j in range(J) for i in range(I)), 
                                     cat='Binary')
hire = pulp.LpVariable.dicts("hire", 
                              range(J), 
                              cat='Binary')

#### Objective function
problem += (pulp.lpSum(data['fixed_costs'][j] * hire[j] for j in range(J)) + 
            pulp.lpSum(data['additional_costs'][i][j] * assignments[(j, i)] 
                       for i in range(I) for j in range(J)))

#### Constraints
#### Each project must be assigned to exactly one consultant
for i in range(I):
    problem += pulp.lpSum(assignments[(j, i)] for j in range(J)) == 1

#### Each consultant can be assigned to a maximum of K projects
for j in range(J):
    problem += pulp.lpSum(assignments[(j, i)] for i in range(I)) <= K * hire[j]

#### Solve the problem
problem.solve()

#### Collect the results
assignment_matrix = [[0 for _ in range(I)] for _ in range(J)]
for j in range(J):
    for i in range(I):
        assignment_matrix[j][i] = int(assignments[(j, i)].value())

total_cost = pulp.value(problem.objective)

#### Prepare output
output = {
    "assignments": assignment_matrix,
    "total_cost": total_cost
}

#### Print result
print(json.dumps(output))
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')
```

