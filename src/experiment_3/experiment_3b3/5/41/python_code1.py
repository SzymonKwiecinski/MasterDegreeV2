import pulp

# Data
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
C = data['capacity']
file_sizes = data['size']
N = len(file_sizes)

# Problem
problem = pulp.LpProblem("FloppyDiskBackup", pulp.LpMinimize)

# Variables
# We will create a large enough upper bound for the number of disks
upper_bound_disks = int(sum(file_sizes) // C) + 1  # Ensure this is an integer
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(upper_bound_disks) for j in range(N)), cat='Binary')
n_disks = pulp.LpVariable('n_disks', lowBound=1, cat='Integer')

# Objective Function
problem += n_disks

# Constraints
# Each file must be assigned to exactly one disk
for j in range(N):
    problem += pulp.lpSum(x[i, j] for i in range(upper_bound_disks)) == 1

# Disk capacity constraints
for i in range(upper_bound_disks):
    problem += pulp.lpSum(file_sizes[j] * x[i, j] for j in range(N)) <= C

# Setting n_disks as the max index with any file assigned
for i in range(upper_bound_disks):
    problem += pulp.lpSum(x[i, j] for j in range(N)) <= n_disks

# Solve the problem
problem.solve()

# Results
whichdisk = [-1] * N
for j in range(N):
    for i in range(upper_bound_disks):
        if pulp.value(x[i, j]) == 1:
            whichdisk[j] = i + 1  # Disk indices start from 1
            break

print("Total number of floppy disks used:", pulp.value(n_disks))
print("Disk assignments for each file:", whichdisk)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')