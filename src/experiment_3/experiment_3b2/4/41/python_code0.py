import pulp
import json

# Given data
data = json.loads('{"capacity": 3, "size": [1, 2, 0.5, 1.5, 2.5]}')
capacity = data['capacity']
sizes = data['size']
N = len(sizes)
M = N  # Upper bound on the number of disks

# Create the problem
problem = pulp.LpProblem("Floppy_Disk_Backup", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", (range(M), range(N)), cat='Binary')  # x[i][j]
y = pulp.LpVariable.dicts("y", range(M), cat='Binary')              # y[i]

# Objective Function
problem += pulp.lpSum(y[i] for i in range(M)), "Minimize_Disks_Used"

# Constraints
# Each file must be stored on exactly one disk
for j in range(N):
    problem += pulp.lpSum(x[i][j] for i in range(M)) == 1, f"File_{j+1}_Storage"

# Disk capacity constraints for each disk
for i in range(M):
    problem += pulp.lpSum(sizes[j] * x[i][j] for j in range(N)) <= capacity * y[i], f"Disk_{i+1}_Capacity"

# Solve the problem
problem.solve()

# Output results
n_disks = sum(y[i].value() for i in range(M))
which_disk = [next(i for i in range(M) if x[i][j].value() == 1) for j in range(N)]

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(f'Number of disks used: {n_disks}')
print(f'Disk assignments: {which_disk}')