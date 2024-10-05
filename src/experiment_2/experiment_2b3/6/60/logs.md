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

#### Data provided
data = {'fixed_costs': [100, 150, 135], 'additional_costs': [[10, 12, 20], [10, 8, 12], [15, 8, 20], [10, 6, 15], [8, 10, 15]], 'max_projects_per_consultant': 3}

fixed_costs = data['fixed_costs']
additional_costs = data['additional_costs']
max_projects_per_consultant = data['max_projects_per_consultant']

num_projects = len(additional_costs)
num_consultants = len(fixed_costs)

#### Problem
problem = pulp.LpProblem("Minimize_Assignment_Costs", pulp.LpMinimize)

#### Variables
assignments = pulp.LpVariable.dicts("Assignment", ((j, i) for j in range(num_consultants) for i in range(num_projects)), cat='Binary')
hire = pulp.LpVariable.dicts("Hire", (j for j in range(num_consultants)), cat='Binary')

#### Objective Function
problem += pulp.lpSum([fixed_costs[j] * hire[j] for j in range(num_consultants)]) + \
    pulp.lpSum([additional_costs[i][j] * assignments[j, i] for j in range(num_consultants) for i in range(num_projects)])

#### Constraints
for i in range(num_projects):
    problem += pulp.lpSum([assignments[j, i] for j in range(num_consultants)]) == 1, f"Project_{i}_Assignment"

for j in range(num_consultants):
    problem += pulp.lpSum([assignments[j, i] for i in range(num_projects)]) <= max_projects_per_consultant * hire[j], f"Consultant_{j}_Capacity"

#### Solve the problem
problem.solve()

#### Results
assignments_result = [[pulp.value(assignments[j, i]) for i in range(num_projects)] for j in range(num_consultants)]
total_cost = pulp.value(problem.objective)

output = {
    "assignments": assignments_result,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

