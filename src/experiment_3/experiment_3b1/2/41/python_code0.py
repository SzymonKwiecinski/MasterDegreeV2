import pulp
import json

# Data provided in JSON format
data = '{"capacity": 3, "size": [1, 2, 0.5, 1.5, 2.5]}'
data = json.loads(data)

# Parameters
C = data['capacity']
sizes = data['size']
N = len(sizes)

# Problem definition
problem = pulp.LpProblem("FloppyDiskBackup", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", (range(N), range(N)), cat='Binary')
y = pulp.LpVariable.dicts("y", range(N), cat='Binary')

# Objective function
problem += pulp.lpSum(y[i] for i in range(N)), "MinimizeDisks"

# Constraints
# Each file must be assigned to exactly one disk
for j in range(N):
    problem += pulp.lpSum(x[i][j] for i in range(N)) == 1, f"AssignFile_{j}"

# The total size of files on each disk cannot exceed its capacity
for i in range(N):
    problem += pulp.lpSum(sizes[j] * x[i][j] for j in range(N)) <= C * y[i], f"CapacityDisk_{i}"

# The number of disks used should be equal to the sum of used disks
problem += pulp.lpSum(y[i] for i in range(N)) == pulp.lpSum(y[i] for i in range(N)), "CountDisks"

# Solve the problem
problem.solve()

# Output results
n_disks = int(pulp.value(problem.objective))
which_disk = {j: [i for i in range(N) if pulp.value(x[i][j]) == 1] for j in range(N)}

print(f' (Objective Value): <OBJ>{n_disks}</OBJ>')
print(f' (Which Disk): {which_disk}')