import pulp

# Data
fixed_costs = [100, 150, 135]
additional_costs = [
    [10, 12, 20],
    [10, 8, 12],
    [15, 8, 20],
    [10, 6, 15],
    [8, 10, 15]
]
max_projects_per_consultant = 3

# Sets
I = range(len(additional_costs))  # Projects
J = range(len(fixed_costs))       # Consultants

# Create the LP problem
problem = pulp.LpProblem("Consultant_Assignment_Problem", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", J, cat='Binary')  # Binary hire decision for each consultant
y = pulp.LpVariable.dicts("y", (I, J), cat='Binary')  # Binary assignment for each project to consultants

# Objective Function
problem += pulp.lpSum([fixed_costs[j] * x[j] for j in J]) + \
           pulp.lpSum([additional_costs[i][j] * y[i][j] for i in I for j in J]), "Total Cost"

# Constraints
# Each project must be assigned to exactly one consultant
for i in I:
    problem += pulp.lpSum([y[i][j] for j in J]) == 1, f"Project_Assignment_{i}"

# The number of projects assigned to each consultant cannot exceed max_projects_per_consultant
for j in J:
    problem += pulp.lpSum([y[i][j] for i in I]) <= max_projects_per_consultant * x[j], f"Max_Projects_{j}"

# Solve the problem
problem.solve()

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')