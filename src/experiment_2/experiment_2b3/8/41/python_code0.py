import pulp

# Parse input data
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
capacity = data["capacity"]
sizes = data["size"]
N = len(sizes)  # Number of files

# Create decision variables
# x[i][j] = 1 if file j is placed on disk i, 0 otherwise
# y[i] = 1 if disk i is used, 0 otherwise
max_disks = N  # At most one disk per file initially
x = pulp.LpVariable.dicts("x", (range(max_disks), range(N)), cat='Binary')
y = pulp.LpVariable.dicts("y", range(max_disks), cat='Binary')

# Define the problem
problem = pulp.LpProblem("FloppyDiskBackup", pulp.LpMinimize)

# Objective function: minimize the number of used disks
problem += pulp.lpSum(y[i] for i in range(max_disks))

# Constraints
# Each file must be placed on exactly one disk
for j in range(N):
    problem += pulp.lpSum(x[i][j] for i in range(max_disks)) == 1

# The total size of files on each disk cannot exceed its capacity
for i in range(max_disks):
    problem += pulp.lpSum(x[i][j] * sizes[j] for j in range(N)) <= capacity * y[i]

# Solve the problem
result = problem.solve()

# Determine the number of disks used and which files go to which disk
whichdisk = [-1] * N
n_disks = sum(pulp.value(y[i]) for i in range(max_disks) if pulp.value(y[i]) == 1)
for j in range(N):
    for i in range(max_disks):
        if pulp.value(x[i][j]) == 1:
            whichdisk[j] = i
            break

# Output result
output = {
    "n_disks": int(n_disks),
    "whichdisk": whichdisk
}

print(output)
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')