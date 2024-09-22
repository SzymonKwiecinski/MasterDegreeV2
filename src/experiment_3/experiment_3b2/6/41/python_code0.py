import pulp
import json

# Data from JSON format
data = json.loads('{"capacity": 3, "size": [1, 2, 0.5, 1.5, 2.5]}')
capacity = data['capacity']
sizes = data['size']

N = len(sizes)  # Number of files
M = N  # Assuming we have as many disks as files for flexibility

# Create the problem
problem = pulp.LpProblem("Disk_Packing_Problem", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", (range(M), range(N)), cat='Binary')
y = pulp.LpVariable.dicts("y", range(M), cat='Binary')

# Objective Function
problem += pulp.lpSum(y[i] for i in range(M)), "Minimize_Disks"

# Constraints

# Each file must be placed on exactly one disk
for j in range(N):
    problem += pulp.lpSum(x[i][j] for i in range(M)) == 1, f"File_{j}_Placement"

# Total size of files on each disk must not exceed its capacity
for i in range(M):
    problem += pulp.lpSum(sizes[j] * x[i][j] for j in range(N)) <= capacity * y[i], f"Disk_{i}_Capacity"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')