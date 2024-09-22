import pulp

# Data
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
capacity = data['capacity']
sizes = data['size']
num_files = len(sizes)

# Problem
problem = pulp.LpProblem("Minimum_Disks_Backup", pulp.LpMinimize)

# Variables
n_disks = pulp.LpVariable('n_disks', lowBound=0, cat='Integer')
assignments = pulp.LpVariable.dicts('disk_assign', ((i, j) for i in range(num_files) for j in range(num_files)), cat='Binary')
disks_used = pulp.LpVariable.dicts('disk_used', (j for j in range(num_files)), cat='Binary')

# Objective
problem += n_disks

# Constraints
for i in range(num_files):
    problem += pulp.lpSum(assignments[i, j] for j in range(num_files)) == 1

for j in range(num_files):
    problem += pulp.lpSum(assignments[i, j] * sizes[i] for i in range(num_files)) <= capacity * disks_used[j]

problem += pulp.lpSum(disks_used[j] for j in range(num_files)) == n_disks

# Solve
problem.solve()

# Extract solution
n_disks_value = int(pulp.value(n_disks))
whichdisk = [-1] * num_files

disk_indices = [j for j in range(num_files) if pulp.value(disks_used[j]) > 0.5]

for i in range(num_files):
    for j in disk_indices:
        if pulp.value(assignments[i, j]) > 0.5:
            whichdisk[i] = disk_indices.index(j)
            break

# Output
result = {
    "n_disks": n_disks_value,
    "whichdisk": whichdisk
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')