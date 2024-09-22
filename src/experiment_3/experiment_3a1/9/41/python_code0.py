import pulp

# Given data
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
C = data['capacity']
size = data['size']
N = len(size)

# Create the linear programming problem
problem = pulp.LpProblem("Floppy_Disk_Backup", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(N) for j in range(N)), cat='Binary')
n_d = pulp.LpVariable("n_d", lowBound=0, cat='Integer')

# Objective function: Minimize the total number of disks used
problem += n_d, "Total Number of Disks Used"

# Constraints
# Each file must be assigned to exactly one disk
for j in range(N):
    problem += pulp.lpSum(x[i, j] for i in range(N)) == 1, f"File_{j}_assignment"

# The total size of files on each disk cannot exceed the capacity
for i in range(N):
    problem += pulp.lpSum(size[j] * x[i, j] for j in range(N)) <= C, f"Disk_{i}_capacity"

# Number of disks used must be counted
for i in range(N):
    for j in range(N):
        problem += n_d >= x[i, j], f"Counting_disks_for_file_{j}_on_disk_{i}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')