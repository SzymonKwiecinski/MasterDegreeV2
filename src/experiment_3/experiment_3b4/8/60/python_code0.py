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

I = len(additional_costs)
J = len(fixed_costs)

# Define the problem
problem = pulp.LpProblem("Consultant_Assignment", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("assignment", (range(I), range(J)), cat='Binary')
y = pulp.LpVariable.dicts("consultant_used", range(J), cat='Binary')

# Objective function
problem += pulp.lpSum(fixed_costs[j] * y[j] for j in range(J)) + \
           pulp.lpSum(additional_costs[i][j] * x[i][j] for i in range(I) for j in range(J))

# Constraints
# Each project is assigned to exactly one consultant
for i in range(I):
    problem += pulp.lpSum(x[i][j] for j in range(J)) == 1

# Consultant capacity
for j in range(J):
    problem += pulp.lpSum(x[i][j] for i in range(I)) <= K * y[j]

# If a project is assigned to a consultant, the consultant must be used
for i in range(I):
    for j in range(J):
        problem += x[i][j] <= y[j]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')