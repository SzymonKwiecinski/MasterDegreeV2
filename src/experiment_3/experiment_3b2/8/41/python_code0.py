import pulp

# Data from JSON
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
capacity = data['capacity']
sizes = data['size']
N = len(sizes)

# Define the problem
problem = pulp.LpProblem("Disk_Usage_Optimization", pulp.LpMinimize)

# Define variables
M = N  # The maximum number of disks we might need is at least the number of files
x = pulp.LpVariable.dicts("x", (range(M), range(N)), cat='Binary')
y = pulp.LpVariable.dicts("y", range(M), cat='Binary')

# Objective function: Minimize the number of disks used
problem += pulp.lpSum(y[i] for i in range(M)), "Minimize_Disks"

# Constraints
# Each file should be assigned to exactly one disk
for j in range(N):
    problem += pulp.lpSum(x[i][j] for i in range(M)) == 1, f"Assign_File_{j}"

# Capacity constraints for each disk
for i in range(M):
    problem += pulp.lpSum(sizes[j] * x[i][j] for j in range(N)) <= capacity * y[i], f"Capacity_Disk_{i}"

# Linking constraints: x_ij <= y_i
for i in range(M):
    for j in range(N):
        problem += x[i][j] <= y[i], f"Link_{i}_{j}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')