import pulp

# Data from the JSON format
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
N = len(data['size'])
capacity = data['capacity']
size = data['size']

# Create the linear programming problem
problem = pulp.LpProblem("MinimizeFloppyDisks", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", (range(N), range(N)), cat='Binary')  # x[i][j] is 1 if file j is on disk i
y = pulp.LpVariable.dicts("y", range(N), cat='Binary')  # y[i] is 1 if disk i is used

# Objective Function: Minimize the number of disks used
problem += pulp.lpSum(y[i] for i in range(N)), "MinimizeDisks"

# Constraints
# 1. The sum of file sizes on each floppy disk cannot exceed the capacity
for i in range(N):
    problem += (pulp.lpSum(size[j] * x[i][j] for j in range(N)) <= capacity * y[i]), f"CapacityConstraint_{i}"

# 2. Each file must be placed on exactly one floppy disk
for j in range(N):
    problem += (pulp.lpSum(x[i][j] for i in range(N)) == 1), f"FilePlacement_{j}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')