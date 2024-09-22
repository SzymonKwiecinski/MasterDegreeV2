import pulp
import json

# Input data
data = {'fixed_costs': [100, 150, 135], 'additional_costs': [[10, 12, 20], [10, 8, 12], [15, 8, 20], [10, 6, 15], [8, 10, 15]], 'max_projects_per_consultant': 3}

# Extracting data from JSON
fixed_costs = data['fixed_costs']
additional_costs = data['additional_costs']
max_projects_per_consultant = data['max_projects_per_consultant']

# Defining the problem
I = len(additional_costs)  # Number of projects
J = len(fixed_costs)       # Number of consultants

problem = pulp.LpProblem("Consultant_Assignment_Problem", pulp.LpMinimize)

# Decision variables
assignments = pulp.LpVariable.dicts("assignment", (range(J), range(I)), cat='Binary')
hire = pulp.LpVariable.dicts("hire", range(J), cat='Binary')

# Objective function
problem += pulp.lpSum(fixed_costs[j] * hire[j] for j in range(J)) + pulp.lpSum(additional_costs[i][j] * assignments[j][i] for i in range(I) for j in range(J))

# Constraints
# Each project must be assigned to exactly one consultant
for i in range(I):
    problem += pulp.lpSum(assignments[j][i] for j in range(J)) == 1

# A consultant can be assigned a maximum of K projects
for j in range(J):
    problem += pulp.lpSum(assignments[j][i] for i in range(I)) <= max_projects_per_consultant * hire[j]

# Solve the problem
problem.solve()

# Prepare the output
assignments_result = [[int(assignments[j][i].value()) for i in range(I)] for j in range(J)]
total_cost = pulp.value(problem.objective)

output = {
    "assignments": assignments_result,
    "total_cost": total_cost
}

# Print the result
print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')