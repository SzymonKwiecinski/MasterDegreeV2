import pulp
import json

# Data
data = json.loads('{"capacity": 3, "size": [1, 2, 0.5, 1.5, 2.5]}')
C = data['capacity']
sizes = data['size']
N = len(sizes)

# Create the problem
problem = pulp.LpProblem("FloppyDiskBackup", pulp.LpMinimize)

# Decision Variables
M = N  # The number of disks is initially set to the number of files
d = pulp.LpVariable.dicts("d", range(M), cat='Binary')
x = pulp.LpVariable.dicts("x", (range(N), range(M)), cat='Binary')

# Objective Function
problem += pulp.lpSum(d[k] for k in range(M)), "MinimizeTotalDisks"

# Constraints
# Each file must be assigned to exactly one disk
for j in range(N):
    problem += pulp.lpSum(x[j][k] for k in range(M)) == 1, f"FileAssignment_{j}"

# The total size of the files assigned to a disk cannot exceed its capacity
for k in range(M):
    problem += pulp.lpSum(sizes[j] * x[j][k] for j in range(N)) <= C * d[k], f"DiskCapacity_{k}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')