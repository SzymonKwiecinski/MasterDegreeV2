import pulp

# Data
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
capacity = data['capacity']
sizes = data['size']
N = len(sizes)

# Problem
problem = pulp.LpProblem("FloppyDiskOptimization", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(N) for j in range(N)), cat='Binary')
y = pulp.LpVariable.dicts("y", range(N), cat='Binary')

# Objective Function
problem += pulp.lpSum(y[i] for i in range(N)), "Minimize the number of floppy disks used"

# Constraints
# Capacity constraint for each floppy disk
for i in range(N):
    problem += pulp.lpSum(sizes[j] * x[i, j] for j in range(N)) <= capacity * y[i], f"Capacity_Constraint_{i}"

# Each file must be placed on exactly one floppy disk
for j in range(N):
    problem += pulp.lpSum(x[i, j] for i in range(N)) == 1, f"File_Placement_Constraint_{j}"

# Solve the problem
problem.solve()

# Output
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')