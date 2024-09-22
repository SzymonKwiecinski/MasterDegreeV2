import pulp

# Data
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
C = data['capacity']
sizes = data['size']
N = len(sizes)

# Create the problem
problem = pulp.LpProblem("FloppyDiskBackup", pulp.LpMinimize)

# Decision Variables
n_disks = pulp.LpVariable("n_disks", lowBound=0, cat='Integer')
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(N) for j in range(N)), cat='Binary')

# Objective Function
problem += n_disks, "MinimizeNumberOfDisks"

# Constraints
# Each file must be stored on exactly one disk
for j in range(N):
    problem += pulp.lpSum(x[i, j] for i in range(N)) == 1, f"FileAssignment_{j}"

# Total size of files on each disk cannot exceed its capacity
for i in range(N):
    problem += pulp.lpSum(sizes[j] * x[i, j] for j in range(N)) <= C, f"DiskCapacity_{i}"

# Number of disks must be greater than or equal to the number of files assigned
for j in range(N):
    problem += n_disks >= pulp.lpSum(x[i, j] for i in range(N)), f"DiskCountRequirement_{j}"

# Solve the problem
problem.solve()

# Output the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
for j in range(N):
    for i in range(N):
        if pulp.value(x[i, j]) == 1:
            print(f'File {j+1} is stored on Disk {i+1}')