import pulp
import json

# Data initialization
data = json.loads('{"capacity": 3, "size": [1, 2, 0.5, 1.5, 2.5]}')
C = data['capacity']  # capacity of each floppy disk
sizes = data['size']  # sizes of the files
N = len(sizes)  # number of files
M = 5  # Assuming 5 disks available

# Problem definition
problem = pulp.LpProblem("Disk_Packing_Problem", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", (range(M), range(N)), cat='Binary')  # x[i][j] = 1 if file j is on disk i
y = pulp.LpVariable.dicts("y", range(M), cat='Binary')  # y[i] = 1 if disk i is used

# Objective Function
problem += pulp.lpSum(y[i] for i in range(M)), "Minimize_Disks_Used"

# Constraints
# Each file must be assigned to exactly one disk
for j in range(N):
    problem += pulp.lpSum(x[i][j] for i in range(M)) == 1, f"File_{j+1}_Assigned"

# The total size of files on each disk cannot exceed its capacity
for i in range(M):
    problem += pulp.lpSum(sizes[j] * x[i][j] for j in range(N)) <= C * y[i], f"Capacity_Constraint_Disk_{i+1}"

# Solve the problem
problem.solve()

# Output results
n_disks = sum(y[i].varValue for i in range(M))
whichdisk = [next(i for i in range(M) if x[i][j].varValue == 1) for j in range(N)]

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(f'Total number of disks used: {n_disks}')
print(f'Files are distributed on disks: {whichdisk}')