import pulp

# Data
fixed_costs = [100, 150, 135]  # Fixed costs for consultants
additional_costs = [[10, 12, 20], [10, 8, 12], [15, 8, 20], [10, 6, 15], [8, 10, 15]]  # Additional costs for projects
max_projects_per_consultant = 3  # Maximum projects per consultant

# Sets
I = range(len(additional_costs))  # Projects
J = range(len(fixed_costs))  # Consultants

# Create the problem
problem = pulp.LpProblem("Project Assignment Problem", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", J, cat='Binary')  # Consultant hired
a = pulp.LpVariable.dicts("a", (I, J), cat='Binary')  # Project i assigned to consultant j

# Objective Function
problem += pulp.lpSum([fixed_costs[j] * x[j] for j in J]) + \
           pulp.lpSum([additional_costs[i][j] * a[i][j] for i in I for j in J]), "Total Cost"

# Constraints
# Each project must be assigned to exactly one consultant
for i in I:
    problem += pulp.lpSum([a[i][j] for j in J]) == 1, f"Project_Assignment_{i}"

# A consultant can only assign projects if they are hired
for i in I:
    for j in J:
        problem += a[i][j] <= x[j], f"Consultant_Hired_{i}_{j}"

# Each consultant can be assigned a maximum of K projects
for j in J:
    problem += pulp.lpSum([a[i][j] for i in I]) <= max_projects_per_consultant * x[j], f"Max_Projects_Consultant_{j}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')