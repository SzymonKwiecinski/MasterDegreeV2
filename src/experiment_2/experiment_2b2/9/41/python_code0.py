import pulp

# Data
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
capacity = data['capacity']
sizes = data['size']
N = len(sizes)

# Maximum possible disks needed
max_disks = N

# Define the problem
problem = pulp.LpProblem("Minimize Number of Floppy Disks", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(max_disks) for j in range(N)), cat='Binary')
y = pulp.LpVariable.dicts("y", (i for i in range(max_disks)), cat='Binary')

# Objective: Minimize the number of disks used
problem += pulp.lpSum(y[i] for i in range(max_disks))

# Constraints
# Each file must be assigned to exactly one disk
for j in range(N):
    problem += pulp.lpSum(x[i, j] for i in range(max_disks)) == 1

# The sum of files sizes on each disk cannot exceed its capacity
for i in range(max_disks):
    problem += pulp.lpSum(sizes[j] * x[i, j] for j in range(N)) <= capacity * y[i]

# Solve the problem
problem.solve()

# Collect results
n_disks = int(pulp.value(pulp.lpSum(y[i] for i in range(max_disks))))
whichdisk = [-1] * N

# Determine which disk each file is placed on
for j in range(N):
    for i in range(max_disks):
        if pulp.value(x[i, j]) == 1:
            whichdisk[j] = i
            break

# Output the results
output = {
    "n_disks": n_disks,
    "whichdisk": whichdisk
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')