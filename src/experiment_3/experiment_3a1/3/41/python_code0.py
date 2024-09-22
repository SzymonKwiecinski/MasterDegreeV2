import pulp

# Data from the provided JSON format
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
C = data['capacity']
sizes = data['size']
N = len(sizes)

# Create the problem variable
problem = pulp.LpProblem("FloppyDiskBackupProblem", pulp.LpMinimize)

# Create decision variables
n_disks = pulp.LpVariable("n_disks", lowBound=1, cat='Integer')  # total number of disks used
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(N) for j in range(N)), cat='Binary')  # assignment variables

# Objective function: Minimize n_disks
problem += n_disks, "Minimize number of disks"

# Constraints
# Each file can only be assigned to one disk
for j in range(N):
    problem += pulp.lpSum(x[i, j] for i in range(N)) == 1, f"File_{j}_assignment"

# The total size of files assigned to each disk cannot exceed its capacity
for i in range(N):
    problem += pulp.lpSum(sizes[j] * x[i, j] for j in range(N)) <= C, f"Disk_{i}_capacity"

# Solve the problem
problem.solve()

# Output the results
n_disks_used = pulp.value(problem.objective)
assignments = {j: i for i in range(N) for j in range(N) if pulp.value(x[i, j]) == 1}

print(f' (Objective Value): <OBJ>{n_disks_used}</OBJ>')
print("File assignments to disks:")
for j, i in assignments.items():
    print(f"File {j} is assigned to Disk {i + 1}")