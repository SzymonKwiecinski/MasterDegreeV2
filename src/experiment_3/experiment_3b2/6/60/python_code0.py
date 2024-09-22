import pulp

# Data from the provided JSON
data = {
    'fixed_costs': [100, 150, 135],
    'additional_costs': [[10, 12, 20], [10, 8, 12], [15, 8, 20], [10, 6, 15], [8, 10, 15]],
    'max_projects_per_consultant': 3
}

# Number of projects and consultants
I = len(data['additional_costs'])  # number of projects
J = len(data['fixed_costs'])        # number of consultants
K = data['max_projects_per_consultant']

# Create the problem
problem = pulp.LpProblem("ConsultantAssignment", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(I) for j in range(J)), cat='Binary')
y = pulp.LpVariable.dicts("y", range(J), cat='Binary')

# Objective Function
problem += (pulp.lpSum(data['fixed_costs'][j] * y[j] for j in range(J)) +
            pulp.lpSum(data['additional_costs'][i][j] * x[i, j] for i in range(I) for j in range(J)))

# Constraints
# Each project must be assigned to exactly one consultant
for i in range(I):
    problem += pulp.lpSum(x[i, j] for j in range(J)) == 1

# Consultants can handle at most K projects
for j in range(J):
    problem += pulp.lpSum(x[i, j] for i in range(I)) <= K * y[j]

# Project can be assigned only if the consultant is hired
for i in range(I):
    for j in range(J):
        problem += x[i, j] <= y[j]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')