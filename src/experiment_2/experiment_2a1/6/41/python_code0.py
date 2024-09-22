import pulp
import json

# Input data
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
capacity = data['capacity']
sizes = data['size']
N = len(sizes)

# Create the problem
problem = pulp.LpProblem("FloppyDiskBackup", pulp.LpMinimize)

# Variables
n_disks = pulp.LpVariable("n_disks", lowBound=1, cat='Integer')
x = pulp.LpVariable.dicts("x", (range(N), range(N)), cat='Binary')

# Objective function: minimize the number of disks used
problem += n_disks

# Constraints: each file must be assigned to exactly one disk
for j in range(N):
    problem += pulp.lpSum(x[j][i] for i in range(N)) == 1

# Capacity constraints: the total size of files on each disk must not exceed capacity
for i in range(N):
    problem += pulp.lpSum(sizes[j] * x[j][i] for j in range(N)) <= capacity

# Link the number of disks to the x variables
for i in range(N):
    problem += pulp.lpSum(x[j][i] for j in range(N)) <= n_disks

# Solve the problem
problem.solve()

# Prepare output
n_disks_used = int(pulp.value(n_disks))
which_disk = [next(i for i in range(N) if pulp.value(x[j][i]) == 1) for j in range(N)]

# Output format
output = {
    "n_disks": n_disks_used,
    "whichdisk": which_disk
}

print(json.dumps(output))

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')