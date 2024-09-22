import pulp

# Data
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
capacity = data['capacity']
sizes = data['size']
N = len(sizes)  # Number of files

# Problem
problem = pulp.LpProblem("FloppyDiskUsage", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(N) for j in range(N)), cat='Binary')
y = pulp.LpVariable.dicts("y", [i for i in range(N)], cat='Binary')

# Objective Function
problem += pulp.lpSum(y[i] for i in range(N)), "Minimize number of disks used"

# Constraints
# Capacity Constraint
for i in range(N):
    problem += pulp.lpSum(sizes[j] * x[(i, j)] for j in range(N)) <= capacity * y[i], f"Capacity_Constraint_{i}"

# Each file on exactly one floppy disk
for j in range(N):
    problem += pulp.lpSum(x[(i, j)] for i in range(N)) == 1, f"File_Assignment_Constraint_{j}"

# Solve the problem
problem.solve()

# Print Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')