import pulp
import json

# Load data
data_json = '{"capacity": 3, "size": [1, 2, 0.5, 1.5, 2.5]}'
data = json.loads(data_json)

# Problem parameters
C = data['capacity']
sizes = data['size']
N = len(sizes)

# Create the LP problem
problem = pulp.LpProblem("FloppyDiskBackup", pulp.LpMinimize)

# Variables
M = N  # Number of disks can be at most equal to number of files
x = pulp.LpVariable.dicts("x", (range(M), range(N)), cat='Binary')  # Binary variables for file assignment
y = pulp.LpVariable.dicts("y", range(M), cat='Binary')  # Binary variables for disk usage

# Objective function: Minimize the number of disks used
problem += pulp.lpSum(y[i] for i in range(M)), "MinimizeDisks"

# Constraints
# Each file must be assigned to exactly one disk
for j in range(N):
    problem += pulp.lpSum(x[i][j] for i in range(M)) == 1, f"AssignFile_{j}"

# The total size on each disk cannot exceed its capacity
for i in range(M):
    problem += pulp.lpSum(sizes[j] * x[i][j] for j in range(N)) <= C * y[i], f"DiskCapacity_{i}"

# Solve the problem
problem.solve()

# Output results
n_disks_used = sum(pulp.value(y[i]) for i in range(M))
which_disk = [None] * N

for j in range(N):
    for i in range(M):
        if pulp.value(x[i][j]) == 1:
            which_disk[j] = i
            break

print(f' (Objective Value): <OBJ>{n_disks_used}</OBJ>')
print(f'whichdisk: {which_disk}')