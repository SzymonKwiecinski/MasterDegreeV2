import pulp

# Data
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
C = data['capacity']
sizes = data['size']
N = len(sizes)

# Create the linear programming problem
problem = pulp.LpProblem("Disk_Packing", pulp.LpMinimize)

# Decision Variables
# Binary variable x[i][j]: 1 if file j is placed on disk i
x = pulp.LpVariable.dicts("x", (range(N), range(N)), cat='Binary')

# Binary variable y[i]: 1 if disk i is used
y = pulp.LpVariable.dicts("y", range(N), cat='Binary')

# Objective Function
problem += pulp.lpSum(y[i] for i in range(N)), "MinimizeDisksUsed"

# Constraints
# Each file must be assigned to exactly one disk
for j in range(N):
    problem += pulp.lpSum(x[i][j] for i in range(N)) == 1, f"FileAssignment_{j}"

# The total size of files assigned to each disk cannot exceed its capacity
for i in range(N):
    problem += pulp.lpSum(sizes[j] * x[i][j] for j in range(N)) <= C * y[i], f"DiskCapacity_{i}"

# Solve the problem
problem.solve()

# Output the total number of disks used
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')