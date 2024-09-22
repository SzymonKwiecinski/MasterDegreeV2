import pulp

# Data
data = {
    'capacity': 3,
    'size': [1, 2, 0.5, 1.5, 2.5]
}

# Parameters
N = len(data['size'])  # Number of files
M = N  # Maximum potential number of disks
capacity = data['capacity']  # Capacity of each floppy disk
size = data['size']

# Problem
problem = pulp.LpProblem("Minimize_Floppy_Disks", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(M) for j in range(N)), cat='Binary')
y = pulp.LpVariable.dicts("y", (i for i in range(M)), cat='Binary')

# Objective Function
problem += pulp.lpSum(y[i] for i in range(M)), "Minimize number of disks used"

# Constraints
# Each file must be on one disk
for j in range(N):
    problem += pulp.lpSum(x[i, j] for i in range(M)) == 1, f"File_{j}_on_one_disk"

# Disk capacity and usage
for i in range(M):
    problem += pulp.lpSum(size[j] * x[i, j] for j in range(N)) <= capacity * y[i], f"Disk_{i}_capacity"

# Solve
problem.solve()

# Result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')