import pulp

# Data from the provided JSON
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
N = len(data['size'])
capacity = data['capacity']
size = data['size']

# Create the linear programming problem
problem = pulp.LpProblem("Minimize_Floppy_Disks", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", (range(N), range(N)), 0, 1, pulp.LpBinary)
y = pulp.LpVariable.dicts("y", range(N), 0, 1, pulp.LpBinary)

# Objective function: Minimize the number of floppy disks used
problem += pulp.lpSum(y[i] for i in range(N)), "Minimize_Floppy_Disks"

# Constraints
# 1. The sum of file sizes on each floppy disk cannot exceed the capacity
for i in range(N):
    problem += pulp.lpSum(size[j] * x[i][j] for j in range(N)) <= capacity * y[i], f"Capacity_Constraint_{i}"

# 2. Each file must be placed on exactly one floppy disk
for j in range(N):
    problem += pulp.lpSum(x[i][j] for i in range(N)) == 1, f"File_Placement_Constraint_{j}"

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')