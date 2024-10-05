import pulp

# Parse the data
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
capacity = data['capacity']
sizes = data['size']
num_files = len(sizes)

# Create a problem variable
problem = pulp.LpProblem("FloppyDiskBackup", pulp.LpMinimize)

# Decision variables
# x[i][j] = 1 if file j is assigned to disk i, else 0
max_disks = num_files  # upper bound on the number of disks needed
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(max_disks) for j in range(num_files)), cat='Binary')

# y[i] = 1 if disk i is used, else 0
y = pulp.LpVariable.dicts("y", (i for i in range(max_disks)), cat='Binary')

# Objective function: minimize the number of disks used
problem += pulp.lpSum(y[i] for i in range(max_disks))

# Constraints
# Each file must be assigned to exactly one disk
for j in range(num_files):
    problem += pulp.lpSum(x[i, j] for i in range(max_disks)) == 1

# The total size of files on each disk cannot exceed the disk capacity
for i in range(max_disks):
    problem += pulp.lpSum(sizes[j] * x[i, j] for j in range(num_files)) <= capacity * y[i]

# Solve the problem
problem.solve()

# Extract results
n_disks = sum(y[i].varValue for i in range(max_disks))
whichdisk = [-1] * num_files
for j in range(num_files):
    for i in range(max_disks):
        if pulp.value(x[(i, j)]) == 1:
            whichdisk[j] = i
            break

results = {
    "n_disks": int(n_disks),
    "whichdisk": whichdisk
}

print(results)
print(f" (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")