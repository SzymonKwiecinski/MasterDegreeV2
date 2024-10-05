import pulp

# Parse the input data
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

I = len(additional_costs)  # Number of projects
J = len(fixed_costs)       # Number of consultants

# Initialize the problem
problem = pulp.LpProblem("Consultant_Assignment_Problem", pulp.LpMinimize)

# Decision variables
x = [
    [pulp.LpVariable(f'x_{j}_{i}', cat='Binary') for i in range(I)] 
    for j in range(J)
]

y = [pulp.LpVariable(f'y_{j}', cat='Binary') for j in range(J)]

# Objective function
problem += pulp.lpSum(
    [fixed_costs[j] * y[j] + pulp.lpSum([additional_costs[i][j] * x[j][i] for i in range(I)]) for j in range(J)]
)

# Constraints
# Each project is assigned to exactly one consultant
for i in range(I):
    problem += pulp.lpSum([x[j][i] for j in range(J)]) == 1

# A consultant can be assigned a project only if they are hired
for j in range(J):
    for i in range(I):
        problem += x[j][i] <= y[j]

# A consultant cannot be assigned more projects than the maximum allowed
for j in range(J):
    problem += pulp.lpSum([x[j][i] for i in range(I)]) <= max_projects_per_consultant

# Solve the problem
problem.solve()

# Generate the output
assignments = [[int(x[j][i].varValue) for i in range(I)] for j in range(J)]
total_cost = pulp.value(problem.objective)

output = {
    'assignments': assignments,
    'total_cost': total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')