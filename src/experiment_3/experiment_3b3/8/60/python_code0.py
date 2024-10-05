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

# Sets
I = range(len(data['additional_costs']))  # Projects
J = range(len(data['fixed_costs']))       # Consultants

# Parameters
f = data['fixed_costs']
c = data['additional_costs']
K = data['max_projects_per_consultant']

# Problem
problem = pulp.LpProblem("Consultant_Assignment", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("Hire", J, cat=pulp.LpBinary)
assignment = pulp.LpVariable.dicts("Assign", ((j, i) for j in J for i in I), cat=pulp.LpBinary)

# Objective Function
problem += pulp.lpSum(f[j] * x[j] for j in J) + pulp.lpSum(c[i][j] * assignment[j, i] for i in I for j in J)

# Constraints
# Each project assigned to at most one consultant
for i in I:
    problem += pulp.lpSum(assignment[j, i] for j in J) <= 1

# Each consultant assigned to maximum K projects
for j in J:
    problem += pulp.lpSum(assignment[j, i] for i in I) <= K * x[j]

# A project only assigned if consultant is hired
for i in I:
    for j in J:
        problem += assignment[j, i] <= x[j]

# Solve the problem
problem.solve()

# Output the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')