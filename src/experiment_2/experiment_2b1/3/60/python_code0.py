import pulp
import json

# Input data
data = json.loads('{"fixed_costs": [100, 150, 135], "additional_costs": [[10, 12, 20], [10, 8, 12], [15, 8, 20], [10, 6, 15], [8, 10, 15]], "max_projects_per_consultant": 3}')

fixed_costs = data['fixed_costs']
additional_costs = data['additional_costs']
max_projects_per_consultant = data['max_projects_per_consultant']

I = len(additional_costs)  # number of projects
J = len(fixed_costs)  # number of consultants

# Create the problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Decision variables
assignments = pulp.LpVariable.dicts("assignment", (range(J), range(I)), cat='Binary')
consultant_hired = pulp.LpVariable.dicts("hired", range(J), cat='Binary')

# Objective function
problem += (
    pulp.lpSum(fixed_costs[j] * consultant_hired[j] for j in range(J)) + 
    pulp.lpSum(additional_costs[i][j] * assignments[j][i] for j in range(J) for i in range(I))
)

# Constraints

# Each project must be assigned to exactly one consultant
for i in range(I):
    problem += pulp.lpSum(assignments[j][i] for j in range(J)) == 1

# A consultant can only handle a limited number of projects
for j in range(J):
    problem += pulp.lpSum(assignments[j][i] for i in range(I)) <= max_projects_per_consultant * consultant_hired[j]

# Solve the problem
problem.solve()

# Prepare output
assignments_result = [[int(assignments[j][i].varValue) for i in range(I)] for j in range(J)]
total_cost = pulp.value(problem.objective)

output = {
    "assignments": assignments_result,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')