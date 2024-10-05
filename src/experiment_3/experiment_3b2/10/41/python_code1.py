import pulp
import json

# Data provided in JSON format
data = json.loads('{"capacity": 3, "size": [1, 2, 0.5, 1.5, 2.5]}')
capacity = data['capacity']
file_sizes = data['size']

# Define the number of files and disks
N = len(file_sizes)
M = N  # Upper bound on the number of disks

# Create the LP problem
problem = pulp.LpProblem("Minimize_Floppy_Disks", pulp.LpMinimize)

# Define decision variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(M) for j in range(N)), cat='Binary')
y = pulp.LpVariable.dicts("y", range(M), cat='Binary')

# Objective function: Minimize the sum of used disks
problem += pulp.lpSum(y[i] for i in range(M))

# Constraints
# Constraint (1): The total size of files on each disk cannot exceed its capacity
for i in range(M):
    problem += pulp.lpSum(file_sizes[j] * x[(i, j)] for j in range(N)) <= capacity * y[i]

# Constraint (2): Each file must be assigned to exactly one disk
for j in range(N):
    problem += pulp.lpSum(x[(i, j)] for i in range(M)) == 1

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')