import pulp

# Data
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
N = len(data['size'])  # Number of files
M = N  # Upper bound on the number of disks

# Problem definition
problem = pulp.LpProblem("FloppyDiskBackup", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", (range(M), range(N)), cat='Binary')  # x_ij
y = pulp.LpVariable.dicts("y", range(M), cat='Binary')  # y_i

# Objective Function
problem += pulp.lpSum(y[i] for i in range(M)), "Minimize_Disk_Usage"

# Constraints

# 1. Each file must be assigned to exactly one disk
for j in range(N):
    problem += pulp.lpSum(x[i][j] for i in range(M)) == 1, f"Assign_File_{j+1}"

# 2. Capacity constraint for each disk
for i in range(M):
    problem += pulp.lpSum(data['size'][j] * x[i][j] for j in range(N)) <= data['capacity'] * y[i], f"Capacity_Disk_{i+1}"

# 3. File assignment implies disk usage
for i in range(M):
    for j in range(N):
        problem += x[i][j] <= y[i], f"File_Assignment_Implices_Disk_Usage_{i+1}_{j+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')