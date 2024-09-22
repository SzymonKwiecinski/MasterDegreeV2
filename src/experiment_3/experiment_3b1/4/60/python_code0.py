import pulp

# Data
data = {
    'fixed_costs': [100, 150, 135],
    'additional_costs': [[10, 12, 20], [10, 8, 12], [15, 8, 20], [10, 6, 15], [8, 10, 15]],
    'max_projects_per_consultant': 3
}

# Sets
I = range(len(data['additional_costs']))  # Projects
J = range(len(data['fixed_costs']))        # Consultants

# Parameters
f = data['fixed_costs']                         # Fixed costs
c = data['additional_costs']                     # Additional costs
K = data['max_projects_per_consultant']         # Max projects per consultant

# Problem definition
problem = pulp.LpProblem("Consultant_Assignment", pulp.LpMinimize)

# Variables
x = pulp.LpVariable.dicts("hire", J, cat='Binary')  # Hiring consultants
y = pulp.LpVariable.dicts("assign", (I, J), cat='Binary')  # Project assignment

# Objective function
problem += pulp.lpSum(f[j] * x[j] for j in J) + pulp.lpSum(c[i][j] * y[i][j] for i in I for j in J)

# Constraints
# Each project must be assigned to exactly one consultant
for i in I:
    problem += pulp.lpSum(y[i][j] for j in J) == 1

# A consultant can only take on projects if they are hired
for i in I:
    for j in J:
        problem += y[i][j] <= x[j]

# A consultant can handle at most K projects
for j in J:
    problem += pulp.lpSum(y[i][j] for i in I) <= K * x[j]

# Solve the problem
problem.solve()

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')