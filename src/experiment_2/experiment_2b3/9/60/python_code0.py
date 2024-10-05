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

J = len(data['fixed_costs'])  # Number of consultants
I = len(data['additional_costs'])  # Number of projects
K = data['max_projects_per_consultant']

# Create the MILP problem
problem = pulp.LpProblem("Consultant_Assignment_Optimization", pulp.LpMinimize)

# Define decision variables
assignment = pulp.LpVariable.dicts("assignment", ((j, i) for j in range(J) for i in range(I)), cat='Binary')
hire_consultant = pulp.LpVariable.dicts("hire", (j for j in range(J)), cat='Binary')

# Objective function: Minimize the total cost
problem += pulp.lpSum([data['fixed_costs'][j] * hire_consultant[j] for j in range(J)]) + \
           pulp.lpSum([data['additional_costs'][i][j] * assignment[j, i] for j in range(J) for i in range(I)])

# Constraints
# Each project must be assigned to exactly one consultant
for i in range(I):
    problem += pulp.lpSum([assignment[j, i] for j in range(J)]) == 1

# Each consultant can be assigned up to K projects
for j in range(J):
    problem += pulp.lpSum([assignment[j, i] for i in range(I)]) <= K

# A consultant can only be assigned a project if they are hired
for j in range(J):
    for i in range(I):
        problem += assignment[j, i] <= hire_consultant[j]

# Solve the problem
problem.solve()

# Prepare output data
assignments = [[pulp.value(assignment[j, i]) for i in range(I)] for j in range(J)]
total_cost = pulp.value(problem.objective)

# Output format
output = {
    "assignments": assignments,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')