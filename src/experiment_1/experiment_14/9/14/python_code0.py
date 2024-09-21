import pulp

# Data
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
Capacity = data['capacity']
Sizes = data['size']
N = len(Sizes)

# Problem
problem = pulp.LpProblem("FloppyDiskUsage", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(N) for j in range(N)), cat='Binary')
y = pulp.LpVariable.dicts("y", (i for i in range(N)), cat='Binary')

# Objective Function
problem += pulp.lpSum(y[i] for i in range(N)), "Minimize number of disks used"

# Constraints
# 1. Capacity constraint
for i in range(N):
    problem += pulp.lpSum(Sizes[j] * x[i, j] for j in range(N)) <= Capacity * y[i], f"Capacity_constraint_disk_{i}"

# 2. Each file on exactly one disk
for j in range(N):
    problem += pulp.lpSum(x[i, j] for i in range(N)) == 1, f"File_{j}_placement"

# Solving the problem
problem.solve()

# Output the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')