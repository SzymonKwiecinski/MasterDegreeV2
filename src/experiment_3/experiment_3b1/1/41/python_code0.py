import pulp

# Data
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
C = data['capacity']
S = data['size']
N = len(S)

# Create the problem
problem = pulp.LpProblem("Floppy_Disk_Allocation", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", (range(N), range(N)), 0, 1, pulp.LpBinary)  # x[i][j]: 1 if file j is assigned to disk i
y = pulp.LpVariable.dicts("y", range(N), 0, 1, pulp.LpBinary)             # y[i]: 1 if disk i is used

# Objective Function
problem += pulp.lpSum(y[i] for i in range(N)), "Minimize_Disk_Usage"

# Constraints

# Disk capacity constraint
for i in range(N):
    problem += pulp.lpSum(S[j] * x[i][j] for j in range(N)) <= C * y[i], f"Capacity_Constraint_{i}"

# Each file is assigned to exactly one disk
for j in range(N):
    problem += pulp.lpSum(x[i][j] for i in range(N)) == 1, f"File_Assignment_Constraint_{j}"

# Solve the problem
problem.solve()

# Output results
n_disks = sum(pulp.value(y[i]) for i in range(N))
whichdisk = [next(i for i in range(N) if pulp.value(x[i][j]) == 1) for j in range(N)]

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(f'Total number of disks used: {n_disks}')
print(f'File assignments to disks: {whichdisk}')