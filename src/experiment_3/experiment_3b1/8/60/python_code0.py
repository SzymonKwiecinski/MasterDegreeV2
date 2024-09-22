import pulp

# Data from the input
data = {
    'fixed_costs': [100, 150, 135],
    'additional_costs': [[10, 12, 20], [10, 8, 12], [15, 8, 20], [10, 6, 15], [8, 10, 15]],
    'max_projects_per_consultant': 3
}

# Define indices
I = len(data['additional_costs'])  # Number of projects
J = len(data['fixed_costs'])        # Number of consultants
K = data['max_projects_per_consultant']

# Create the problem
problem = pulp.LpProblem("Consultant_Assignment", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(J), lowBound=0, upBound=1, cat='Binary')  # Consultant hired
y = pulp.LpVariable.dicts("y", (range(I), range(J)), lowBound=0, upBound=1, cat='Binary')  # Project assigned

# Objective function
problem += pulp.lpSum(data['fixed_costs'][j] * x[j] for j in range(J)) + \
           pulp.lpSum(data['additional_costs'][i][j] * y[i][j] for i in range(I) for j in range(J))

# Constraints
# 1. Each project must be assigned to exactly one consultant
for i in range(I):
    problem += pulp.lpSum(y[i][j] for j in range(J)) == 1

# 2. A consultant can only assign projects if they are hired
for i in range(I):
    for j in range(J):
        problem += y[i][j] <= x[j]

# 3. Each consultant can handle a maximum of K projects
for j in range(J):
    problem += pulp.lpSum(y[i][j] for i in range(I)) <= K * x[j]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')