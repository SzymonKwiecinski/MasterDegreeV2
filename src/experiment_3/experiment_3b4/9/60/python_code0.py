import pulp

# Data
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
J = len(fixed_costs)  # Number of consultants

# Problem
problem = pulp.LpProblem("Project_Assignment", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(I) for j in range(J)), cat='Binary')
y = pulp.LpVariable.dicts("y", (j for j in range(J)), cat='Binary')

# Objective Function
problem += (
    pulp.lpSum(fixed_costs[j] * y[j] for j in range(J)) +
    pulp.lpSum(additional_costs[i][j] * x[i, j] for i in range(I) for j in range(J))
)

# Constraints
# Each project is assigned to exactly one consultant
for i in range(I):
    problem += pulp.lpSum(x[i, j] for j in range(J)) == 1

# A consultant can handle up to K projects
for j in range(J):
    problem += pulp.lpSum(x[i, j] for i in range(I)) <= K * y[j]

# If project i is assigned, consultant j must be hired
for i in range(I):
    for j in range(J):
        problem += x[i, j] <= y[j]

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')