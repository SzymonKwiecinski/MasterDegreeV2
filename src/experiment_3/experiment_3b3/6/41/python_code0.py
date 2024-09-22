import pulp

# Data
data = {
    'capacity': 3,
    'size': [1, 2, 0.5, 1.5, 2.5]
}

C = data['capacity']
sizes = data['size']
N = len(sizes)
M = N  # Maximum number of disks (one file per disk if needed)

# Problem
problem = pulp.LpProblem("Floppy_Disk_Backup", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(M) for j in range(N)), 
                          cat='Binary')
y = pulp.LpVariable.dicts("y", (i for i in range(M)), cat='Binary')

# Objective Function
problem += pulp.lpSum(y[i] for i in range(M)), "Minimize_Number_of_Disks"

# Constraints
# Each file must be assigned to exactly one disk
for j in range(N):
    problem += pulp.lpSum(x[i, j] for i in range(M)) == 1, f"File_{j+1}_Assigned"

# Disk capacity constraints
for i in range(M):
    problem += pulp.lpSum(sizes[j] * x[i, j] for j in range(N)) <= C * y[i], f"Disk_{i+1}_Capacity"

# Ensure a disk is only used if at least one file is assigned to it
for i in range(M):
    for j in range(N):
        problem += x[i, j] <= y[i], f"Disk_{i+1}_File_{j+1}_Usage"

# Solve the problem
problem.solve()

# Output
n_disks = sum(pulp.value(y[i]) for i in range(M))
which_disk = [i for j in range(N) for i in range(M) if pulp.value(x[i, j]) == 1]

print(f'Total Disks Used: {n_disks}')
for j in range(N):
    print(f'File {j+1} is on disk {which_disk[j] + 1}')

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')