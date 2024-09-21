import pulp

# Data
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
capacity = data['capacity']
file_sizes = data['size']
N = len(file_sizes)

# Problem
problem = pulp.LpProblem("Floppy_Disk_Optimization", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(N) for j in range(N)), cat='Binary')
y = pulp.LpVariable.dicts("y", range(N), cat='Binary')

# Objective Function
problem += pulp.lpSum(y[i] for i in range(N)), "Minimize_number_of_floppy_disks"

# Constraints
# Sum of file sizes on each floppy disk cannot exceed capacity
for i in range(N):
    problem += pulp.lpSum(file_sizes[j] * x[i, j] for j in range(N)) <= capacity * y[i], f"Capacity_constraint_disk_{i}"

# Each file must be placed on exactly one floppy disk
for j in range(N):
    problem += pulp.lpSum(x[i, j] for i in range(N)) == 1, f"File_assignment_constraint_file_{j}"

# Solve
problem.solve()

# Output Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')