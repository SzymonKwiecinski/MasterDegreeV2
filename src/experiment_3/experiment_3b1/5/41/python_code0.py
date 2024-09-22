import pulp
import json

# Load data from JSON format
data = json.loads('{"capacity": 3, "size": [1, 2, 0.5, 1.5, 2.5]}')
C = data['capacity']
file_sizes = data['size']
N = len(file_sizes)

# Initialize the problem
problem = pulp.LpProblem("Floppy_Disk_Backup_Problem", pulp.LpMinimize)

# Decision variables
# x[i][j] is 1 if file j is placed on disk i, else 0
x = pulp.LpVariable.dicts("x", (range(N), range(N)), cat='Binary')
# n is the total number of disks used
n = pulp.LpVariable("n", lowBound=1, cat='Integer')

# Objective function: Minimize the number of disks used
problem += n

# Constraints
# 1. Each file must be assigned to exactly one disk
for j in range(N):
    problem += pulp.lpSum(x[i][j] for i in range(N)) == 1

# 2. The total size of files on each disk must not exceed its capacity
for i in range(N):
    problem += pulp.lpSum(file_sizes[j] * x[i][j] for j in range(N)) <= C

# 3. The number of disks used should consider the number of assigned files
for i in range(N):
    problem += pulp.lpSum(x[i][j] for j in range(N)) <= n

# Solve the problem
problem.solve()

# Collect results
n_disks = n.varValue
which_disk = [0] * N
for j in range(N):
    for i in range(N):
        if pulp.value(x[i][j]) == 1:
            which_disk[j] = i + 1  # +1 to convert to 1-indexed

# Print objective
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')