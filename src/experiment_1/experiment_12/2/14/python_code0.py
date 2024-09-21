import pulp

# Data
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
capacity = data['capacity']
sizes = data['size']
N = len(sizes)

# Problem
problem = pulp.LpProblem("Minimize_Disks_Used", pulp.LpMinimize)

# Decision Variables
x = [[pulp.LpVariable(f"x_{i}_{j}", cat="Binary") for j in range(N)] for i in range(N)]
y = [pulp.LpVariable(f"y_{i}", cat="Binary") for i in range(N)]

# Objective Function
problem += pulp.lpSum(y), "Minimize the number of floppy disks used"

# Constraints
# Capacity constraint for each floppy disk
for i in range(N):
    problem += pulp.lpSum(sizes[j] * x[i][j] for j in range(N)) <= capacity * y[i]

# Each file must be placed on exactly one floppy disk
for j in range(N):
    problem += pulp.lpSum(x[i][j] for i in range(N)) == 1

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')