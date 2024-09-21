import pulp

# Data provided
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}

# Extract data
capacity = data['capacity']
sizes = data['size']
N = len(sizes)  # Number of files

# Define the problem
problem = pulp.LpProblem("Floppy_Disk_Optimization", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(N) for j in range(N)), cat='Binary')
y = pulp.LpVariable.dicts("y", (i for i in range(N)), cat='Binary')

# Objective function
problem += pulp.lpSum(y[i] for i in range(N)), "Minimize the number of floppy disks"

# Constraints
# Capacity constraint for each floppy disk
for i in range(N):
    problem += pulp.lpSum(sizes[j] * x[(i, j)] for j in range(N)) <= capacity * y[i], f"Capacity_constraint_floppy_{i}"

# Each file must be placed on exactly one floppy disk
for j in range(N):
    problem += pulp.lpSum(x[(i, j)] for i in range(N)) == 1, f"File_assignment_{j}"

# Solve the problem
problem.solve()

# Print the results
print(f'Status: {pulp.LpStatus[problem.status]}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')