import pulp
import json

# Load data
data = json.loads('{"capacity": 3, "size": [1, 2, 0.5, 1.5, 2.5]}')

# Parameters
N = len(data['size'])  # Number of files
M = N  # Maximum number of disks
capacity = data['capacity']
sizes = data['size']

# Create the problem
problem = pulp.LpProblem("File_Distribution", pulp.LpMinimize)

# Decision Variables
y = pulp.LpVariable.dicts("y", range(M), 0, 1, pulp.LpBinary)  # Disk usage
x = pulp.LpVariable.dicts("x", (range(M), range(N)), 0, 1, pulp.LpBinary)  # File assignment

# Objective Function
problem += pulp.lpSum(y[i] for i in range(M)), "Minimize number of disks used"

# Constraints
# Each file must be on one disk
for j in range(N):
    problem += pulp.lpSum(x[i][j] for i in range(M)) == 1, f"File_{j+1}_on_one_disk"

# Capacity constraint
for i in range(M):
    problem += pulp.lpSum(sizes[j] * x[i][j] for j in range(N)) <= capacity * y[i], f"Capacity_disk_{i+1}"

# Linking constraint
for i in range(M):
    for j in range(N):
        problem += x[i][j] <= y[i], f"Link_disk_{i+1}_file_{j+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')