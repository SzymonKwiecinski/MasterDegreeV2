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

#### Problem parameters
fixed_costs = data['fixed_costs']
additional_costs = data['additional_costs']
max_projects_per_consultant = data['max_projects_per_consultant']

I = len(additional_costs)  #### Number of projects
J = len(fixed_costs)       #### Number of consultants

#### Define the problem
problem = pulp.LpProblem("Consultant_Assignment_Problem", pulp.LpMinimize)

#### Decision variables
assignments = pulp.LpVariable.dicts("assignment", (range(J), range(I)), 
                                     cat='Binary')  #### assignment[j][i] = 1 if consultant j is assigned project i

#### Objective function
total_cost = pulp.lpSum(fixed_costs[j] * pulp.lpSum(assignments[j][i] for i in range(I)) for j in range(J)) + \
                       pulp.lpSum(additional_costs[i][j] * assignments[j][i] for i in range(I) for j in range(J))
problem += total_cost

#### Constraints
#### Each project is assigned to exactly one consultant
for i in range(I):
    problem += pulp.lpSum(assignments[j][i] for j in range(J)) == 1, f"Project_{i}_assignment"

#### Each consultant can handle a maximum number of projects
for j in range(J):
    problem += pulp.lpSum(assignments[j][i] for i in range(I)) <= max_projects_per_consultant, f"Consultant_{j}_max_projects"

#### Solve the problem
problem.solve()

#### Prepare the output
assignments_result = [[int(assignments[j][i].value()) for i in range(I)] for j in range(J)]
total_cost_value = pulp.value(problem.objective)

#### Output the results
output = {
    "assignments": assignments_result,
    "total_cost": total_cost_value
}

print(json.dumps(output))  #### Printing in JSON format
print(f' (Objective Value): <OBJ>{total_cost_value}</OBJ>')
```

