import pulp

# Data
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
size = data['size']
capacity = data['capacity']
N = len(size)
M = N  # Large constant set to N

# Problem
problem = pulp.LpProblem("Minimize_Number_of_Floppy_Disks", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(M) for j in range(N)), cat='Binary')
y = pulp.LpVariable.dicts("y", range(M), cat='Binary')

# Objective Function
problem += pulp.lpSum(y[i] for i in range(M)), "Minimize the number of disks used"

# Constraints
# Constraint 1: Total size on each disk does not exceed capacity
for i in range(M):
    problem += pulp.lpSum(x[i, j] * size[j] for j in range(N)) <= capacity * y[i], f"Capacity_Constraint_Disk_{i}"

# Constraint 2: Each file is placed on exactly one disk
for j in range(N):
    problem += pulp.lpSum(x[i, j] for i in range(M)) == 1, f"File_Placement_Constraint_{j}"

# Solve the problem
problem.solve()

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')