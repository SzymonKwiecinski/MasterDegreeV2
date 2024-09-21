import pulp

# Data input
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
N = len(data['size'])
Capacity = data['capacity']
Size = data['size']

# Create the problem
problem = pulp.LpProblem("FloppyDiskPacking", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(N) for j in range(N)), cat='Binary')
y = pulp.LpVariable.dicts("y", range(N), cat='Binary')

# Objective Function
problem += pulp.lpSum(y[i] for i in range(N)), "MinimizeDiskUsage"

# Constraints
# Capacity constraints
for i in range(N):
    problem += (
        pulp.lpSum(Size[j] * x[i, j] for j in range(N)) <= Capacity * y[i],
        f"CapacityConstraint_{i}"
    )

# Each file must be placed on exactly one floppy disk
for j in range(N):
    problem += (
        pulp.lpSum(x[i, j] for i in range(N)) == 1,
        f"FilePlacement_{j}"
    )

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')