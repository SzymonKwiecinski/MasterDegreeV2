import pulp

# Data
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}

capacity = data['capacity']
sizes = data['size']
N = len(sizes)

# Create the MILP problem
problem = pulp.LpProblem("Floppy_Disk_Minimization", pulp.LpMinimize)

# Variables
# x[i][j] = 1 if file j is placed on disk i, 0 otherwise
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(N) for j in range(N)), cat='Binary')

# y[i] = 1 if disk i is used, 0 otherwise
y = pulp.LpVariable.dicts("y", range(N), cat='Binary')

# Objective: minimize the number of disks used
problem += pulp.lpSum(y[i] for i in range(N))

# Constraints
# Each file must be placed on exactly one disk
for j in range(N):
    problem += pulp.lpSum(x[i, j] for i in range(N)) == 1

# The total size on each disk cannot exceed its capacity
for i in range(N):
    problem += pulp.lpSum(x[i, j] * sizes[j] for j in range(N)) <= capacity * y[i]

# Solve the problem
problem.solve()

# Extract results
n_disks = int(sum(y[i].varValue for i in range(N)))
whichdisk = [-1] * N
for j in range(N):
    for i in range(N):
        if pulp.value(x[i, j]) == 1:
            whichdisk[j] = i
            break

# Output
result = {
    "n_disks": n_disks,
    "whichdisk": whichdisk
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')