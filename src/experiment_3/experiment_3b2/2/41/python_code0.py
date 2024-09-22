import pulp
import json

# Data in JSON format
data_json = '{"capacity": 3, "size": [1, 2, 0.5, 1.5, 2.5]}'
data = json.loads(data_json)

# Parameters
M = 5  # Number of disks (you can modify this according to your requirement)
N = len(data['size'])  # Number of items
capacity = data['capacity']
size = data['size']

# Create the problem
problem = pulp.LpProblem("Minimize_Disks", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts('x', (range(M), range(N)), cat='Binary')
y = pulp.LpVariable.dicts('y', range(M), cat='Binary')

# Objective function
problem += pulp.lpSum(y[i] for i in range(M)), "Minimize_Disks_Used"

# Constraints
# Each item must be assigned to exactly one disk
for j in range(N):
    problem += pulp.lpSum(x[i][j] for i in range(M)) == 1, f"Assign_Item_{j}"

# Capacity constraints for each disk
for i in range(M):
    problem += pulp.lpSum(size[j] * x[i][j] for j in range(N)) <= capacity * y[i], f"Capacity_Constraint_{i}"

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')