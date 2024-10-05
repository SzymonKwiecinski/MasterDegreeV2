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

I = len(data['additional_costs'])  # Number of projects
J = len(data['fixed_costs'])        # Number of consultants
K = data['max_projects_per_consultant']  # Max projects per consultant

# Create the problem
problem = pulp.LpProblem("Project_Assignment", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", (range(I), range(J)), cat='Binary')
y = pulp.LpVariable.dicts("y", range(J), cat='Binary')

# Objective Function
problem += (
    pulp.lpSum(data['fixed_costs'][j] * y[j] for j in range(J)) + 
    pulp.lpSum(data['additional_costs'][i][j] * x[i][j] for i in range(I) for j in range(J))
)

# Constraints
# Each project must be assigned to exactly one consultant
for i in range(I):
    problem += pulp.lpSum(x[i][j] for j in range(J)) == 1

# A consultant must be hired if they are assigned any projects
for i in range(I):
    for j in range(J):
        problem += x[i][j] <= y[j]

# Each consultant can be assigned up to K projects
for j in range(J):
    problem += pulp.lpSum(x[i][j] for i in range(I)) <= K * y[j]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')