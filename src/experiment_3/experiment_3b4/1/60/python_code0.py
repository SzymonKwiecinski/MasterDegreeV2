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

# Indices
I = range(len(additional_costs))  # Projects
J = range(len(fixed_costs))       # Consultants

# Create the problem
problem = pulp.LpProblem("Consultant_Project_Assignment", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in I for j in J), cat='Binary')
y = pulp.LpVariable.dicts("y", (j for j in J), cat='Binary')

# Objective Function
problem += (
    pulp.lpSum(fixed_costs[j] * y[j] for j in J) +
    pulp.lpSum(additional_costs[i][j] * x[(i, j)] for i in I for j in J)
), "Total Cost"

# Constraints

# Each project must be assigned to exactly one consultant
for i in I:
    problem += (
        pulp.lpSum(x[(i, j)] for j in J) == 1
    ), f"Project_Assignment_{i}"

# A consultant must be hired before they are assigned any project
for i in I:
    for j in J:
        problem += (
            x[(i, j)] <= y[j]
        ), f"Consultant_Hired_{i}_{j}"

# A consultant can handle at most K projects
for j in J:
    problem += (
        pulp.lpSum(x[(i, j)] for i in I) <= max_projects_per_consultant * y[j]
    ), f"Max_Projects_{j}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')