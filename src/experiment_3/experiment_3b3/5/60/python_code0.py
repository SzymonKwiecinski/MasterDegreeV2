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
J = len(fixed_costs)       # Number of consultants

# Initialize the problem
problem = pulp.LpProblem("Consultant_Assignment_Problem", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(J), cat='Binary')
y = pulp.LpVariable.dicts("y", ((i, j) for i in range(I) for j in range(J)), cat='Binary')

# Objective Function
problem += pulp.lpSum(fixed_costs[j] * x[j] for j in range(J)) + \
           pulp.lpSum(additional_costs[i][j] * y[(i, j)] for i in range(I) for j in range(J))

# Constraints
# Each project is assigned to exactly one consultant
for i in range(I):
    problem += pulp.lpSum(y[(i, j)] for j in range(J)) == 1

# A consultant can only be assigned projects if they are hired
for i in range(I):
    for j in range(J):
        problem += y[(i, j)] <= x[j]

# Each consultant can be assigned at most K projects
for j in range(J):
    problem += pulp.lpSum(y[(i, j)] for i in range(I)) <= K * x[j]

# Solve the problem
problem.solve()

# Output the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')