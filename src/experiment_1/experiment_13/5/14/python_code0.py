import pulp

# Data
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
N = len(data['size'])
Capacity = data['capacity']
Size = data['size']

# Create a linear programming problem
problem = pulp.LpProblem("FloppyDiskPacking", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(N) for j in range(N)), cat='Binary')
y = pulp.LpVariable.dicts("y", range(N), cat='Binary')

# Objective function: Minimize the number of floppy disks used
problem += pulp.lpSum(y[i] for i in range(N)), "MinimizeFloppyDisksUsed"

# Constraints
# 1. The sum of file sizes on each floppy disk cannot exceed the capacity
for i in range(N):
    problem += pulp.lpSum(Size[j] * x[i, j] for j in range(N)) <= Capacity * y[i], f"CapacityConstraint_{i}"

# 2. Each file must be placed on exactly one floppy disk
for j in range(N):
    problem += pulp.lpSum(x[i, j] for i in range(N)) == 1, f"FilePlacementConstraint_{j}"

# Solve the problem
problem.solve()

# Output the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')