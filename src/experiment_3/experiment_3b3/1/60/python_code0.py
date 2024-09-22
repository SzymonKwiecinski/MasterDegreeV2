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

# Unpack data
f = data['fixed_costs']
c = data['additional_costs']
K = data['max_projects_per_consultant']

# Dimensions
I = len(c)  # Number of projects
J = len(f)  # Number of consultants

# Problem
problem = pulp.LpProblem("ConsultantAssignment", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts('x', ((j, i) for j in range(J) for i in range(I)), cat='Binary')
y = pulp.LpVariable.dicts('y', (j for j in range(J)), cat='Binary')

# Objective function
problem += pulp.lpSum(f[j] * y[j] for j in range(J)) + pulp.lpSum(c[i][j] * x[(j, i)] for i in range(I) for j in range(J))

# Constraints
# Each project must be assigned to exactly one consultant
for i in range(I):
    problem += pulp.lpSum(x[(j, i)] for j in range(J)) == 1

# A consultant can only take on up to K projects
for j in range(J):
    problem += pulp.lpSum(x[(j, i)] for i in range(I)) <= K * y[j]

# Solve the problem
problem.solve()

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Assignments matrix
assignments = [[int(x[(j, i)].varValue) for i in range(I)] for j in range(J)]

# Print assignments
for j in range(J):
    for i in range(I):
        print(f'Consultant {j} assigned to Project {i}: {assignments[j][i]}')

# Show total cost
print(f'Total Cost: {pulp.value(problem.objective)}')