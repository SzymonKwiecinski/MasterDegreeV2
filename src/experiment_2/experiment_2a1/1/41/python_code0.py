import pulp
import json

# Input data
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}

capacity = data['capacity']
sizes = data['size']
N = len(sizes)

# Create the problem
problem = pulp.LpProblem("FloppyDiskPacking", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("disk", range(N), cat='Binary')
y = pulp.LpVariable.dicts("used_disk", range(N), cat='Binary')

# Objective function: Minimize the number of disks used
problem += pulp.lpSum(y[d] for d in range(N)), "TotalDisksUsed"

# Constraints
for j in range(N):
    problem += pulp.lpSum(x[j] for d in range(N) if j < d) <= (1 * y[j]), f"File_Allocation_{j}"

for d in range(N):
    for j in range(N):
        problem += x[j] <= y[d], f"Assign_File_{j}_to_Disk_{d}"

# Capacity constraints
for d in range(N):
    problem += pulp.lpSum(sizes[j] * x[j] for j in range(N)) <= capacity * y[d], f"Capacity_Constraint_{d}"

# Solve the problem
problem.solve()

# Extract the results
n_disks = int(pulp.value(problem.objective))
whichdisk = [0] * N

for d in range(N):
    if pulp.value(y[d]) == 1:
        for j in range(N):
            if pulp.value(x[j]) == 1:
                whichdisk[j] = d + 1  # Disk numbers start from 1

# Output the results
output = {
    "n_disks": n_disks,
    "whichdisk": whichdisk
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')