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

# Number of projects and consultants
I = len(data['additional_costs'])
J = len(data['fixed_costs'])
K = data['max_projects_per_consultant']

# Initialize the problem
problem = pulp.LpProblem("Project_Assignment_Problem", pulp.LpMinimize)

# Decision variables
x = [pulp.LpVariable(f"x_{j}", cat="Binary") for j in range(J)]
y = [[pulp.LpVariable(f"y_{i}_{j}", cat="Binary") for j in range(J)] for i in range(I)]

# Objective function
problem += (pulp.lpSum([data['fixed_costs'][j] * x[j] for j in range(J)]) +
            pulp.lpSum([data['additional_costs'][i][j] * y[i][j] for i in range(I) for j in range(J)]))

# Constraints
# Each project must be assigned to exactly one consultant
for i in range(I):
    problem += pulp.lpSum([y[i][j] for j in range(J)]) == 1

# A consultant can only work on projects if they are hired
for i in range(I):
    for j in range(J):
        problem += y[i][j] <= x[j]

# Each consultant can be assigned a maximum of K projects
for j in range(J):
    problem += pulp.lpSum([y[i][j] for i in range(I)]) <= K * x[j]

# Solve the problem
problem.solve()

# Results
assignments = {(i, j): pulp.value(y[i][j]) for i in range(I) for j in range(J)}
total_cost = pulp.value(problem.objective)

# Print the objective
print(f'(Objective Value): <OBJ>{total_cost}</OBJ>')