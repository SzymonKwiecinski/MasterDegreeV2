import pulp
import json

# Input data
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
capacity = data['capacity']
file_sizes = data['size']
num_files = len(file_sizes)

# Create the LP problem
problem = pulp.LpProblem("FloppyDiskAllocation", pulp.LpMinimize)

# Decision variables
# x[i][j] = 1 if file i is placed on disk j, else 0
x = pulp.LpVariable.dicts("x", (range(num_files), range(num_files)), cat='Binary')

# Objective function: minimize the number of disks used
n_disks = pulp.LpVariable("n_disks", lowBound=0, cat='Integer')
problem += n_disks

# Constraints for each file
for i in range(num_files):
    problem += pulp.lpSum(x[i][j] for j in range(num_files)) == 1  # Each file must be on one disk

# Constraints for each disk capacity
for j in range(num_files):
    problem += pulp.lpSum(file_sizes[i] * x[i][j] for i in range(num_files)) <= capacity  # Capacity constraint

# Add a constraint to limit the number of disks used
for j in range(num_files):
    for i in range(num_files):
        problem += x[i][j] <= n_disks  # If a file is placed on disk j, it counts against the n_disks

# Solve the problem
problem.solve()

# Prepare output
n_disks_value = int(pulp.value(n_disks))
whichdisk = [0] * num_files
for i in range(num_files):
    for j in range(num_files):
        if pulp.value(x[i][j]) == 1:
            whichdisk[i] = j + 1  # +1 to make disks 1-indexed

# Print results
output = {
    "n_disks": n_disks_value,
    "whichdisk": whichdisk
}
print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')