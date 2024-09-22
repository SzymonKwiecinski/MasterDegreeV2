import pulp

# Data
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
capacity = data['capacity']
sizes = data['size']

# Parameters
N = len(sizes)
M = N  # Setting upper bound for number of disks (each file on separate disk)

# Problem Definition
problem = pulp.LpProblem("Floppy Disk Backup Problem", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(M) for j in range(N)), cat='Binary')
y = pulp.LpVariable.dicts("y", range(M), cat='Binary')

# Objective Function
problem += pulp.lpSum(y[i] for i in range(M)), "Total Number of Disks Used"

# Constraints

# Each file must be assigned to exactly one disk
for j in range(N):
    problem += pulp.lpSum(x[i, j] for i in range(M)) == 1, f"File_{j}_assignment"

# Disk capacity constraints
for i in range(M):
    problem += pulp.lpSum(sizes[j] * x[i, j] for j in range(N)) <= capacity * y[i], f"Disk_{i}_capacity"

# File assignment constraint that file can only be on a used disk
for i in range(M):
    for j in range(N):
        problem += x[i, j] <= y[i], f"File_{j}_on_disk_{i}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')