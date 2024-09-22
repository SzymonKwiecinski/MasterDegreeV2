import pulp
import json

# Input data in JSON format
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
capacity = data['capacity']
sizes = data['size']

# Number of files
N = len(sizes)

# Create the optimization problem
problem = pulp.LpProblem("FloppyDiskPacking", pulp.LpMinimize)

# Decision variables
# x[i][j] = 1 if file i is placed on disk j, 0 otherwise
x = pulp.LpVariable.dicts("x", (range(N), range(N)), 0, 1, pulp.LpBinary)

# Objective function: minimize number of disks used
problem += pulp.lpSum(x[i][j] for i in range(N) for j in range(N)), "Minimize_NofDisks"

# Each file must be placed on exactly one disk
for i in range(N):
    problem += pulp.lpSum(x[i][j] for j in range(N)) == 1, f"File_{i+1}_Placement"

# Capacity constraints for each disk
for j in range(N):
    problem += pulp.lpSum(sizes[i] * x[i][j] for i in range(N)) <= capacity, f"Capacity_Disk_{j+1}"

# Solve the problem
problem.solve()

# Extract the results
n_disks = sum(1 for j in range(N) if pulp.value(pulp.lpSum(x[i][j] for i in range(N))) > 0)
whichdisk = [next(j for j in range(N) if pulp.value(x[i][j]) == 1) for i in range(N)]

# Prepare output in JSON format
output = {
    "n_disks": n_disks,
    "whichdisk": whichdisk
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')