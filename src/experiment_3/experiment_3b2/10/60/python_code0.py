import pulp

# Data extraction from the provided JSON
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

# Set of projects and consultants
projects = range(len(data['additional_costs']))
consultants = range(len(data['fixed_costs']))

# Create the model
problem = pulp.LpProblem("Consultant_Assignment_Problem", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", (projects, consultants), cat='Binary')  # Project assignment
y = pulp.LpVariable.dicts("y", consultants, cat='Binary')               # Consultant hiring

# Objective function
problem += pulp.lpSum(data['fixed_costs'][j] * y[j] for j in consultants) + \
           pulp.lpSum(data['additional_costs'][i][j] * x[i][j] for i in projects for j in consultants)

# Constraints
# Each project is assigned to exactly one consultant
for i in projects:
    problem += pulp.lpSum(x[i][j] for j in consultants) == 1

# Consultant limits on projects
for j in consultants:
    problem += pulp.lpSum(x[i][j] for i in projects) <= data['max_projects_per_consultant'] * y[j]

# Project assignment only if consultant is hired
for i in projects:
    for j in consultants:
        problem += x[i][j] <= y[j]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')