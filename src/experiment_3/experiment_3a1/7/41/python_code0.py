import pulp
import json

# Data from the provided JSON format
data = json.loads("{'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}")

# Extracting parameters
C = data['capacity']
sizes = data['size']
N = len(sizes)
M = N  # Assume we can have at most N disks, one for each file as an initial upper bound

# Create the problem variable
problem = pulp.LpProblem("FloppyDiskBackupProblem", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(M) for j in range(N)), cat='Binary')
y = pulp.LpVariable.dicts("y", range(M), cat='Binary')

# Objective Function
problem += pulp.lpSum(y[i] for i in range(M)), "Minimize number of disks used"

# Constraints
# Each file must be assigned to exactly one disk
for j in range(N):
    problem += pulp.lpSum(x[i, j] for i in range(M)) == 1, f"OneDiskPerFile_{j}"

# Disk capacity constraint
for i in range(M):
    problem += pulp.lpSum(sizes[j] * x[i, j] for j in range(N)) <= C * y[i], f"DiskCapacity_{i}"

# Solve the problem
problem.solve()

# Output results
n_disks = sum(pulp.value(y[i]) for i in range(M))
which_disk = {(j: [i for i in range(M) if pulp.value(x[i, j]) == 1]) for j in range(N)}

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(f'Total number of disks used: {n_disks}')
print('Distribution of files across disks:', which_disk)