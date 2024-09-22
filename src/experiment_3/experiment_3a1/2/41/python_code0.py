import pulp

# Data from the JSON format
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
capacity = data['capacity']
size = data['size']

# Sets
J = range(len(size))  # Set of files
D = range(len(size))  # Set of available disks (same as files for this problem)

# Create the problem
problem = pulp.LpProblem("FloppyDiskBackup", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", (D, J), cat='Binary')  # x[i][j]: 1 if file j is placed on disk i
y = pulp.LpVariable.dicts("y", D, cat='Binary')      # y[i]: 1 if disk i is used

# Objective Function: Minimize the number of disks used
problem += pulp.lpSum(y[i] for i in D), "TotalDisksUsed"

# Constraints

# Each file must be assigned to exactly one disk
for j in J:
    problem += pulp.lpSum(x[i][j] for i in D) == 1, f"FileAssignment_{j}"

# Capacity Constraint: Total size of files on each disk cannot exceed its capacity
for i in D:
    problem += (pulp.lpSum(size[j] * x[i][j] for j in J) <= capacity * y[i]), f"CapacityConstraint_{i}"

# Disk Utilization: A disk can only be used if it has at least one file
for i in D:
    for j in J:
        problem += (y[i] >= x[i][j]), f"DiskUtilization_{i}_{j}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')