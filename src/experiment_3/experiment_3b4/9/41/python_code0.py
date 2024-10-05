import pulp

# Data
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
capacity = data['capacity']
sizes = data['size']
num_files = len(sizes)
num_disks = num_files  # To simplify, assume maximum one file per disk in worst-case

# Problem
problem = pulp.LpProblem("Disk_Allocation_Problem", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(num_disks) for j in range(num_files)), cat='Binary')
y = pulp.LpVariable.dicts("y", (i for i in range(num_disks)), cat='Binary')

# Objective Function
problem += pulp.lpSum(y[i] for i in range(num_disks))

# Constraints
for i in range(num_disks):
    problem += pulp.lpSum(x[i, j] * sizes[j] for j in range(num_files)) <= capacity * y[i]

for j in range(num_files):
    problem += pulp.lpSum(x[i, j] for i in range(num_disks)) == 1

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')