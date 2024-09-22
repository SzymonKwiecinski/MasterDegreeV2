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

# Extract data
fixed_costs = data['fixed_costs']
additional_costs = data['additional_costs']
K = data['max_projects_per_consultant']

# Sets
projects = range(len(additional_costs))
consultants = range(len(fixed_costs))

# Problem
problem = pulp.LpProblem("ConsultantAssignment", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", [(i, j) for i in projects for j in consultants], cat='Binary')
y = pulp.LpVariable.dicts("y", consultants, cat='Binary')

# Objective Function
problem += pulp.lpSum(fixed_costs[j] * y[j] for j in consultants) + \
           pulp.lpSum(additional_costs[i][j] * x[(i, j)] for i in projects for j in consultants)

# Constraints

# 1. Each project is assigned to exactly one consultant
for i in projects:
    problem += pulp.lpSum(x[(i, j)] for j in consultants) == 1

# 2. A consultant is not assigned more than K projects
for j in consultants:
    problem += pulp.lpSum(x[(i, j)] for i in projects) <= K

# 3. A project is assigned to a consultant only if they are hired
for i in projects:
    for j in consultants:
        problem += x[(i, j)] <= y[j]

# Solve
problem.solve()

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')