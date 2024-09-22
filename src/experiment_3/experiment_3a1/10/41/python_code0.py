import pulp

# Data
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
C = data['capacity']
sizes = data['size']
N = len(sizes)
M = N  # Assuming the number of disks at most equals the number of files

# Create the problem
problem = pulp.LpProblem("File_Distribution", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(M) for j in range(N)), cat='Binary')
y = pulp.LpVariable.dicts("y", range(M), cat='Binary')

# Objective Function
problem += pulp.lpSum(y[i] for i in range(M)), "Total_Disks_Used"

# Constraints

# 1. Each file must be assigned to exactly one disk
for j in range(N):
    problem += pulp.lpSum(x[i, j] for i in range(M)) == 1, f"Assign_one_disk_for_file_{j}"

# 2. The total size of files on each disk must not exceed its capacity
for i in range(M):
    problem += pulp.lpSum(sizes[j] * x[i, j] for j in range(N)) <= C * y[i], f"Capacity_constraint_for_disk_{i}"

# 3. A disk can only be used if at least one file is assigned to it
for i in range(M):
    problem += pulp.lpSum(x[i, j] for j in range(N)) <= M * y[i], f"Disk_usage_constraint_{i}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')