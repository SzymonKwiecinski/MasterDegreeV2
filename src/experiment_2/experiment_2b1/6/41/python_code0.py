import pulp
import json

# Data input
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
capacity = data['capacity']
file_sizes = data['size']
N = len(file_sizes)

# Problem definition
problem = pulp.LpProblem("FloppyDiskPacking", pulp.LpMinimize)

# Binary variables indicating if file j is on disk i
x = pulp.LpVariable.dicts("x", ((j, i) for j in range(N) for i in range(N)), cat='Binary')

# Variable for the number of disks used
n_disks = pulp.LpVariable("n_disks", lowBound=0, cat='Integer')

# Objective function: Minimize the number of disks used
problem += n_disks

# Constraints
# Each file must be placed on exactly one disk
for j in range(N):
    problem += pulp.lpSum(x[j, i] for i in range(N)) == 1

# Capacity constraints for each disk
for i in range(N):
    problem += pulp.lpSum(file_sizes[j] * x[j, i] for j in range(N)) <= capacity

# Constraints to ensure the number of disks used
for i in range(N):
    for j in range(N):
        problem += x[j, i] <= n_disks

# Solve the problem
problem.solve()

# Output result
n_disks_used = int(pulp.value(n_disks))
whichdisk = [next(i for i in range(n_disks_used) if pulp.value(x[j, i]) == 1) for j in range(N)]

result = {
    "n_disks": n_disks_used,
    "whichdisk": whichdisk
}

print(json.dumps(result))

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')