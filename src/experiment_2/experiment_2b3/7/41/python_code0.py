import pulp

# Input data
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}

# Extracting capacity and sizes
capacity = data['capacity']
sizes = data['size']
N = len(sizes)

# Define the problem
problem = pulp.LpProblem("Floppy_Disk_Backup", pulp.LpMinimize)

# Decision variables
# y[i] indicates if disk i is used
y = [pulp.LpVariable(f'y_{i}', cat='Binary') for i in range(N)]
# x[j][i] indicates if file j is stored in disk i
x = [[pulp.LpVariable(f'x_{j}_{i}', cat='Binary') for i in range(N)] for j in range(N)]

# Objective Function: Minimize the number of disks used
problem += pulp.lpSum(y[i] for i in range(N))

# Constraints
# Each file must be stored in exactly one disk
for j in range(N):
    problem += pulp.lpSum(x[j][i] for i in range(N)) == 1

# The total size of files on each disk should not exceed its capacity
for i in range(N):
    problem += pulp.lpSum(sizes[j] * x[j][i] for j in range(N)) <= capacity * y[i]

# Solve the problem
problem.solve()

# Retrieve results
n_disks = int(sum(y[i].varValue for i in range(N)))
whichdisk = [None] * N

for j in range(N):
    for i in range(N):
        if pulp.value(x[j][i]) == 1:
            whichdisk[j] = i + 1  # Assuming disk indexing starts from 1

# Output format
output = {
    "n_disks": n_disks,
    "whichdisk": whichdisk
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')