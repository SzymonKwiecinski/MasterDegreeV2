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
import pulp
import json

#### Input data
data = {'fixed_costs': [100, 150, 135], 
        'additional_costs': [[10, 12, 20], 
                             [10, 8, 12], 
                             [15, 8, 20], 
                             [10, 6, 15], 
                             [8, 10, 15]], 
        'max_projects_per_consultant': 3}

#### Extracting the data
fixed_costs = data['fixed_costs']
additional_costs = data['additional_costs']
max_projects_per_consultant = data['max_projects_per_consultant']

I = len(additional_costs)  #### number of projects
J = len(fixed_costs)       #### number of consultants

#### Create the problem
problem = pulp.LpProblem("ConsultantAssignment", pulp.LpMinimize)

#### Decision variables
assignment = pulp.LpVariable.dicts("assignment", (range(J), range(I)), cat='Binary')
consultant_hired = pulp.LpVariable.dicts("consultant_hired", range(J), cat='Binary')

#### Objective function
problem += pulp.lpSum(fixed_costs[j] * consultant_hired[j] for j in range(J)) + \
           pulp.lpSum(additional_costs[i][j] * assignment[j][i] for i in range(I) for j in range(J))

#### Constraints
for i in range(I):
    problem += pulp.lpSum(assignment[j][i] for j in range(J)) == 1  #### Each project is assigned to exactly one consultant

for j in range(J):
    problem += pulp.lpSum(assignment[j][i] for i in range(I)) <= max_projects_per_consultant * consultant_hired[j]  #### Projects assigned do not exceed maximum

#### Solve the problem
problem.solve()

#### Prepare the results
assignments = [[int(assignment[j][i].varValue) for i in range(I)] for j in range(J)]
total_cost = pulp.value(problem.objective)

#### Output results
output = {
    "assignments": assignments,
    "total_cost": total_cost
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')
```

