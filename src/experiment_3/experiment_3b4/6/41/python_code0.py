import pulp

# Data from the JSON input
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
capacity = data['capacity']
sizes = data['size']
N = len(sizes)  # Number of files

# Create a linear programming problem
problem = pulp.LpProblem("FloppyDiskBackup", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", [(i, j) for i in range(N) for j in range(N)], cat='Binary')
y = pulp.LpVariable.dicts("y", [i for i in range(N)], cat='Binary')

# Objective function: Minimize the number of disks used
problem += pulp.lpSum(y[i] for i in range(N))

# Constraints

# Each file must be placed on exactly one disk
for j in range(N):
    problem += pulp.lpSum(x[i, j] for i in range(N)) == 1

# Total size of files on each disk cannot exceed the disk capacity
for i in range(N):
    problem += pulp.lpSum(sizes[j] * x[i, j] for j in range(N)) <= capacity * y[i]

# x_{ij} can only be 1 if y_i is 1
for i in range(N):
    for j in range(N):
        problem += x[i, j] <= y[i]

# Solve the problem
problem.solve()

# Output results
n_disks = sum(y[i].varValue for i in range(N))
whichdisk = [None] * N
for j in range(N):
    for i in range(N):
        if x[i, j].varValue == 1:
            whichdisk[j] = i
            break

print(f'Total number of floppy disks used: {int(n_disks)}')
print(f'Assignment of files to disks: {whichdisk}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')