import pulp
import json

# Input data
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
capacity = data['capacity']
sizes = data['size']
N = len(sizes)

# Problem definition
problem = pulp.LpProblem("FloppyDiskPacking", pulp.LpMinimize)

# Decision Variables
# x[i][j] is 1 if file j is placed on disk i, 0 otherwise
x = pulp.LpVariable.dicts("x", (range(N), range(N)), cat='Binary')

# Objective Function: Minimize the number of disks used
n_disks = pulp.LpVariable("n_disks", lowBound=0, cat='Integer')
problem += n_disks

# Constraints: Each file should be assigned to exactly one disk
for j in range(N):
    problem += pulp.lpSum(x[i][j] for i in range(N)) == 1

# Constraints: The sum of sizes in each disk cannot exceed its capacity
for i in range(N):
    problem += pulp.lpSum(sizes[j] * x[i][j] for j in range(N)) <= capacity

# Constraints to ensure that n_disks accurately represents the number of used disks
for i in range(N):
    problem += pulp.lpSum(x[i][j] for j in range(N)) <= n_disks

# Solve the problem
problem.solve()

# Prepare the output
n_disks_value = int(pulp.value(n_disks))
whichdisk = [-1] * N  # Initialize with -1 (denote unassigned)

for j in range(N):
    for i in range(N):
        if pulp.value(x[i][j]) == 1:
            whichdisk[j] = i
            break

# Output format
output = {
    "n_disks": n_disks_value,
    "whichdisk": whichdisk
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')