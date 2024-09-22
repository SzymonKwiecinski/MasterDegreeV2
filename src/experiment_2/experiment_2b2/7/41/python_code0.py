import pulp

# Data
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
capacity = data['capacity']
sizes = data['size']
N = len(sizes)

# Problem
problem = pulp.LpProblem("Floppy_Distribution_Problem", pulp.LpMinimize)

# Variables
# y[i] = 1 if disk i is used
y = [pulp.LpVariable(f'y_{i}', cat='Binary') for i in range(N)]

# x[j][i] = 1 if file j is on disk i
x = [[pulp.LpVariable(f'x_{j}_{i}', cat='Binary') for i in range(N)] for j in range(N)]

# Objective: Minimize the number of disks used
problem += pulp.lpSum(y), "Minimize_Disks_Used"

# Constraints
# Each file must be on exactly one disk
for j in range(N):
    problem += pulp.lpSum(x[j][i] for i in range(N)) == 1, f"File_{j}_on_One_Disk"

# Capacity constraints for each disk
for i in range(N):
    problem += pulp.lpSum(sizes[j] * x[j][i] for j in range(N)) <= capacity * y[i], f"Capacity_Constraint_{i}"

# Solve the problem
problem.solve()

# Results
n_disks = int(pulp.value(pulp.lpSum(y)))
whichdisk = [None] * N

for j in range(N):
    for i in range(N):
        if pulp.value(x[j][i]) == 1:
            whichdisk[j] = i

# Output
output = {
    "n_disks": n_disks,
    "whichdisk": whichdisk
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')