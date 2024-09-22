import pulp

# Data from the JSON
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
I = range(len(data['additional_costs']))  # Set of projects
J = range(len(data['fixed_costs']))       # Set of consultants

# Parameters
f_j = data['fixed_costs']
c_ij = data['additional_costs']
K = data['max_projects_per_consultant']

# Problem
problem = pulp.LpProblem("Consultant_Assignment_Problem", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in I for j in J), cat='Binary')
y = pulp.LpVariable.dicts("y", (j for j in J), cat='Binary')

# Objective Function
problem += pulp.lpSum(f_j[j] * y[j] for j in J) + pulp.lpSum(c_ij[i][j] * x[i, j] for i in I for j in J)

# Constraints
# Each project is assigned to exactly one consultant
for i in I:
    problem += pulp.lpSum(x[i, j] for j in J) == 1, f"One_Consultant_Per_Project_{i}"

# Each consultant is assigned up to K projects
for j in J:
    problem += pulp.lpSum(x[i, j] for i in I) <= K * y[j], f"Max_Projects_Per_Consultant_{j}"

# Projects assigned only if consultant is hired
for i in I:
    for j in J:
        problem += x[i, j] <= y[j], f"Assign_Project_Only_If_Hired_{i}_{j}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')