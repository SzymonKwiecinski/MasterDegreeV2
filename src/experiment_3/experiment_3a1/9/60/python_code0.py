import pulp

# Data extraction from the provided JSON-like structure
data = {
    'fixed_costs': [100, 150, 135],
    'additional_costs': [[10, 12, 20], [10, 8, 12], [15, 8, 20], [10, 6, 15], [8, 10, 15]],
    'max_projects_per_consultant': 3
}

# Define problem
I = len(data['additional_costs'])  # Number of projects
J = len(data['fixed_costs'])        # Number of consultants
K = data['max_projects_per_consultant']
fixed_costs = data['fixed_costs']
additional_costs = data['additional_costs']

# Problem setup
problem = pulp.LpProblem("Consultant_Assignment_Problem", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("Hire_Consultant", range(J), cat='Binary')
y = pulp.LpVariable.dicts("Assign_Project", (range(I), range(J)), cat='Binary')

# Objective function
problem += pulp.lpSum(fixed_costs[j] * x[j] for j in range(J)) + pulp.lpSum(additional_costs[i][j] * y[i][j] for i in range(I) for j in range(J))

# Constraints
# Each project is assigned to exactly one consultant
for i in range(I):
    problem += pulp.lpSum(y[i][j] for j in range(J)) == 1

# Consultant can take at most K projects
for j in range(J):
    problem += pulp.lpSum(y[i][j] for i in range(I)) <= K * x[j]

# A project can only be assigned to a hired consultant
for i in range(I):
    for j in range(J):
        problem += y[i][j] <= x[j]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')