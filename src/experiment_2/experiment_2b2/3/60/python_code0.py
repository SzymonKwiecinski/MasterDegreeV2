import pulp

# Data from JSON
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

# Extract data
fixed_costs = data["fixed_costs"]
additional_costs = data["additional_costs"]
max_projects_per_consultant = data["max_projects_per_consultant"]

I = len(additional_costs)  # Number of projects
J = len(fixed_costs)  # Number of consultants

# Create the MILP problem
problem = pulp.LpProblem("Consultant_Assignment", pulp.LpMinimize)

# Variables
assignment = [
    [pulp.LpVariable(f'assign_{j}_{i}', cat='Binary') for i in range(I)]
    for j in range(J)
]

hire = [pulp.LpVariable(f'hire_{j}', cat='Binary') for j in range(J)]

# Objective function
total_cost = pulp.lpSum([
    hire[j] * fixed_costs[j] + pulp.lpSum(assignment[j][i] * additional_costs[i][j] for i in range(I))
    for j in range(J)
])

problem += total_cost

# Constraints
# Every project must be assigned to exactly one consultant
for i in range(I):
    problem += pulp.lpSum(assignment[j][i] for j in range(J)) == 1

# A consultant can handle a maximum of K projects
for j in range(J):
    problem += pulp.lpSum(assignment[j][i] for i in range(I)) <= max_projects_per_consultant

# A project can be assigned to consultant j only if consultant j is hired
for j in range(J):
    for i in range(I):
        problem += assignment[j][i] <= hire[j]

# Solve the problem
problem.solve()

# Prepare the output
assignments = [[int(assignment[j][i].varValue) for i in range(I)] for j in range(J)]
total_cost = pulp.value(problem.objective)

output = {
    "assignments": assignments,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')