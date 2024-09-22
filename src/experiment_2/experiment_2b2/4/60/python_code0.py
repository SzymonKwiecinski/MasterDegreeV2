import pulp

# Data from JSON
data = {
    'fixed_costs': [100, 150, 135],
    'additional_costs': [[10, 12, 20], [10, 8, 12], [15, 8, 20], [10, 6, 15], [8, 10, 15]],
    'max_projects_per_consultant': 3
}

# Extracting data
fixed_costs = data['fixed_costs']
additional_costs = data['additional_costs']
K = data['max_projects_per_consultant']

I = len(additional_costs)  # Number of projects
J = len(fixed_costs)  # Number of consultants

# Initialize the problem
problem = pulp.LpProblem("Consultant_Assignment_Problem", pulp.LpMinimize)

# Decision variables
assignments = [[pulp.LpVariable(f'assign_{j}_{i}', cat='Binary') for i in range(I)] for j in range(J)]
hire = [pulp.LpVariable(f'hire_{j}', cat='Binary') for j in range(J)]

# Objective function
total_cost = pulp.lpSum([fixed_costs[j] * hire[j] for j in range(J)]) + \
             pulp.lpSum([additional_costs[i][j] * assignments[j][i] for j in range(J) for i in range(I)])

problem += total_cost

# Constraints
# Each project is assigned to exactly one consultant
for i in range(I):
    problem += pulp.lpSum([assignments[j][i] for j in range(J)]) == 1

# A consultant can be assigned to at most K projects
for j in range(J):
    problem += pulp.lpSum([assignments[j][i] for i in range(I)]) <= K

# Project assignment implies hiring the consultant
for j in range(J):
    for i in range(I):
        problem += assignments[j][i] <= hire[j]

# Solve the problem
problem.solve()

# Extract results
assignments_result = [[int(assignments[j][i].varValue) for i in range(I)] for j in range(J)]
total_cost_value = pulp.value(problem.objective)

# Result formatting
result = {
    "assignments": assignments_result,
    "total_cost": total_cost_value
}

# Print the result and objective value
print(f'Result: {result}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')