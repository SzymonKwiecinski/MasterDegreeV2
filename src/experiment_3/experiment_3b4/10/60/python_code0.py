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

fixed_costs = data['fixed_costs']
additional_costs = data['additional_costs']
K = data['max_projects_per_consultant']

I = len(additional_costs)  # Number of projects
J = len(fixed_costs)       # Number of consultants

# Define the problem
problem = pulp.LpProblem("Consultant_Selection", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((j, i) for j in range(J) for i in range(I)), cat='Binary')
y = pulp.LpVariable.dicts("y", (j for j in range(J)), cat='Binary')

# Objective function
problem += pulp.lpSum(fixed_costs[j] * y[j] + pulp.lpSum(additional_costs[i][j] * x[j, i] for i in range(I)) for j in range(J))

# Constraints
for i in range(I):
    problem += pulp.lpSum(x[j, i] for j in range(J)) == 1

for j in range(J):
    problem += pulp.lpSum(x[j, i] for i in range(I)) <= K * y[j]

for i in range(I):
    for j in range(J):
        problem += x[j, i] <= y[j]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')