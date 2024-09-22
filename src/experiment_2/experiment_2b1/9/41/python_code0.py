import pulp
import json

# Input data
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
capacity = data['capacity']
sizes = data['size']
N = len(sizes)

# Create the problem
problem = pulp.LpProblem("FloppyDiskPacking", pulp.LpMinimize)

# Create binary decision variables for files and disks
x = pulp.LpVariable.dicts("file", (range(N), range(N)), cat='Binary')  # x[i][j] is 1 if file i is on disk j
y = pulp.LpVariable.dicts("disk", range(N), cat='Binary')  # y[j] is 1 if disk j is used

# Objective function: Minimize the number of disks used
problem += pulp.lpSum(y[j] for j in range(N)), "MinimizeNumberOfDisks"

# Constraints: Each file must be assigned to exactly one disk
for i in range(N):
    problem += pulp.lpSum(x[i][j] for j in range(N)) == 1, f"File_{i}_assigned"

# Constraints: The total size of files on each disk cannot exceed the capacity
for j in range(N):
    problem += pulp.lpSum(sizes[i] * x[i][j] for i in range(N)) <= capacity * y[j], f"Disk_{j}_capacity"

# Solve the problem
problem.solve()

# Gather results
n_disks = int(pulp.value(problem.objective))
whichdisk = [0] * N

for i in range(N):
    for j in range(N):
        if pulp.value(x[i][j]) == 1:
            whichdisk[i] = j + 1  # To make disk indices start from 1

# Prepare the output
output = {
    "n_disks": n_disks,
    "whichdisk": whichdisk
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')