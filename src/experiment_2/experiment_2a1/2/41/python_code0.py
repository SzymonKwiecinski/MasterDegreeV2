import pulp
import json

# Input data
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
capacity = data['capacity']
file_sizes = data['size']
N = len(file_sizes)

# Create the linear programming problem
problem = pulp.LpProblem("Minimize_Floppy_Disks", pulp.LpMinimize)

# Variables: x[i][j] = 1 if file j is on disk i, 0 otherwise
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(N) for j in range(N)), cat='Binary')

# Objective: Minimize the number of disks used
n_disks = pulp.LpVariable("n_disks", lowBound=0, cat='Integer')
problem += n_disks

# Constraints: Each file must be assigned to exactly one disk
for j in range(N):
    problem += pulp.lpSum(x[i, j] for i in range(N)) == 1

# Constraints: Disk i cannot exceed capacity
for i in range(N):
    problem += pulp.lpSum(file_sizes[j] * x[i, j] for j in range(N)) <= capacity

# Constraints to ensure n_disks is at least the number of disks used
for i in range(N):
    problem += pulp.lpSum(x[i, j] for j in range(N)) <= n_disks

# Solve the problem
problem.solve()

# Output the results
n_disks_used = int(pulp.value(n_disks))
whichdisk = [next(i for i in range(N) if pulp.value(x[i, j]) == 1) for j in range(N)]

# Preparing output format
output = {
    "n_disks": n_disks_used,
    "whichdisk": whichdisk
}

print(json.dumps(output))

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')