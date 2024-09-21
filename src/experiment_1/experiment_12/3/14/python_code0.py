import pulp

# Data from the JSON input
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
capacity = data['capacity']
sizes = data['size']
N = len(sizes)

# Initialize the problem
problem = pulp.LpProblem("Minimize_Floppy_Disks", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(N) for j in range(N)), cat='Binary')
y = pulp.LpVariable.dicts("y", (i for i in range(N)), cat='Binary')

# Objective function
problem += pulp.lpSum(y[i] for i in range(N)), "Minimize the number of floppy disks used"

# Constraints
# Capacity constraints
for i in range(N):
    problem += pulp.lpSum(sizes[j] * x[i, j] for j in range(N)) <= capacity * y[i], f"Capacity_constraint_disk_{i}"

# Assignment constraints
for j in range(N):
    problem += pulp.lpSum(x[i, j] for i in range(N)) == 1, f"Assignment_constraint_file_{j}"

# Solve the problem
problem.solve()

# Output the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')