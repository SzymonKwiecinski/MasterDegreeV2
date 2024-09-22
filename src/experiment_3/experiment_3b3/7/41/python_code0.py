import pulp

# Data
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
sizes = data['size']
capacity = data['capacity']

# Indices
J = range(len(sizes))
N = len(J)
# Assuming M (max disk number) is sufficiently large initially
M = len(sizes)

# Problem
problem = pulp.LpProblem("Minimize_Number_of_Disks", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("disk_used", range(M), cat='Binary')
y = pulp.LpVariable.dicts("file_on_disk", ((j, d) for j in J for d in range(M)), cat='Binary')

# Objective Function
problem += pulp.lpSum(x[d] for d in range(M)), "Total Number of Disks Used"

# Constraints
# Each file must be assigned to exactly one disk
for j in J:
    problem += pulp.lpSum(y[j, d] for d in range(M)) == 1, f"File_{j}_assignment"

# Disk capacity constraints
for d in range(M):
    problem += pulp.lpSum(sizes[j] * y[j, d] for j in J) <= capacity * x[d], f"Capacity_Constraint_Disk_{d}"

# A file can only be assigned if the disk is in use
for j in J:
    for d in range(M):
        problem += y[j, d] <= x[d], f"File_{j}_on_Disk_{d}_only_if_used"

# Max number of disks constraint
problem += pulp.lpSum(x[d] for d in range(M)) <= M, "Max_number_of_disks"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')