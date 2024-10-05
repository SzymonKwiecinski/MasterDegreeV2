import pulp

# Extract the data from JSON
data = {
    'fixed_costs': [100, 150, 135],
    'additional_costs': [[10, 12, 20], [10, 8, 12], [15, 8, 20], [10, 6, 15], [8, 10, 15]],
    'max_projects_per_consultant': 3
}

fixed_costs = data['fixed_costs']
additional_costs = data['additional_costs']
K = data['max_projects_per_consultant']

# Indices
I = range(len(additional_costs))  # Projects
J = range(len(fixed_costs))  # Consultants

# Problem
problem = pulp.LpProblem("ConsultantAssignment", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in I for j in J), cat='Binary')
y = pulp.LpVariable.dicts("y", J, cat='Binary')

# Objective function
problem += pulp.lpSum(fixed_costs[j] * y[j] for j in J) + \
           pulp.lpSum(additional_costs[i][j] * x[i, j] for i in I for j in J)

# Constraints
# Each project is assigned to exactly one consultant
for i in I:
    problem += pulp.lpSum(x[i, j] for j in J) == 1

# A project can only be assigned to a hired consultant
for i in I:
    for j in J:
        problem += x[i, j] <= y[j]

# Limit the number of projects per consultant
for j in J:
    problem += pulp.lpSum(x[i, j] for i in I) <= K * y[j]

# Solve the problem
problem.solve()

# Output the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')