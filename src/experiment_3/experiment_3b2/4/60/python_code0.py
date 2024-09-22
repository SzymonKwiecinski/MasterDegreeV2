import pulp

# Data input
data = {
    'fixed_costs': [100, 150, 135],
    'additional_costs': [[10, 12, 20], [10, 8, 12], [15, 8, 20], [10, 6, 15], [8, 10, 15]],
    'max_projects_per_consultant': 3
}

# Sets and indices
I = range(len(data['additional_costs']))  # Projects
J = range(len(data['fixed_costs']))       # Consultants

# Parameters
f = data['fixed_costs']                              # Fixed costs
c = data['additional_costs']                         # Additional costs
K = data['max_projects_per_consultant']              # Maximum projects per consultant

# Decision Variables
x = pulp.LpVariable.dicts("x", (I, J), cat='Binary')  # Project assignment variables
y = pulp.LpVariable.dicts("y", J, cat='Binary')       # Consultant hiring variables

# Problem definition
problem = pulp.LpProblem("Consultant_Allocation_Problem", pulp.LpMinimize)

# Objective Function
problem += (pulp.lpSum(f[j] * y[j] for j in J) + 
            pulp.lpSum(c[i][j] * x[i][j] for i in I for j in J))

# Constraints
# Each project is assigned to exactly one consultant
for i in I:
    problem += pulp.lpSum(x[i][j] for j in J) == 1

# Limit the number of projects per consultant
for j in J:
    problem += pulp.lpSum(x[i][j] for i in I) <= K * y[j]

# Project can only be assigned if the consultant is hired
for i in I:
    for j in J:
        problem += x[i][j] <= y[j]

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')