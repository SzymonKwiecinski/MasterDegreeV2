import pulp

# Extracting data from the provided JSON format
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

fixed_costs = data['fixed_costs']
additional_costs = data['additional_costs']
max_projects_per_consultant = data['max_projects_per_consultant']

# Number of consultants and projects
J = len(fixed_costs)
I = len(additional_costs)

# Define the problem
problem = pulp.LpProblem("Consultant_Project_Assignment", pulp.LpMinimize)

# Decision variables
y = [pulp.LpVariable(f'y_{j}', cat='Binary') for j in range(J)]
x = [[pulp.LpVariable(f'x_{i}_{j}', cat='Binary') for j in range(J)] for i in range(I)]

# Objective Function
problem += (
    pulp.lpSum(fixed_costs[j] * y[j] for j in range(J)) +
    pulp.lpSum(additional_costs[i][j] * x[i][j] for i in range(I) for j in range(J))
)

# Constraints
# Each project is assigned to exactly one consultant
for i in range(I):
    problem += pulp.lpSum(x[i][j] for j in range(J)) == 1

# A consultant can take up to a limited number of projects if hired
for j in range(J):
    problem += pulp.lpSum(x[i][j] for i in range(I)) <= max_projects_per_consultant * y[j]

# A project can only be assigned to a consultant if the consultant is hired
for i in range(I):
    for j in range(J):
        problem += x[i][j] <= y[j]

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')