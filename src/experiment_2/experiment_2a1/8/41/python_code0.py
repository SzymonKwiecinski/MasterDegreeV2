import pulp
import json

# Input data
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}

# Problem parameters
capacity = data['capacity']
sizes = data['size']
N = len(sizes)

# Create a linear programming problem
problem = pulp.LpProblem("FloppyDiskPacking", pulp.LpMinimize)

# Create binary decision variables
x = pulp.LpVariable.dicts("x", (range(N), range(N)), cat='Binary')

# Objective function: Minimize the number of disks used
problem += pulp.lpSum([x[i][j] for i in range(N) for j in range(N)]), "MinimizeDisks"

# Each file must be assigned to exactly one disk
for i in range(N):
    problem += pulp.lpSum([x[i][j] for j in range(N)]) == 1, f"FileAssigned_{i}"

# Capacity constraints for each disk
for j in range(N):
    problem += pulp.lpSum([sizes[i] * x[i][j] for i in range(N)]) <= capacity, f"DiskCapacity_{j}"

# Solve the problem
problem.solve()

# Collect results
n_disks = sum(1 for j in range(N) if any(x[i][j].varValue == 1 for i in range(N)))
whichdisk = [next(j for j in range(N) if x[i][j].varValue == 1) for i in range(N)]

# Output the results in the requested format
output = {
    "n_disks": int(n_disks),
    "whichdisk": whichdisk
}

print(json.dumps(output))

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')