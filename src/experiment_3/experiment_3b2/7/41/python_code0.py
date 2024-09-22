import pulp

# Data
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
N = len(data['size'])
capacity = data['capacity']
sizes = data['size']

# Create the problem
problem = pulp.LpProblem("File_Backup", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(N) for j in range(N)), cat='Binary')
y = pulp.LpVariable.dicts("y", range(N), cat='Binary')

# Objective Function
problem += pulp.lpSum(y[i] for i in range(N)), "Minimize the number of disks used"

# Constraints
# Constraint 1: Each file must be placed on exactly one disk
for j in range(N):
    problem += pulp.lpSum(x[i, j] for i in range(N)) == 1, f"FilePlacement_{j+1}"

# Constraint 2: The total size of the files on each disk should not exceed the disk's capacity
for i in range(N):
    problem += (pulp.lpSum(sizes[j] * x[i, j] for j in range(N)) 
                 <= capacity * y[i]), f"DiskCapacity_{i+1}"

# Constraint 3: Ensure files are only placed on used disks
for i in range(N):
    for j in range(N):
        problem += x[i, j] <= y[i], f"FileOnUsedDisk_{i+1}_{j+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')