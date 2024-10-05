import pulp

# Input Data
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
capacity = data['capacity']
sizes = data['size']
N = len(sizes)

# MILP Model
problem = pulp.LpProblem("FloppyDiskBackup", pulp.LpMinimize)

# Variables: x[i][j] is 1 if file i is stored on disk j, otherwise 0
x = [[pulp.LpVariable(f"x_{i}_{j}", cat='Binary') for j in range(N)] for i in range(N)]

# Variable: y[j] is 1 if disk j is used, otherwise 0
y = [pulp.LpVariable(f"y_{j}", cat='Binary') for j in range(N)]

# Objective: Minimize the number of disks used
problem += pulp.lpSum(y)

# Constraints: Each file must be on exactly one disk
for i in range(N):
    problem += pulp.lpSum(x[i][j] for j in range(N)) == 1

# Constraints: Disk capacity
for j in range(N):
    problem += pulp.lpSum(sizes[i] * x[i][j] for i in range(N)) <= capacity * y[j]

# Solve the problem
problem.solve()

# Extract the results
n_disks = int(sum(y[j].varValue for j in range(N)))
whichdisk = [j for i in range(N) for j in range(N) if x[i][j].varValue == 1]

# Output
result = {
    "n_disks": n_disks,
    "whichdisk": whichdisk
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')