import pulp

# Data from the input
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}

# Parameters
capacity = data['capacity']
file_sizes = data['size']
N = len(file_sizes)  # Number of files

# Estimating the maximum number of disks needed
max_disks = N

# Problem
problem = pulp.LpProblem("MinimizeFloppyDisks", pulp.LpMinimize)

# Variables
# x[i][j] = 1 if file i is on disk j
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(N) for j in range(max_disks)), cat='Binary')

# y[j] = 1 if disk j is used
y = pulp.LpVariable.dicts("y", (j for j in range(max_disks)), cat='Binary')

# Objective function: Minimize the number of disks used
problem += pulp.lpSum([y[j] for j in range(max_disks)])

# Constraints
# Each file must be on exactly one disk
for i in range(N):
    problem += pulp.lpSum([x[i, j] for j in range(max_disks)]) == 1

# Capacity constraint for each disk
for j in range(max_disks):
    problem += pulp.lpSum([file_sizes[i] * x[i, j] for i in range(N)]) <= capacity * y[j]

# Solve the problem
problem.solve()

# Determine the number of disks used and the disk distribution
n_disks = sum(pulp.value(y[j]) for j in range(max_disks))
whichdisk = [None] * N

for i in range(N):
    for j in range(max_disks):
        if pulp.value(x[i, j]) == 1:
            whichdisk[i] = j
            break

output = {
    "n_disks": int(n_disks),
    "whichdisk": whichdisk
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')